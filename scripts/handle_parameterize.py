# -*- coding: utf-8 -*-
import re

from scripts.handle_yaml import c_yaml


class Parameterize:
    """
    参数化类
    """
    company_id_pattern = r'{company_id}'
    sim_group_id_pattern = r'{sim_group_id}'    # SIM Card Group ID
    sim_group_name_pattern = r'{sim_group_name}'    # SIM Card Group Name
    sim_group_description_pattern = r'{sim_group_description}'  # SIM Card Group Description
    first_sim_id_pattern = r'{first_sim_id}'    # Add SIM Card to Group列表返回的第一个SIM Card的id

    @classmethod
    def common_replace(cls, data):
        # 数据为空不做处理
        if data is None:
            pass

        # companyId正则匹配
        elif re.search(cls.company_id_pattern, data):
            company_id = c_yaml.read('account', 'companyId')
            data = re.sub(cls.company_id_pattern, company_id, data)

        return data

    @classmethod
    def sim_group_replace(cls, data):
        # 数据为空不做处理
        if data is None:
            pass

        # SIM Card Group Id正则匹配
        elif re.search(cls.sim_group_id_pattern, data):
            sim_card_group_id = getattr(cls, 'sim_card_group_id')
            data = re.sub(cls.sim_group_id_pattern, sim_card_group_id, data)

        # SIM Card Group Name正则匹配
        elif re.search(cls.sim_group_name_pattern, data):
            sim_card_group_name = getattr(cls, 'sim_card_group_name')
            data = re.sub(cls.sim_group_name_pattern, sim_card_group_name, data)

        # SIM Card Description正则匹配
        elif re.search(cls.sim_group_description_pattern, data):
            sim_card_group_description = getattr(cls, 'sim_card_group_description')
            data = re.sub(cls.sim_group_description_pattern, sim_card_group_description, data)

        return data

    @classmethod
    def sim_id_replace(cls, data):
        # 数据为空不做处理
        if data is None:
            pass
        # 添加SIM Card到组返回的第一个SIM Card Id正则匹配
        elif re.search(cls.first_sim_id_pattern, data):
            first_sim_id = getattr(cls, 'first_sim_id')
            data = re.sub(cls.first_sim_id_pattern, first_sim_id, data)

        return data

    @classmethod
    def to_param(cls, data):
        data = cls.common_replace(data)
        data = cls.sim_group_replace(data)
        data = cls.sim_id_replace(data)
        return data


