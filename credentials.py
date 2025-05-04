import requests
import yaml

class Credentials:
    def __init__(self):
        with open("creds.yaml", "rb") as f:
            config = yaml.load(f, yaml.SafeLoader)
        self.__openai_api_key = config["OPENAI"]
        self.__deepseek_api_key = config["DEEPSEEK"]
        self.__gigachat_auth_key = config["GIGACHAT"]["AUTHORIZATION_KEY"]
        self.__gigachat_api_key = ""

    def __get_gigachat_auth_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        payload = {
            'scope': 'GIGACHAT_API_PERS'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': 'bb7b60b7-1098-4808-90d9-bc58416ac973',
            'Authorization': f'Basic {self.__gigachat_auth_key}'
        }
        response = requests.post(url, headers=headers, data=payload, verify=False)
        if response.status_code == 200:
            print("OK 200")
            response_json = response.json()
            return response_json["access_token"]
        else:
            raise Exception(f"STATUS CODE {response.status_code}")

    @property
    def openai_api_key(self):
        return self.__openai_api_key

    @property
    def deepseek_api_key(self):
        return self.__deepseek_api_key

    @property
    def gigachat_api_key(self):
        try:
            self.__gigachat_api_key = self.__get_gigachat_auth_token()
            return self.__gigachat_api_key
        except Exception as e:
            raise e