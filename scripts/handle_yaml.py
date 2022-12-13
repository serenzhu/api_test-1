# -*- coding: utf-8 -*-
import yaml

from scripts.handle_path import CONFIG_FILE_PATH, TOKEN_FILE_PATH


class HandleYaml:
    def __init__(self, filename):
        with open(filename, encoding="utf-8") as one_file:
            self.data = yaml.full_load(one_file)

    def read(self, section, option):
        """
        读数据
        :param section: 区域名
        :param option: 选项名
        :return:
        """
        return self.data[section][option]

    @staticmethod
    def write(data, filename):
        """
        写数据
        :param data: 嵌套字典的字典
        :param filename: yaml文件路径
        :return:
        """
        with open(filename, mode="w", encoding="utf-8") as one_file:
            yaml.dump(data, one_file, allow_unicode=True)


c_yaml = HandleYaml(CONFIG_FILE_PATH)
t_yaml = HandleYaml(TOKEN_FILE_PATH)
