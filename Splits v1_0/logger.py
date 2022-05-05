import datetime
import logging
import os


def get_logger() -> logging.Logger:
    logging.basicConfig(
        filename=get_log_filename(),
        filemode='a',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m-%d-%Y %I:%M:%S %p',
        level=logging.INFO,
    )
    return logging.getLogger()


def get_log_filename() -> str:
    log_folder = "Log"
    if not os.path.exists(log_folder):
        try:
            os.mkdir(log_folder)
        except FileExistsError:
            pass
    time_now = str(datetime.datetime.today().date())
    for char in ['-', ':', ".", " "]:
        time_now = time_now.replace(char, '_')
    return "Log/LOG_" + time_now + ".log"

logger = get_logger()

if __name__ == "__main__":
    pass
