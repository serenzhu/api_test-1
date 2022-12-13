import pytest
import allure

from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import c_yaml,  t_yaml
from scripts.handle_log import do_log
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import do_mysql
from scripts.handle_parameterize import Parameterize


@pytest.mark.usefixtures("init_login")
class TestSimList:
    excel = HandleExcel('sim_card_list')   # 创建HandleExcel对象
    cases = excel.read_data_obj()     # 获取excel中group表单下的所有数据

    @pytest.mark.parametrize('case', cases)
    def test_group(self, case, init_login):
        allure.dynamic.title(case.title)
        # 1. 请求数据参数化
        new_data = Parameterize.to_param(case.data)
        # 2. 拼接完整的url并进行参数化
        new_url = c_yaml.read('api', 'prefix') + case.url
        new_url = Parameterize.to_param(new_url)
        # 3. 向服务器发起请求
        res = init_login.send(url=new_url,  # url地址
                              method=case.method,    # 请求方法
                              data=new_data,   # 请求参数
                              is_json=True   # 是否以json格式来传递数据, 默认为True
                              )
        # 将相应报文中的数据转化为字典
        actual_value = res.json()
        #
        # # 是否需要查询数据库进行数据校验
        # check_sql = case.check_sql
        #
        # # 将返回的SIM Card Group Id、Name、Description设置为Parameterize类动态属性
        # if case.case_id == 2:
        #     sim_card_group_id = actual_value['data']['id']
        #     sim_card_group_name = actual_value['data']['name']
        #     sim_card_group_description = actual_value['data']['description']
        #     setattr(Parameterize, 'sim_card_group_id', sim_card_group_id)
        #     setattr(Parameterize, 'sim_card_group_name', sim_card_group_name)
        #     setattr(Parameterize, 'sim_card_group_description', sim_card_group_description)
        # # 对需要进行数据校验的SQL语句进行参数化
        # check_sql = Parameterize.to_param(check_sql)
        #
        # # 将返回的第一个SIM Card Id设置为动态属性，供后续接口使用
        # if case.flag:
        #     sim_list_for_group = actual_value['data']['list']
        #     first_sim_id = sim_list_for_group[0]['id']
        #     setattr(Parameterize, 'first_sim_id', first_sim_id)
        #
        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        expected_result = eval(case.expected)
        msg = case.title    # 获取标题
        success_msg = c_yaml.read('msg', 'success_result')  # 获取用例执行成功的提示
        fail_msg = c_yaml.read('msg', 'fail_result')       # 获取用例执行失败的提示

        # 对返回的Code进行断言
        try:
            assert expected_result['code'] == actual_value.get('code')
            assert expected_result['message'] in actual_value.get('message')
            # # 根据返回的groupId查询数据库，判断组是否添加成功
            # if check_sql:
            #     add_group_result = do_mysql.run(check_sql)
            #     assert add_group_result
            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")
            self.excel.write_success_result(row)
        except AssertionError as e:
            do_log.error(f"{msg}, 执行的结果为: {fail_msg}\n具体异常为: {e}\n")
            self.excel.write_fail_result(row)
            raise e

        finally:
            self.excel.write_response(row=row, res_text=res.text)