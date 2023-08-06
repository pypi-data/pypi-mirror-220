import requests
import configparser
import argparse
import json
import os

def GET_USER_ACCESS_TOKEN(login_code=None, app_access_token=None, config_file=None):
    if config_file is None:
        config_file = 'feishu-config.ini'

    #print("Starting the process of getting the user access token.")

    # 确保配置文件存在
    if not os.path.exists(config_file):
        #print("The configuration file does not exist. Creating a new one.")
        with open(config_file, 'w') as f:
            pass

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    # 确保 TOKEN 部分存在
    if not config.has_section('TOKEN'):
        #print("The TOKEN section does not exist in the configuration file. Adding it.")
        config.add_section('TOKEN')

    # 从配置文件获取参数
    if not app_access_token:
        app_access_token = config.get('TOKEN', 'app_access_token', fallback=None)

    # 如果app_access_token不存在，需要用户先获取它
    if not app_access_token:
        raise ValueError("app_access_token not found in the configuration file. Please provide it or get it first.")

    # 构建请求URL和请求头
    url = "https://open.feishu.cn/open-apis/authen/v1/access_token"
    headers = {
        'Authorization': f'Bearer {app_access_token}',
        'Content-Type': 'application/json; charset=utf-8',
    }

    # 构建请求体
    payload = {
        "grant_type": "authorization_code",
        "code": login_code
    }

    #print("Sending the request to get the user access token.")
    # 发起请求
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_json = response.json()

    # 检查响应状态码
    if response.status_code != 200:
        print(f"HTTP Error: {response_json}")
        return None

    # 检查响应体中的 code
    if response_json.get('code') != 0:
        print(f"Response Error: {response_json}")
        return None

    # 更新配置文件
    if 'data' in response_json and 'access_token' in response_json['data']:
        config.set('TOKEN', 'user_access_token', response_json['data']['access_token'])
        # 如果存在 refresh_token，也保存到配置文件
        if 'refresh_token' in response_json['data']:
            #print("Refresh token found. Updating the configuration file.")
            config.set('TOKEN', 'refresh_token', response_json['data']['refresh_token'])
        with open(config_file, 'w', encoding='utf-8') as configfile:
            config.write(configfile)

    #print("Finished getting the user access token.")
    return response_json.get('data', {}).get('access_token'), response_json.get('data', {}).get('refresh_token')


def GET_USER_ACCESS_TOKEN_CMD():
    # 解析命令行参数
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--login_code', help='登录预授权码')
    parser.add_argument('--config_file', default='feishu-config.ini', help='config file path')
    args = parser.parse_args()

    # 获取登录码，优先从命令行参数获取，没有则从配置文件获取
    login_code = args.login_code
    config_file = args.config_file

    if not login_code:
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read(config_file, encoding='utf-8')
        login_code = config.get('TOKEN', 'login_code', fallback=None)

        if not login_code:
            raise ValueError("login_code is required either in command line argument or in the configuration file.")

    # 调用 GET_USER_ACCESS_TOKEN 函数，获取 user_access_token
    user_access_token, refresh_token = GET_USER_ACCESS_TOKEN(login_code, config_file=config_file)
    
    # 打印结果
    print(f'user_access_token: {user_access_token}')
    print(f'refresh_token: {refresh_token}')



# 主函数
if __name__ == "__main__":
    GET_USER_ACCESS_TOKEN_CMD()
