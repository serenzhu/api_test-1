import pytest
import allure

from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import c_yaml
from scripts.handle_log import do_log
from scripts.handle_mysql import do_mysql
from scripts.handle_parameterize import Parameterize


@pytest.mark.usefixtures("init_test_sim_group")
class TestAddGroup:
    add_group_sheet = HandleExcel('add_group')
    add_group_cases = add_group_sheet.read_data_obj()

    @pytest.mark.parametrize('case', add_group_cases)
    def test_add_group(self, case, init_test_sim_group):
        allure.dynamic.title(case.title)
        # 请求接口
        res = init_test_sim_group.request_interface(case.url, case.method, case.data)
        # 将相应报文中的数据转化为字典
        actual_value = res.json()
        # 是否需要查询数据库进行数据校验
        check_sql = case.check_sql
        if check_sql:
            sim_card_group_id = actual_value['data']['id']
            setattr(Parameterize, 'sim_card_group_id', sim_card_group_id)
            sim_card_group_name = actual_value['data']['name']
            setattr(Parameterize, 'sim_card_group_name', sim_card_group_name)
        # 对需要进行数据校验的SQL语句进行参数化
        check_sql = Parameterize.to_param(check_sql)
        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        expected_result = eval(case.expected)
        try:
            assert expected_result['code'] == actual_value.get('code')
            assert expected_result['message'] in actual_value.get('message')
            if check_sql:
                run_sql_result = do_mysql.run(check_sql)
                assert run_sql_result
            if case.flag:
                assert eval(Parameterize.to_param(case.data)).get('keyword') in res.text
            do_log.info(f"{case.title}, 执行的结果为: 通过")
            self.add_group_sheet.write_success_result(row)
        except AssertionError as e:
            do_log.error(f"{case.title}, 执行的结果为: 不通过。具体异常为: {e}\n")
            self.add_group_sheet.write_fail_result(row)
            raise e
        finally:
            self.add_group_sheet.write_response(row, res.text)


@pytest.mark.usefixtures("init_test_sim_group")
class TestEditGroup:
    edit_group_sheet = HandleExcel('update_group')
    edit_group_cases = edit_group_sheet.read_data_obj()

    @pytest.mark.parametrize('case', edit_group_cases)
    def test_edit_group(self, case, init_test_sim_group):
        allure.dynamic.title(case.title)
        # 请求接口
        res = init_test_sim_group.request_interface(case.url, case.method, case.data)
        # 将相应报文中的数据转化为字典
        actual_value = res.json()
        # 是否需要查询数据库进行数据校验
        check_sql = case.check_sql

        if check_sql:
            sim_card_group_id = actual_value['data']['id']
            setattr(Parameterize, 'sim_card_group_id', sim_card_group_id)

        # 对需要进行数据校验的SQL语句进行参数化
        check_sql = Parameterize.to_param(check_sql)
        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        expected_result = eval(case.expected)

        try:
            assert expected_result['code'] == actual_value.get('code')
            assert expected_result['message'] in actual_value.get('message')
            if check_sql:
                run_sql_result = do_mysql.run(check_sql)
                assert run_sql_result
            if case.flag:
                assert expected_result['name'] == actual_value.get('data').get('name')
                assert expected_result['description'] == actual_value.get('data').get('description')

            do_log.info(f"{case.title}, 执行的结果为: 通过")
            self.edit_group_sheet.write_success_result(row)
        except AssertionError as e:
            do_log.error(f"{case.title}, 执行的结果为: 不通过。具体异常为: {e}\n")
            self.edit_group_sheet.write_fail_result(row)
            raise e
        finally:
            self.edit_group_sheet.write_response(row, res.text)


@pytest.mark.usefixtures("init_test_sim_group")
class TestEditGroupSIM:
    edit_group_sim_sheet = HandleExcel('edit_group_sim')
    edit_group_sim_cases = edit_group_sim_sheet.read_data_obj()

    @pytest.mark.parametrize('case', edit_group_sim_cases)
    def test_edit_group_sim(self, case, init_test_sim_group):
        allure.dynamic.title(case.title)
        # 请求接口
        res = init_test_sim_group.request_interface(case.url, case.method, case.data)
        # 将相应报文中的数据转化为字典
        actual_value = res.json()
        # 是否需要查询数据库进行数据校验
        check_sql = case.check_sql

        if case.case_id == 1:
            sim_card_group_id = actual_value['data']['id']
            setattr(Parameterize, 'sim_card_group_id', sim_card_group_id)
        # 将返回的第一个SIM Card Id设置为动态属性，供后续接口使用
        if case.flag:
            sim_list_for_group = actual_value['data']['list']
            first_sim_id = sim_list_for_group[0]['id']
            setattr(Parameterize, 'first_sim_id', first_sim_id)
        # 对需要进行数据校验的SQL语句进行参数化
        check_sql = Parameterize.to_param(check_sql)
        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        expected_result = eval(case.expected)

        try:
            assert expected_result['code'] == actual_value.get('code')
            assert expected_result['message'] in actual_value.get('message')
            if check_sql:
                run_sql_result = do_mysql.run(check_sql)
                if case.case_id == 5:
                    assert not(run_sql_result)
                else:
                    assert run_sql_result
            do_log.info(f"{case.title}, 执行的结果为: 通过")
            self.edit_group_sim_sheet.write_success_result(row)
        except AssertionError as e:
            do_log.error(f"{case.title}, 执行的结果为: 不通过。具体异常为: {e}\n")
            self.edit_group_sim_sheet.write_fail_result(row)
            raise e
        finally:
            self.edit_group_sim_sheet.write_response(row, res.text)