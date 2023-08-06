# -*- coding: utf-8 -*-

import datetime
import logging.config
import logging.config as log_conf
import os
import coloredlogs

'''
 * @Author       : YKenan
 * @Description  : Log file configuration
'''

"""
Set the log output color style
"""
coloredlogs.DEFAULT_FIELD_STYLES = {
    'asctime': {
        'color': 'green'
    },
    'hostname': {
        'color': 'magenta'
    },
    'levelname': {
        'color': 'green',
        'bold': True
    },
    'request_id': {
        'color': 'yellow'
    },
    'name': {
        'color': 'blue'
    },
    'programname': {
        'color': 'cyan'
    },
    'threadName': {
        'color': 'yellow'
    }
}


class Logger:
    """
    Log initialization
    """

    def __init__(self, log_path: str = "", level: str = "DEBUG"):
        """
        Log initialization
        :param log_path: Log file output path
        :param level: Log printing level
        """
        self.log_path = log_path
        self.level = level
        # log  路径
        self.today = datetime.datetime.now().strftime("%Y%m%d")
        self.default_log_file = f"ykenan_log_{self.today}.log"

        log_path = self.getLogPath()

        # Define two log output formats
        standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' '[%(levelname)s] ===> %(message)s'
        simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] ===> %(message)s'

        # log 配置字典
        # logging_dic 第一层的所有的键不能改变
        self.logging_dic = {
            # 版本号
            'version': 1,
            # 固定写法
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': standard_format
                },
                'simple': {
                    '()': 'coloredlogs.ColoredFormatter',
                    'format': simple_format,
                    'datefmt': '%Y-%m-%d  %H:%M:%S'
                }
            },
            'filters': {},
            'handlers': {
                # 打印到终端的日志
                'sh': {
                    # 打印到屏幕
                    'class': 'logging.StreamHandler',
                    'level': 'DEBUG',
                    'formatter': 'simple'
                },
                # 打印到文件的日志,收集 info 及以上的日志
                'fh': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'standard',
                    # 日志文件
                    'filename': log_path,
                    # 日志大小 单位: 字节
                    'maxBytes': 1024 * 1024 * 1024,
                    # 轮转文件的个数
                    'backupCount': 5,
                    # 日志文件的编码
                    'encoding': 'utf-8',
                },
            },
            'loggers': {
                # logging.getLogger(__name__) 拿到的 logger 配置
                '': {
                    # 这里把上面定义的两个 handler 都加上，即 log 数据既写入文件又打印到屏幕
                    'handlers': ['sh', 'fh'],
                    'level': 'DEBUG',
                    # 向上（更高 level 的 logger）传递
                    'propagate': True,
                },
            },
        }

        # log 日志级别输颜色样式
        self.level_style = {
            'debug': {
                'color': 'white'
            },
            'info': {
                'color': 'green'
            },
            'warn': {
                'color': 'yellow'
            },
            'error': {
                'color': 'red',
                'bold': True,
            }
        }

    def getLogPath(self) -> str:
        """
        Get log output path
        :return:
        """
        # Determine whether it exists
        if self.log_path != "":
            log_path = self.log_path if self.log_path.endswith(".log") else os.path.join(self.log_path, self.default_log_file)
            # create folder
            if not os.path.exists(os.path.dirname(log_path)):
                os.makedirs(os.path.dirname(log_path))
        else:
            return os.path.join(self.default_log_file)

    def __setting__(self):
        """
        log 设置
        :return:
        """
        # 导入上面定义的 logging 配置 通过字典方式去配置这个日志
        log_conf.dictConfig(self.logging_dic)
        # 生成一个 log 实例  这里可以有参数 传给 task_id
        logger = logging.getLogger()
        # 设置颜色
        coloredlogs.install(level=self.level, level_styles=self.level_style, logger=logger)
        return logger

    @staticmethod
    def logger():
        """
        得到 log
        :return:
        """
        return Logger().__setting__()

    @staticmethod
    def debug(content: str):
        """
        log 日志 debug 信息
        :param content: 内容
        :return:
        """
        return Logger().__setting__().debug(content)

    @staticmethod
    def info(content: str):
        """
        log 日志 info 信息
        :param content: 内容
        :return:
        """
        return Logger().__setting__().info(content)

    @staticmethod
    def warn(content: str):
        """
        log 日志 warn 信息
        :param content: 内容
        :return:
        """
        return Logger().__setting__().warning(content)

    @staticmethod
    def error(content: str):
        """
        log 日志 error 信息
        :param content: 内容
        :return:
        """
        return Logger().__setting__().error(content)
