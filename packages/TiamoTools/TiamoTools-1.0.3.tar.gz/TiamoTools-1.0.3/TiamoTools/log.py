import os
import time
import logging


class Log:
    def __init__(self, logger=None, file_dir='./log'):
        """
        指定保存日志的文件路径，日志级别，以及调用文件
        将日志存入到指定的文件中
        """
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        # 创建一个handler，用于写入日志文件
        self.log_time = time.strftime('%Y_%m_%d')
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        self.log_name = os.path.join(file_dir, time.strftime('%Y_%m_%d') + '.log')
        fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')
        fh.setLevel(logging.INFO)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def get_log(self):
        return self.logger
