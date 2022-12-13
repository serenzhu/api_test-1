import pytest
import allure

from scripts.handle_excel import HandleExcel
from scripts.handle_yaml import c_yaml
from scripts.handle_log import do_log
from scripts.handle_parameterize import Parameterize


class TestHome:
    excel = HandleExcel('home')   # 创建HandleExcel对象
    cases = excel.read_data_obj()     # 获取excel中home表单下的所有数据

    @pytest.mark.parametrize('case', cases)
    def test_group(self, case, init_login):
        allure.dynamic.title(case.title)
        # 1. 请求数据参数化
        new_data = Parameterize.to_param(case.data)
        # 2. 拼接完整的url并进行参数化
        new_url = c_yaml.read('api', 'prefix') + case.url
        # new_url = Parameterize.to_param(new_url)
        # 3. 向服务器发起请求
        res = init_login.send(url=new_url,  # url地址
                              method=case.method,    # 请求方法
                              data=new_data,   # 请求参数
                              is_json=True   # 是否以json格式来传递数据, 默认为True
                              )
        # 将相应报文中的数据转化为字典
        actual_value = res.json()

        # 获取用例的行号
        row = case.case_id + 1
        # 获取预期结果
        expected_result = case.expected
        msg = case.title    # 获取标题
        success_msg = c_yaml.read('msg', 'success_result')  # 获取用例执行成功的提示
        fail_msg = c_yaml.read('msg', 'fail_result')       # 获取用例执行失败的提示

        # 对返回的Code进行断言
        try:
            assert expected_result == actual_value.get('code')
            do_log.info(f"{msg}, 执行的结果为: {success_msg}\n")

        except AssertionError as e:
            do_log.error(f"{msg}, 执行的结果为: {fail_msg}\n具体异常为: {e}\n")
            raise e
        finally:
            self.excel.write_data(row=row,
                                  column=c_yaml.read("excel", "actual_col"),
                                  value=res.text)
            self.excel.write_data(row=row,
                                  column=c_yaml.read("excel", "result_col"),
                                  value=success_msg)
