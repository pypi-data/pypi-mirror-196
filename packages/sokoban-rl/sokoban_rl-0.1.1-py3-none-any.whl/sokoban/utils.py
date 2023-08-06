import os
from datetime import datetime


class Logger:

    """
    Log episode history of Sokoban environment, not using Python logging module
    Note that this module is quite different from Python logging, although it looks like similar.
    """

    def __init__(self):
        self.path_output = None
        return

    def get_logger(self, path, prefix):

        """
        Get logger
            - Note : If the file name it is trying to create already exists in the path,
                     then it will create the file after adding index suffix.

        Parameters
        ----------
        path : str
            A path to log
        prefix : str
            A prefix of log file name
        """

        now_time = datetime.today().strftime('%Y%m%d_%H%M')
        idx = 1
        log_name = f"{prefix}_{now_time}.log"
        while log_name in os.listdir(path):
            idx += 1
            log_name = f"{prefix}_log_{now_time}_{idx}.log"
        self.path_output = os.path.join(path, log_name)
        f = open(self.path_output, 'w')
        f.close()
        return
    
    def write(self, logger_comment):

        """
        Write one line log
        """

        f = open(self.path_output, 'a')
        f.write(f"TIME : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {logger_comment}\n")
        f.close()
        return
