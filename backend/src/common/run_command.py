import subprocess
import shlex

from .log_method import application_logger
from .json_responses import debugmessages


# Method to execute the linux commands in terminal.
def command_run(cmd, verbose=False):
    archive_viewer_log = application_logger()
    try:
        cmd = shlex.split(cmd)
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False
        )
        std_out, std_err = process.communicate()
        if verbose:
            print(std_out.strip(), std_err)
        return std_out
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1998"])


# Method to execute the windows commands in command prompt.
def win_command_run(cmd, verbose=False):
    archive_viewer_log = application_logger()
    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=False
        )
        std_out, std_err = process.communicate()
        if verbose:
            print(std_out.strip(), std_err)
        return std_out
    except Exception as e:
        archive_viewer_log.exception(e, exc_info=True)
        archive_viewer_log.error(debugmessages["debug_messages"]["1998"])
