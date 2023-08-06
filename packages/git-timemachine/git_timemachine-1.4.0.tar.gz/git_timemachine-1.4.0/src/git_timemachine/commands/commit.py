import os
import random
import shlex
import subprocess
from datetime import datetime, timedelta
from typing import List

import click
from tabulate import tabulate
# pylint: disable=no-name-in-module
from pygit2 import discover_repository, Repository, Signature, GIT_STATUS_WT_NEW
from pygit2 import GIT_STATUS_INDEX_NEW, GIT_STATUS_INDEX_RENAMED, GIT_STATUS_INDEX_MODIFIED, GIT_STATUS_INDEX_DELETED, GIT_STATUS_INDEX_TYPECHANGE

from git_timemachine.types import ListParamType


@click.command('commit')
@click.option('-t', '--commit-time', help='Time node commit with', type=click.DateTime(formats=['%Y-%m-%dT%H:%M:%S%z']), required=False, default=None)
@click.option('-m', '--message', help='Message describing the commit', required=False)
@click.option('-r', '--random-range', help='Range for random seconds of commit time offset', type=ListParamType(length=2, item_type=int), default=[600, 3600])
@click.option('-e', '--external', help='External command to use for commit', type=str, required=False, default=None)
@click.option('--max-daily-commits', help='Number of maximum daily commits.', type=int, default=None, metavar='N')
@click.argument('args', nargs=-1)
@click.pass_context
def commit_command(ctx: click.Context, commit_time: datetime, message: str, random_range: List[int], external: str, args: List[str], max_daily_commits: int):
    """Record a commit on repository at the specified time node."""

    repo_dir = ctx.obj['repo_dir']
    states = ctx.obj['states']
    config = ctx.obj['config']

    if commit_time is None:
        commit_time = states.get('commit-time', datetime.now())

    repo = Repository(discover_repository(repo_dir))

    if not repo.head_is_unborn and commit_time.timestamp() < next(repo.walk(repo.head.target)).commit_time:
        ctx.fail('Commit time is earlier than HEAD.')

    repo_status = repo.status(untracked_files='no')
    if repo_status == {} or len([value for value in repo_status.values() if value < GIT_STATUS_WT_NEW]) < 1:
        ctx.fail(f'Nothing to commit or pending changes on repository: "{repo_dir}".')

    random.seed()
    commit_time += timedelta(seconds=random.randint(random_range[0], random_range[1]))

    if max_daily_commits is None:
        max_daily_commits = config['max-daily-commits']

    try:
        check_max_commits(repo, commit_time, max_daily_commits)
    except Exception as exc:
        ctx.fail(str(exc))

    if external is not None:
        commit_env = commit_time.replace(microsecond=0).astimezone().isoformat()
        subprocess.run(
            shlex.split(external) + list(args),
            cwd=repo_dir,
            env={**os.environ, 'GIT_AUTHOR_DATE': commit_env, 'GIT_COMMITTER_DATE': commit_env}
        )

        return

    parents = []
    if repo.head_is_unborn:
        try:
            git_config = repo.config.get_global_config()
            ref_name = git_config['init.defaultBranch'] if 'init.defaultBranch' in git_config else 'main'
        except OSError:
            ref_name = 'main'

        ref_name = f'refs/heads/{ref_name}'
    else:
        parents.append(repo.head.target)
        ref_name = repo.head.name

    signature = Signature(
        name=repo.default_signature.name,
        email=repo.default_signature.email,
        time=int(commit_time.replace(microsecond=0).timestamp()),
        encoding='utf-8',
        offset=int(commit_time.tzinfo.utcoffset(commit_time).seconds / 60)
    )

    tree = repo.index.write_tree()
    if tree is None:
        ctx.fail('Failed to write index tree.')

    if message is None:
        raise click.exceptions.MissingParameter(ctx=ctx, param=next(param for param in ctx.command.params if param.name == 'message'))

    oid = repo.create_commit(ref_name, signature, signature, message, tree, parents)

    if oid is None:
        ctx.fail('Failed to create commit.')

    states.set('commit-time', commit_time)

    status_texts = {
        GIT_STATUS_INDEX_NEW: 'new',
        GIT_STATUS_INDEX_MODIFIED: 'modified',
        GIT_STATUS_INDEX_DELETED: 'deleted',
        GIT_STATUS_INDEX_RENAMED: 'renamed',
        GIT_STATUS_INDEX_TYPECHANGE: 'type changed'
    }

    table = []
    for file in repo_status:
        table.append([
            ', '.join(map(lambda i: status_texts[i], filter(lambda i: repo_status[file] & i == i, status_texts.keys()))),
            file,
            oct(repo.index[file].mode & 0o100777)[2:]
        ])

    click.echo(f'commit: {oid.hex}')
    click.echo(f'author: {signature.name} <{signature.email}>')
    click.echo(f'committer: {signature.name} <{signature.email}>')
    click.echo(f'datetime: {datetime.fromtimestamp(signature.time).astimezone().isoformat()}')
    click.echo(f'message: {message}')
    click.echo()
    click.echo(tabulate(table, headers=['status', 'file']))


def check_max_commits(repo: Repository, commit_time: datetime, max_num: int):
    if repo.head_is_unborn or max_num == 0:
        return

    date_str = commit_time.strftime('%Y-%m-%d')

    commits = [commit for commit in repo.walk(repo.head.target) if datetime.fromtimestamp(commit.commit_time).strftime('%Y-%m-%d') == date_str]

    if len(commits) >= max_num:
        raise RuntimeError(f'Exceeded the daily commit limit: {max_num}.')
