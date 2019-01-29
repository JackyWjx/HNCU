#Hncu
import requests
from lxml import etree
from bs4 import BeautifulSoup

login_url='http://********/zfca/login'
main_url='http://********/xs_main.aspx?xh=2016051617'
selecj_url='http://********/xscj.aspx?xh=2016051617&xm=%CD%F5%BC%AA%CF%E9&gnmkdm=N121604'
username='********'
password='********'
header={'Refer': 'http://********/zfca/login',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36',
            'Host': '********'}
session=requests.Session()
requests.utils.add_dict_to_cookiejar(session.cookies,{"ASP.NET_SessionId":"0ftp4drb5uar0r55urffkobr"})#手动创建ASP.NET_SessionId
#登录：
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
#print('post_data:'+str(response.text))
#进入主页
response = session.get(main_url, headers=header)
print(response.cookies)
print(response.status_code)
#selector = etree.HTML(response.text)
print(BeautifulSoup(response.text, 'lxml'))

#查询成绩
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
