import json
import os

import pymysql as pymysql
import requests

import readConfig
from common.Log import Log

local_Read_Config=readConfig.ReadConfig()

class Config_Http():
    def __init__(self):
        global shcme,baseUrl,ip,username,password,port,dataname
        shcme = local_Read_Config.get_HTTP("schme")
        baseUrl = local_Read_Config.get_HTTP("baseUrl")
        ip = local_Read_Config.get_DATA("ip")
        username = local_Read_Config.get_DATA("username")
        password = local_Read_Config.get_DATA("password")
        port = local_Read_Config.get_DATA("port")
        dataname = local_Read_Config.get_DATA("dataname")
        self.logger=Log().logger
        self.header={}
        self.param={}
        self.data={}
        self.url=None
        self.file={}

    #获取请求路径
    def get_Path(self,url):
        self.url= shcme + baseUrl + url
        print(self.url)


    #设置请求头
    def get_Heardes(self,headers):

        self.header = headers
    def get_cookies(self,cookies):
        self.cookies=cookies

    #设置请求体
    #1,get请求传参 paerams 2，post请求传参 data
    def get_parm(self,param):
        self.params=param

    def get_data(self,data):
        self.data=data


    def get_file(self,filename):
        porDir=readConfig.porDir
        testFilePath=os.path.join(porDir,"testFile")
        if not os.path.exists(testFilePath):
            os.mkdir(testFilePath)
        if filename !="":
            filPath=testFilePath+ filename
            self.file = {"file",open(filPath,"rb") }
        if filename=="" or filename is None:
            self.state=1
    def get_datebase(self):
        mysql_conn=pymysql.Connect(
            host=ip,
            port=int(port),
            user=username,
            password=password,
            db=dataname,

        )
        print(mysql_conn)
        return mysql_conn



    #设置get请求

    def set_get(self):
        try:
            response=requests.get(self.url,params=self.params,headers=self.header,cookies=self.cookies)
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None
        #post请求
    def set_post(self):
        try:
            response = requests.post(url=self.url,headers=self.header,data=self.data)
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    def set_Post_With_File(self):
        try:
            response = requests.post(self.url,headers=self.header,data=self.data,file=self.file)
            return response
        except TimeoutError:
            self.logger.error("Time out")
            return None

    def set_Post_with_json(self):
        try:
            response=requests.post(self.url,headers=self.header,data=self.data)
            return response
        except TimeoutError:
            self.logger.error("Time out")
Config_Http().get_datebase()