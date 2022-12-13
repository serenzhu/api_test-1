# -*- coding: utf-8 -*-
import pymysql

from scripts.handle_yaml import c_yaml


class HandleMysql:
    def __init__(self):
        self.conn = pymysql.connect(host=c_yaml.read('mysql', 'host'),  # mysql服务器ip或者域名
                                    user=c_yaml.read('mysql', 'user'),  # 用户名
                                    password=c_yaml.read('mysql', 'password'),
                                    db=c_yaml.read('mysql', 'db'),  # 要连接的数据库名
                                    port=c_yaml.read('mysql', 'port'),  # 数据库端口号, 默认为3306
                                    charset='utf8',  # 数据库编码为utf8, 不能设为utf-8
                                    cursorclass=pymysql.cursors.DictCursor  # 指定返回的结果为字典或者嵌套字典的列表
                                    )
        self.cursor = self.conn.cursor()

    def run(self, sql, args=None, is_more=False):
        self.cursor.execute(sql, args)
        self.conn.commit()
        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()


do_mysql = HandleMysql()

