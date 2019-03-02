import requests
import lxml
from PIL import Image
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable

try:
    fo = open("account.txt", "r")
except:
    print("无法打开 account.txt")
    exit()
else:
    pass

valid_url = 'http://wb.zk789.cn/ValidCode.ashx' # 验证码地址
post_url = 'http://wb.zk789.cn/Login.aspx' # 登陆地址
info_url = 'http://wb.zk789.cn/ApplyExamination/EditApplyExamination.aspx' # 报考信息
account = fo.readline().strip('\n') # 你的考号
password = fo.readline().strip('\n') # 你的密码

if account=='':
    print("你还没有填写你的考号,请在程序同一目录内。创建名为 account.txt 的文件，同时第一行写考号，第二行写密码。不要写入其他多余的内容。")
    exit()
elif password=='':
    print("你还没有填写你的密码,请在程序同一目录内。创建名为 account.txt 的文件，同时第一行写考号，第二行写密码。不要写入其他多余的内容。")
    exit()
else:
    pass

print("准考证号:"+account)
print("登录密码:"+password)

tb = PrettyTable()
headers = {
    'Host': 'wb.zk789.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://wb.zk789.cn',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://wb.zk789.cn/Login.aspx',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    
}

s = requests.Session()
home = s.get(post_url,headers=headers)
valid = s.get(valid_url,headers=headers)
f = open('valcode.bmp', 'wb')
f.write(valid.content)
f.close()
im = Image.open('valcode.bmp')
im.show()
im.close()
valid_code = input('请输入验证码:')
print()
soup = BeautifulSoup(home.content,'lxml')
viewstate = soup.find('input',id='__VIEWSTATE')['value'] # 获取隐藏属性
viewstategenerator = soup.find('input',id='__VIEWSTATEGENERATOR')['value']

post_data={
    '__EVENTTARGET':'',
    '__EVENTARGUMENT':'',
    '__VIEWSTATE': viewstate,
    '__VIEWSTATEGENERATOR': viewstategenerator,
    'ctl00$ContentPlaceHolder1$RBLKslx': '1',
    'ctl00$ContentPlaceHolder1$DDLDLFS': '2',
    'ctl00$ContentPlaceHolder1$tbDLFS': '2',
    'ctl00$ContentPlaceHolder1$ddlZKLB':'2',
    'ctl00$ContentPlaceHolder1$TBZjhm': account,
    'ctl00$ContentPlaceHolder1$TBPassWord': password,
    'ctl00$ContentPlaceHolder1$TBValidateCode': valid_code,
    'ctl00$ContentPlaceHolder1$BtnLogin':'__EVENTTARGET'
}


post = s.post(post_url,data=post_data,headers=headers) # 登陆
info = s.get(info_url,headers=headers) # 获取报考信息页
html_data = BeautifulSoup(info.text,'lxml') # 解析

if html_data.text.find("考生未登录或已登录超时") != -1:
    print("\033[1;35m登陆失败！请检查 考号、密码 、验证码 是否正确！\033[0m!")
    exit()

name = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKSXM').string # 名字
gender = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKSXB').string # 性别
id = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZKZH').string # 准考证号
uid = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblSFZH').string # 身份证号
major_id = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZYBM').string # 专业代码
major_str = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZYMC').string # 专业名
times = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKAOCBM').string # 考试次数
exam_info = html_data.find('input', {'id':'ctl00_ContentPlaceHolder1_aecEdit_fvData_tbQxRl'}).get('value')

print('考生姓名:'+name)
print('性别:'+gender)
print('准考证号:'+id)
print('身份证号:'+uid)
print('专业代码:'+major_id)
print('专业名:'+major_str)
print('考试次数:'+times)

exam_info = exam_info.replace("qxmc", "\"qxmc\"")
exam_info = exam_info.replace("'", "\"")
exam_info = exam_info.replace("sjbm", "\"sjbm\"")
exam_info = exam_info.replace("sjmc", "\"sjmc\"")
exam_info = exam_info.replace("zdrs", "\"zdrs\"")
exam_info = exam_info.replace("ybrs", "\"ybrs\"")
exam_info = exam_info.replace("yxtb", "\"yxtb\"")
exam_info_json = json.loads(exam_info)

tb.field_names = (["考试场次", "县区名称", "考试时间", "最大人数", "剩余容量", "能否填报"])
for i in exam_info_json:
    tb.add_row([i["sjbm"], i["qxmc"], i["sjmc"], i["zdrs"], i["zdrs"]-i["ybrs"], i["yxtb"]])
print(tb)
print()