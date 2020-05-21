import requests
import re
import json
import os


COOKIES_FILE_PATH = 'taobao_login_cookies.txt'
s = requests.Session()


class TaoBaoLogin:

    def __init__(self, session):
        """
        账号登录对象
        :param username: 用户名
        :param ua: 淘宝的ua参数
        :param TPL_password_2: 加密后的密码
        """
        # 检测是否需要验证码的URL
        self.user_check_url = 'https://login.taobao.com/member/request_nick_check.do?_input_charset=utf-8'
        # 验证密码的URL
        self.verify_password_url = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F%3Fsprefer%3Dsypc00'
        
        # 淘宝个人 主页
        self.my_taobao_url = 'http://i.taobao.com/my_taobao.htm'

        # 用户名和密码
        self.username = "546501664@qq.com"
        self.TPL_password_2 = "558dad3cdf06cb0eea4be60b23a976c031bc6cdfc359e93a9aca8ca87efa0e6c9e729cc7102e401bcb7f777ef08cd93a2512455d067f658c60b27ce5b827fca834212e859897a69e4b021dc2a2eb7674d79a061e556f893038b2f50c92f2962b124cabeead24f40d3ecd54b1a27676ba1afb81f1795c5e7dd2cedf1f760e52d7"
        # 淘宝关键参数，包含用户浏览器等一些信息，很多地方会使用，从浏览器或抓包工具中复制，可重复使用
        self.ua = '121#tyQlkBf/K3wlVlhSxVaillXYDcvSfujVnWKY+EkI+doVOQwdEPv5lwLYAcFfKujVllgm+aAZLPhHA3rnE9jIlwXYLa+xNvo9lGuYZ7pIKM9STQrJEmD5lwLYAcfdK5jVVmgY+zP5KMlVA3rnEkD5bwLYOcMYuwBWIQQVBIbvsbc9MtFPD0rOaQVbbZ3glWfopCibkZ0T83Smbgi0CeIAFtZfkQWXnjxSpqLbCZeTM35O3piDkeHXmo60bZienqC9pCibCZ0T83BhbZs0keHaF9FbbZsbnjxSpXsbMqAT8fB2KNS0CMYlF9K6MEvPnnqMlCjFC6748u/mWMwApZyyt5c7uNsZzFtZw0JFJtPYh6r9+/JtaZsaadTvBKyLi8PbmT48b9rdjgk+0muytizFXDMtORWEtFs2AbQhI/U1WV7T/6KZig6f+q/hZBoPqJ2+pQYaWhMopDkS9ek7o+eeDmdjSjoGMq+cv3k4wmBSOdbSn1aIugwPrSIM+SlaNoWI+ttX8+BDj1CTOmdji4MWKZTE2cNN08lc9/5ogRXtqUYvX+EeGMK4hbotEligYpnZ4AHiQvWvWRkm80zp3ztymX0Wc0D4p2OIm9fJ395UYseg1WkGE0Kh/4oBOntxiJiDR7i2JU+BgfhxpVqjwwMPiNzoM3vLSL1wBgv1RoL9m+hbaBqjolU/dZjWQbSWkh21ooZOqfNhBq/ceRYXRrBauHdPHtEaLJevzXLklp7Weq2hg6pUQXzWv99ySpTcwdqt4Gi5S0I9EFajp3KWFXEHEKi0Ipcii05equGw/kl0mPiWYL5jjfqNVjQYp1YjhPO2DhdN6b0W+rGBCQhrAzgwrpnxrlJX92o2Nn8cjpzjbrqnO1Dilr+UkRdE+5ZrYukB5/V1gji9DCnkv+tsT2YCu0nXuIdbMjsWuwFS/CMPe9+S7JAkMTIzi/nMa1A0wmoMMBQtjX96rxP/99A2/YnibjxNh10nxHdbuxH2KBgekSzLKulpckinQwsSdjZ8aeNeamXEm1YZJmsMfYTkVzPd0N2/oFX+OXaCBPIwJvjiRoD2RuurlSrjZM2+fO3ljCwL9lfEQpI0kHoOh7eb7/A0tFFmbznp4K8x+Nxm1pr0Y09f'
        #session对象，共享cookies
        self.session = session
        # 请求超时时间
        self.timeout = 3

    def _user_check(self):
        """
        检测账号是否需要验证码
        :return:
        """
        data = {
            'username': self.username,
            'ua': self.ua
        }
        try:
            response = self.session.post(self.user_check_url, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('检查验证码请求失败,error:')
            raise(e)
        needcode = response.json()['needcode']
        print('是否需要滑块验证：{}'.format(needcode))
        return needcode
    
    def _verify_password(self):
        """
        验证用户名密码，并获取st码申请URL
        :return: 验证成功返回st码申请地址
        """
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://login.taobao.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F%3Fsprefer%3Dsypc00',
        }
        data = {
            'TPL_username': self.username,
            'ncoToken': 'f2bcf4f5322a3f2161107433994380e88d9b015b',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': 0,
            'newlogin': 0,
            'TPL_redirect_url': 'https://www.taobao.com/?sprefer=sypc00',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'loginType': '3',
            'gvfdcname': '10',
            'gvfdcre': '',
            'TPL_password_2': self.TPL_password_2,
            'loginASR': '1',
            'loginASRSuc': '1',
            'oslanguage': 'zh-CN',
            'sr': '1440*900',
            'osVer': '',
            'naviVer': 'chrome|78.039047',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://www.taobao.com/?sprefer=sypc00&useMobile=true',
            'showAssistantLink': False,
            'um_token': 'T66E7D8617934868E1636D99F408936EF453EC8625EB782448D509EC49D',
            'ua': self.ua
        }
        try:
            response = self.session.post(self.verify_password_url, headers=headers, data=data, timeout=self.timeout)
            response.raise_for_status()
        except Exception as e:
            print('验证用户名和密码请求失败，原因：')
            raise e
        # print(response.text)
        # 提取申请st码url
        apply_st_url_match = re.search(r'<script src="(.*?)"></script>', response.text)
        # 存在则返回
        if apply_st_url_match:
            print('验证用户名密码成功，st码申请地址：{}'.format(apply_st_url_match.group(1)))
            return apply_st_url_match.group(1)
        else:
            raise RuntimeError('用户名密码验证失败！response：{}'.format(response.text))

    def _serialization_cookies(self):
        """
        序列化cookies
        :return:
        """
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        with open(COOKIES_FILE_PATH, "w+", encoding='utf-8') as file:
            json.dump(cookies_dict, file)
            print('cookie保存成功')

    def _deserialization_cookies(self):
        """
        反序列化cookies
        :return:
        """
        with open(COOKIES_FILE_PATH, 'r+', encoding='utf-8') as file:
            cookies_dic = json.load(file)
            cookies = requests.utils.cookiejar_from_dict(cookies_dic)
            return cookies

    def _load_cookies(self):
        if not os.path.exists(COOKIES_FILE_PATH):
            return False
        self.session.cookies = self._deserialization_cookies()
        try:
            self.get_taobao_name()
        except Exception as e:
            os.remove(COOKIES_FILE_PATH)
            print('cookie已经过期，删除cookie文件')
            return False
        return True


    def login(self):
        #cookies文件
        if self._load_cookies():
            return; #无需再登录
        #验证
        self._user_check()
        apply_st_url = self._verify_password()
        try:
            response = self.session.get(apply_st_url)
            response.raise_for_status()
        except Exception as e:
            print('申请st码请求失败，原因：')
            raise e
        # 得到st码后不需要再请求...
        # data_text = re.search(r'callback((.*?));', response.text)
        # data_text_json = json.loads(data_text.group(1)[1:-1])
        # print(data_text_json['data'])
        try:
            response = self.session.get('http://i.taobao.com/my_taobao.htm')
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页请求失败！原因：')
            raise e
        # 登录成功
        self._serialization_cookies()

    def get_taobao_name(self):
        """
        获取淘宝昵称
        :return: 淘宝昵称
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }
        try:
            response = self.session.get(self.my_taobao_url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('获取淘宝主页失败')
            raise e
        # 提取淘宝昵称
        nick_name_match = re.search(r'<input id="mtb-nickname" type="hidden" value="(.*?)"/>', response.text)
        if nick_name_match:
            print('登录淘宝成功，你的用户名是：{}'.format(nick_name_match.group(1)))
            return nick_name_match.group(1)
        else:
            raise RuntimeError('获取淘宝昵称失败！response：{}'.format(response.text))


if __name__ == "__main__":
    tbl = TaoBaoLogin(s)
    tbl.login()
    tbl.get_taobao_name()