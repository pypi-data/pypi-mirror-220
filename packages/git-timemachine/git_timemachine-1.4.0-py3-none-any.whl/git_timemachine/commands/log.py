import sys
import json

import click
from pygit2 import discover_repository, Repository  # pylint: disable=no-name-in-module


@click.command('log')
@click.pass_context
def log_command(ctx: click.Context):
    """Show commit logs of a repository in the specified format."""

    repo_dir = ctx.obj['repo_dir']

    repo = Repository(discover_repository(repo_dir))
    logs = [{
        'id': commit.id.hex,
        'tree_id': commit.tree_id.hex,
        'parents': [parent.id.hex for parent in commit.parents],
        'author': {
            'name': commit.author.name,
            'email': commit.author.email,
            'time': commit.author.time,
            'offset': commit.author.offset
        },
        'committer': {
            'name': commit.committer.name,
            'email': commit.committer.email,
            'time': commit.committer.time,
            'offset': commit.committer.offset
        },
        'gpg': None if commit.gpg_signature[0] is None else [gpg.decode('utf-8') for gpg in commit.gpg_signature],
        'message': commit.message
    } for commit in repo.walk(repo.head.target)]

    json.dump(logs, sys.stdout, ensure_ascii=False, indent=4)
