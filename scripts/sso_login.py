from scripts.handle_request import HandleRequest
from scripts.handle_yaml import t_yaml
from scripts.handle_path import TOKEN_FILE_PATH


my_request = HandleRequest()


def get_token():

    res = my_request.send("https://sso.thingsmatrix.co/v1/oauth/token?client_id=public-client&client_secret=public-client&"
                "grant_type=password&username=autotest@gmail.com&password=9c085d2d884347ac3014c3eae9a38c23")
    login_res = res.json()

    token = login_res.get('data').get('access_token')

    access_token = 'Bearer ' + token
    data = {'account': {'access_token': access_token}}

    t_yaml.write(data, TOKEN_FILE_PATH)


if  __name__ == '__main__':
    get_token()

