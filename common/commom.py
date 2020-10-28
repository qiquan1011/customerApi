import json
import os

import requests
from xlrd import open_workbook

import readConfig
from common import configHTTP
from common.Log import Log

local_read_Config=readConfig
local_config_Http=configHTTP.Config_Http()
porDir=local_read_Config.porDir
logger=Log().logger
chat_cl=[]
customer_cl=[]
chatbot_cl=[]
#获取后台登录cookie
def get_chatbot_login():
    send_pearm={"username":"zhang777","password":"123123","isRememberMe":"false"}
    #baseUrl=local_read_Config.get_HTTP("baseUrl")
    header={"Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*"}
    login_response=requests.post("http://v5-dev-customer.faqrobot.net/admin/login",params=send_pearm,headers=header)
    print(login_response.cookies)

    chatbot_cookies=requests.utils.dict_from_cookiejar(login_response.cookies)
    if len(chat_cl)>0 :
        del chat_cl[-len(chat_cl):]
    for k, v in chatbot_cookies.items():
        if k + ":" + v:
            s = k + "=" + v
            chat_cl.append(s)
    login_chat_cookies=";".join(chat_cl)


    #url = "http://v5-dev-customer.faqrobot.net/customerservice/summary/exportSum"

    #payload = "{\"remark\":\"\",\"classId\":\"\",\"beginTime\":\"2020-05-17 00:00:00\",\"endTime\":\"2020-08-17 23:59:59\",\"visitorName\":\"游客18285154\",\"queryType\":2}"
    #headers = {
        #'Content-Type': 'application/json;charset=UTF-8',
        #'Accept':'application/json, text/plain, */*',
        #'Cookie':login_chat_cookies
    #}
    #print(headers)
    #response = requests.request("POST", url, headers=headers, data=payload)

    #print(response.text.encode('utf8'))



    print(login_chat_cookies)

    return login_chat_cookies,chatbot_cookies

def get_customer_login():
    send_pearm={"username":"rtest2","password":"123456abc","isRememberMe":"false"}
    #baseUrl = local_read_Config.get_HTTP("baseUrl")
    header={"Content-Type":"application/x-www-form-urlencoded","Authorization":"Basic bml5YXpob3U6MTIzNDU2YWJj","Referer":"http://v5-dev-customer.faqrobot.net/webcustomer/index_standard.html",
            "Accept": "application/json, text/plain, */*" }
    customer_login = requests.post("http://v5-dev-customer.faqrobot.net/customerservice/login",params=send_pearm,headers=header)
    customer_cookie=requests.utils.dict_from_cookiejar(customer_login.cookies)
    if len(customer_cl)>0:
        del customer_cl[-len(customer_cl):]
        print(customer_cl)
    for k, v in customer_cookie.items():
        if k + ":" + v:
            s = k + "=" + v

            customer_cl.append(s)
    login_customer_cookies=";".join(customer_cl)

    print(login_customer_cookies)
    return login_customer_cookies

#获取客服信息
def get_agentInfo():
    header={"cookie":get_customer_login()}
    response=requests.get("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/agentInfo",headers=header)
    print(response.json())
    tenantId=response.json()["data"]["agent"]["tenantId"]
    return tenantId


#客服上线技能组
def get_register():
    send_param=[{"tenantId":9,"groupId":"1","groupName":"售前技术","agentId":"25","agentName":"2","status":"ONLINE","orginStatus":"ONLINE"}]
    data=json.dumps(send_param)
    header={"Content-Type":"application/json;charset=UTF-8",
"cookie":get_customer_login()}
    register_response=requests.post("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/register",
                                    data=data,headers=header)
    print("客服上线技能组：",register_response.json())

#初始化机器人
def get_chabot():
    header={"Content-Type":"application/json"}
    reponse=requests.get("http://v5-dev-customer.faqrobot.net/chatbot/web/init/1577067263668?sysNum=1577067263668&sourceId=169&lang=zh_CN&_=1598505740753"
                         ,headers=header)
    get_chabot_cookie=requests.utils.dict_from_cookiejar(reponse.cookies)
    if len(chatbot_cl)>0:
        del chatbot_cl[-len(chatbot_cl):]
        print(chatbot_cl)
    for k, v in get_chabot_cookie.items():
        if k + ":" + v:
            s = k + "=" + v

            chatbot_cl.append(s)
    get_chabot_cookie=";".join(chatbot_cl)

    print("初始化后的cookie",get_chabot_cookie)
    return  get_chabot_cookie


#转人工
def get_visitor():
    cookies=get_chabot()

    header = {"Content-Type": "application/json","cookie":cookies,"Accept":"application/json, text/javascript, */*; q=0.01"}
    send_param={"content":"转人工","type":0}
    data=json.dumps(send_param)
    response=requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1577067263668?sourceId=169",
                           headers=header,data=data)
    print(response.json())
    vissitor_cookies=requests.utils.dict_from_cookiejar(response.cookies)
    print("cookies是：",vissitor_cookies)
    send_params = {"content": "售前技术", "type": 0, "x": 0, "y": 0}
    data_skill=json.dumps(send_params)
    response_skill=requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1577067263668?sourceId=169",
                           headers=header,data=data_skill)
    #print(response_skill.json())
#选择转接的技能组
#def get_skills():
    #cookies1=get_chabot()
    #print("cookies1是：",cookies1)
    #header = {"Content-Type": "application/json", "cookie":cookies1,
               #"Accept":"application/json, text/javascript, */*; q=0.01",
              #"Referer":"http://v5-dev-customer.faqrobot.net/webchatbot/chat.html?sysNum=1577067263668&sourceId=169&lang=zh_CN"}
    #send_param ={"content":"售前技术","type":0,"x":0,"y":0}
    #data = json.dumps(send_param)
    #response = requests.post("http://v5-dev-customer.faqrobot.net/chatbot/web/chat/1577067263668?sourceId=169",
                             # headers=header, data=data)
    #print("技能组是：",response.json())

#获取客服会话信息
def get_inService():
    header={"Content-Type":"application/json;charset=UTF-8","cookie":get_customer_login()}
    reponse=requests.get("http://v5-dev-customer.faqrobot.net/customerservice/webim/agent/inService?serviceType=single",
                         headers=header)
    service=reponse.json()["data"][0]
    print(service["service"])
    serviceId=service["service"]["serviceId"]
    serviceTime=service["service"]["beginTime"]
    visitorName=service["service"]["visitorName"]
    
    return  serviceId,serviceTime,visitorName










def show_return_msg(response):
    msg_url=response.url

    msg=response.text

    print("\n请求地址",msg_url)

    print("\n请求返回"+"\n" + json.dumps(json.loads(msg),ensure_ascii=False,sort_keys=True,indent=4))

#congexcel中读取测试用例
def get_excel(excel_name,sheet_name):
    cls=[]
    #获取excel路径
    excelPath=os.path.join(porDir,"testFile","case",excel_name)

    #打开文件
    try:
        file = open_workbook(excelPath)
        sheet = file.sheet_by_name(sheet_name)
        first_line = sheet.nrows
        for i in range(first_line):
            if sheet.row_values(i)[0] != u'case_name':
                cls.append(sheet.row_values(i))
        return cls
    except FileExistsError:
        logger.error("文件打开失败")



    #获取当前sheet页的首行

def get_dataBase():

    pass






get_customer_login()
get_register()
get_chabot()
get_visitor()

get_inService()



