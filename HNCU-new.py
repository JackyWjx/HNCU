#Hncu
import requests
from lxml import etree
from bs4 import BeautifulSoup

login_url='http://******/zfca/login'
ll_url='http://******/?verify=******&userName=******&strSysDatetime=******&jsName=student&openType=_self&url=xs_main.aspx'#自己去抓，可重复使用
selecj_url='http://******/xscj.aspx?xh=******&xm=******&gnmkdm=N121604'

username='******'
password='******'
header={'Refer': 'http://******/zfca/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Host': '******'}
session=requests.Session()

response = session.get(login_url, headers=header)
cookies = response.cookies
for c in cookies:
    cookie = c.name + '=' + c.value
print('cookie-get:' + cookie)
selector = etree.HTML(response.text)
token = selector.xpath('//input[@name="lt"]/@value')[0]  # 解析出登陆所需的lt信息
print(token)
login_data={
'useValidateCode': '0',
            'isremenberme': '1',
            'ip':'',
            'username': username,
            'password': password,
            'losetime': '30',
            'lt': token,
            '_eventId': 'submit',
            'submit1':''
}
response = session.post(login_url, data=login_data, headers=header)
cookies = response.cookies
for c in cookies:
    cookie = c.name + '=' + c.value
print('cookie-post:' + cookie)
print(response.status_code)


response = session.get(ll_url, headers=header)
cookies = response.cookies
print(BeautifulSoup(response.text, 'lxml'))


response = session.get(selecj_url, headers=header,allow_redirects=False)
print(response.cookies)
print(response.status_code)
#selector = etree.HTML(response.text)
print(BeautifulSoup(response.text, 'lxml'))
soup=BeautifulSoup(response.text, 'lxml')
token = soup.find('input', attrs={'name': '__VIEWSTATE'})['value']
print(token)
data = {
      '__VIEWSTATE':token,
      'ddlXN': '',
      'ddlXQ':'' ,
      'txtQSCJ':'0',
      'txtZZCJ': '100',
      'Button5':''
}
response = session.post(selecj_url,data = data, headers=header)
print(BeautifulSoup(response.text, 'lxml'))
soup =BeautifulSoup(response.text, 'lxml')
Score_lists = soup.find('table',attrs={'class': 'datelist'} )
Score_subjects = Score_lists.find_all('tr')

for trs in Score_subjects:
    # print(trs.text)
    for te in trs:
        try:
            te = te.string.lstrip()  # 清除字符串左边的空格
        except:
            te = '无'
        print(te, end='   ')
    print()
