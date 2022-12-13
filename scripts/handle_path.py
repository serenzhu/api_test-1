# -*- coding: utf-8 -*-
import os


# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取配置文件所在的路径
CONFIGS_DIR = os.path.join(BASE_DIR, 'configs')

# 获取配置文件所在的路径
CONFIG_FILE_PATH = os.path.join(CONFIGS_DIR, 'config.yaml')
TOKEN_FILE_PATH = os.path.join(CONFIGS_DIR, 'token.yaml')


# 获取日志文件所在的目录路径
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# 获取报告文件所在的目录路径
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# 获取excel文件所在的目录路径
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 获取登录token文件的路径
USER_ACCOUNTS_FILE_PATH = os.path.join(CONFIGS_DIR, 'token.yaml')

# 测试用例模块所在目录路径
CASES_DIR = os.path.join(BASE_DIR, 'cases')
CONNECT_DIR = os.path.join(CASES_DIR, 'tmx_connect')


if __name__ == '__main__':
    print(REPORTS_DIR)
