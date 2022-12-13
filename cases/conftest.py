import pytest

from scripts.handle_mysql import do_mysql
from scripts.handle_request import HandleRequest
from scripts.handle_yaml import c_yaml, t_yaml
from scripts.handle_path import TOKEN_FILE_PATH

my_request = HandleRequest()


@pytest.fixture(scope="session")
def init_login():
    res = my_request.send(
        "https://sso.thingsmatrix.co/v1/oauth/token?client_id=public-client&client_secret=public-client&"
        "grant_type=password&username=autotest@gmail.com&password=9c085d2d884347ac3014c3eae9a38c23")
    login_res = res.json()
    token = login_res.get('data').get('access_token')
    access_token = 'Bearer ' + token
    data = {'account': {'access_token': access_token}}
    t_yaml.write(data, TOKEN_FILE_PATH)
    header = {"authorization": t_yaml.read('account', 'access_token'),
              "company-id": c_yaml.read('account', 'companyId'),
              "user-id": c_yaml.read('account', 'userId')}
    my_request.add_headers(header)
    yield my_request
    my_request.close()
    do_mysql.close()    # 关闭数据库连接


@pytest.fixture(scope="class")
def init_test_sim_group(init_login):
    yield init_login
    delete_group_sql = "DELETE FROM `tm_admin`.`simcard_group` WHERE company_code = 'C004512'"
    do_mysql.run(delete_group_sql)


@pytest.fixture(scope="function")
def init_test():
    print("*******start********")
    yield
    print("********end*********")

