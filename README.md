# wb.zk789.cn_spider

四川省自考网上报名系统 爬虫 监控 推送

## 依赖

Python 3.5+

``` pip install requests lxml prettytable Pillow beautifulsoup4 baidu_aip ```

## 注意

程序默认会使用百度 OCR API 识别验证码完成登陆，该 OCR API 每日有 50000次 的免费调用量,对于本项目来说绰绰有余。有关该 API 的详细信息请移步至官方文档。

- https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html
- https://cloud.baidu.com/doc/OCR/OCR-API.html

当使用 OCR API 识别验证码时，会启用 Server酱 推送消息。有关该 API 的详细信息请移步至官方网站。

- http://sc.ftqq.com

## 配置

### 使用 OCR API

下载并解压项目打包文件

https://github.com/blackyau/wb.zk789.cn_spider/archive/master.zip

修改 ```wb.py```13至18行的信息

https://github.com/blackyau/wb.zk789.cn_spider/blob/master/wb.py#L13-L18


通过[百度云 管理中心](https://console.bce.baidu.com/ai/#/ai/ocr/app/list)申请 AppID, API Key, Secret Key

填写信息时请保留 ' ' 并将信息填入 ' ' 之间

```
APP_ID = '123456'
API_KEY = '1234567890123456'
SECRET_KEY = '12345678901234567890'
sckey    = '0123456789012345678901234567890' # 消息推送 http://sc.ftqq.com/
account  = '01234567890' # 你的考号
password = '01234567890' # 你的密码
```

### 手打验证码

下载并解压项目打包文件

https://github.com/blackyau/wb.zk789.cn_spider/archive/master.zip

修改 ```wb.py```17至18行的信息

https://github.com/blackyau/wb.zk789.cn_spider/blob/master/wb.py#L17-L18

填写信息时请保留 ' ' 并将信息填入 ' ' 之间

```
account  = ''    # 你的考号
password = ''    # 你的密码
ocrmod   = False # True 为自动识别验证码模式，False 为手打验证码模式
```

## 运行

Windows：在当前目录双击运行 ```run.bat``` 即可

其他：在当前目录执行 ```python wb.py``` 即可

# License
```
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                   Version 2, December 2004
 
Copyright (C) 2019 BlackYau <blackyau426@gmail.com>

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.
 
           DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
  TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

 1. You just DO WHAT THE FUCK YOU WANT TO.
```