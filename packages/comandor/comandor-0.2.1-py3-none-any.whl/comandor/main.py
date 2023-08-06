from comandor.settings import loadSetting, Setting
from comandor.log import log, FORMAT, DATEFMT
from comandor.models import Action

from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm

from typing import Tuple, List

import subprocess as sp
import argparse


# read args
# return logfile, config, debug settings
def read_args() -> Tuple[str, str, bool]:
    parser = argparse.ArgumentParser()

    parser.add_argument('-l', "--logfile", type=str,
                        default="", help='where save logfile')
    parser.add_argument('-c', "--config", type=str, default=".comandor",
                        help='where you have config file')
    parser.add_argument('-d', "--debug", action='store_true',
                        required=False, help='run debug mod')

    args = parser.parse_args()
    logfile: str = args.logfile
    config: str = args.config
    debug: bool = args.debug
    return (logfile, config, debug)


# setup new config log and load setting form file
def newConfig(logfile: str, config: str, debug: bool) -> Setting:
    setting: Setting = loadSetting(config)

    level: int = log.INFO
    filename: str = ""
    filemode: str = ""

    if debug or setting.debug:
        level = log.DEBUG

    if logfile or setting.logfile:
        filename = logfile or str(setting.logfile)
        filemode = "w"

    log.basicConfig(
        filename=filename,
        filemode=filemode,
        level=level,
        format=FORMAT,
        datefmt=DATEFMT)

    if debug or setting.debug:
        log.debug("run debug mode!")

    log.info("logger configure!")
    log.info("loaded Setting!")
    return setting


# handle 2 type error
# 1- call error system error for your command
# 2- timeout error
def errorHandel(func):
    def wrapper(*a, **kw):
        try:
            return func(*a, **kw)

        except sp.CalledProcessError as err:
            log.error(
                f"Status : FAIL Code: {err.returncode} OutPut: {err.output}")
            return 1

        except sp.TimeoutExpired as e:
            log.error(e)
            return 1

    return wrapper


@errorHandel
def runActions(actions: List[Action]) -> int:
    for action in tqdm(actions):
        log.info(f"Processing {action.action_name}")

        command = f"cd {action.path} && " + "&& ".join(action.commands)

        log.debug(f"run this command: {command}")
        outstr = sp.check_output(command, shell=True, stderr=sp.STDOUT,
                                 timeout=action.timeout)
        log.info(outstr.decode())
        log.info(f"Done Process {action.action_name}")

    log.info("Done All Task!")
    return 0


def main() -> int:
    setting: Setting = newConfig(*read_args())

    log.info(f"start commander -> {setting.name}")

    with logging_redirect_tqdm():
        return runActions(setting.actions)


if __name__ == "__main__":
    exit(main())
