import requests
import lxml
from PIL import Image
from bs4 import BeautifulSoup
import json
from prettytable import PrettyTable
from aip import AipOcr
import time
import os
import sys

# https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
sckey    = ''   # 消息推送:http://sc.ftqq.com/
account  = ''   # 你的考号
password = ''   # 你的密码
ocrmod   = True # True 为自动识别验证码模式，False 为手打验证码模式

valid_url = 'http://wb.zk789.cn/ValidCode.ashx' # 验证码地址
post_url = 'http://wb.zk789.cn/Login.aspx' # 登陆地址
info_url = 'http://wb.zk789.cn/ApplyExamination/EditApplyExamination.aspx' # 报考信息
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
options = {}
options["language_type"] = "ENG"

# GIF 解析
def iter_frames(im):
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 消息推送:http://sc.ftqq.com/
def server_push(sckey, text, desp=''):
    url = "https://sc.ftqq.com/"+sckey+".send"
    try:
        r = requests.post(url, params={'text':text, 'desp':desp})
        r.encoding='utf-8'
        rjson = json.loads(r.text)
    except:
        print("server_push Error")
    else:
        if r.text.find('success') == -1:
            print("server_push Error: ", end='')
            print(rjson)
        else:
            print("server_push Success: ", end='')
            print(rjson)

# 倒计时
def countdown(num):
    for i in reversed(range(1, num)):
        time.sleep(1 - time.time() % 1) # sleep until a whole second boundary
        sys.stderr.write('\r将在%1d'%i+'秒后再次查询')
    print()
    print()

if account=='':
    print("你还没有填写你的考号,请在程序第17行\'\'之前填写你的考号")
    exit()
elif password=='':
    print("你还没有填写你的密码,请在程序第18行\'\'之前填写你的密码")
    exit()
elif APP_ID=='' or API_KEY=='' or SECRET_KEY=='':
    print("你已启动 OCR 模式,但是没有填写相关信息。请填写信息或使用手动打码模式(将19行设为ocrmod = False)。")
    exit()
else:
    pass

print("准考证号:"+account)
print("登录密码:"+password)

cycle = 0
while True:
    cycle = cycle+1
    print("第%d次查询"%cycle)
    print (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    tb = PrettyTable() # 初始化最后用于打印的表格
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
    valid_code = ""
    s = requests.Session()
    home = s.get(post_url,headers=headers)

    # 验证码处理
    valid = s.get(valid_url,headers=headers)
    with open("valcode.gif", "wb+") as myfile:
        myfile.write(valid.content)
    im = Image.open('valcode.gif')
    for i, frame in enumerate(iter_frames(im)):
        frame.save('test%d.png' % i,**frame.info)
    
    # 验证码OCR
    if ocrmod == True:
        baidu_ocr = get_file_content('test0.png')
        baidu_ocr_result = client.basicGeneral(baidu_ocr)
        for word in baidu_ocr_result['words_result']:
            print("OCR识别结果:"+word['words'])
            valid_code = word['words']
    else:
        im.show()
        valid_code = input('请输入验证码:')
        os.system('taskkill /f /im dllhost.exe >null') # 输入验证码后关闭 Windows 照片查看器进程,如果你用的其他图片查看器你需要改成其他的进程

    im.close()
    os.remove("valcode.gif")
    os.remove("test0.png")
    soup = BeautifulSoup(home.content,'lxml')
    try:
        viewstate = soup.find('input',id='__VIEWSTATE')['value'] # 获取隐藏属性
    except:
        print("网站抽风了")
        countdown(31)
        continue
    else:
        pass
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
        print("登陆失败！请检查 考号、密码 、验证码 是否正确！")
        countdown(11)
        continue
    
    name = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKSXM').string # 名字
    gender = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKSXB').string # 性别
    id = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZKZH').string # 准考证号
    uid = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblSFZH').string # 身份证号
    major_id = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZYBM').string # 专业代码
    major_str = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblZYMC').string # 专业名
    times = html_data.find(id='ctl00_ContentPlaceHolder1_aecEdit_fvData_lblKAOCBM').string # 考试次数
    exam_info = html_data.find('input', {'id':'ctl00_ContentPlaceHolder1_aecEdit_fvData_tbQxRl'}).get('value') # 座位信息

    print('考生姓名:'+name)
    print('性别:'+gender)
    print('准考证号:'+id)
    print('身份证号:'+uid)
    print('专业代码:'+major_id)
    print('专业名:'+major_str)
    print('考试次数:'+times)
    
    # 将座位信息格式化为 Json
    exam_info = exam_info.replace("qxmc", "\"qxmc\"")
    exam_info = exam_info.replace("'", "\"")
    exam_info = exam_info.replace("sjbm", "\"sjbm\"")
    exam_info = exam_info.replace("sjmc", "\"sjmc\"")
    exam_info = exam_info.replace("zdrs", "\"zdrs\"")
    exam_info = exam_info.replace("ybrs", "\"ybrs\"")
    exam_info = exam_info.replace("yxtb", "\"yxtb\"")
    exam_info_json = json.loads(exam_info)
    
    # 使用 PrettyTable 输出表格
    flag=False
    tb.field_names = (["考试场次", "县区名称", "考试时间", "最大人数", "剩余容量", "能否填报"])
    post_text = "座位信息有更新"
    post_desp = "| 地区 | 时间 | 最大 | 剩余 | 状态 |\n| :------:| :------: | :------: | :------: | :------: |\n"
    for i in exam_info_json:
        tb.add_row([i["sjbm"], i["qxmc"], i["sjmc"], i["zdrs"], i["zdrs"]-i["ybrs"], i["yxtb"]])
        post_desp += "| "+i["qxmc"]+" |"+" "+i["sjmc"]+" |"+" "+str(i["zdrs"])+" |"+" "+str(i["zdrs"]-i["ybrs"])+" |"+" "+i["yxtb"]+" |\n"
        if i["zdrs"]-i["ybrs"] > 0:
            flag=True
    if flag and ocrmod == True:
        server_push(sckey, post_text, post_desp)
    print(tb)
    print()
    countdown(61)