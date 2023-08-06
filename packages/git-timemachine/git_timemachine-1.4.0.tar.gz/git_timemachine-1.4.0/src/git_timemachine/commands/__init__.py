from .log import log_command
from .commit import commit_command
from .review import review_command
from .switch_date import switch_date_command

command_group = [log_command, commit_command, review_command, switch_date_command]
