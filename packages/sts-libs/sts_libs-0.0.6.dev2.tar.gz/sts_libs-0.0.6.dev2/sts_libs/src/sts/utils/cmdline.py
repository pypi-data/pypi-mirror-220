"""cmdline.py: Module to execute a command line."""
import logging

#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
from typing import Tuple, Union

from testinfra.backend.base import CommandResult

from sts import host_init

host = host_init()


def run(cmd: str) -> CommandResult:
    logging.info(f"Running command: '{cmd}'")
    cr: CommandResult = host.run(cmd)
    if cr.stdout:
        cr.stdout = cr.stdout.rstrip()
    if cr.stderr:
        cr.stderr = cr.stderr.rstrip()

    return host.run(cmd)


def run_ret_out(
    cmd: str,
    return_output: bool = False,
) -> Union[int, Tuple[int, str]]:
    """Runs cmd and returns rc int or rc int, output str tuple.

    For legacy compatibility only. TODO: remove it an it's usages
    """
    completed_command = host.run(cmd)

    if return_output:
        output = completed_command.stdout if completed_command.stdout else completed_command.stderr
        return completed_command.rc, output  # type: ignore [return-value]

    return completed_command.rc


def exists(cmd: str) -> bool:
    return host.exists(cmd)
