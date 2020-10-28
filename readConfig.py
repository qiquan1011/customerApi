import codecs
import configparser
import os
#获取配置文件路径
porDir=os.path.split(os.path.realpath(__file__))[0] #os.path.split()获取的集合
configPath= os.path.join(porDir,"config.ini")

class ReadConfig():
    def __init__(self):
        #porDir = os.path.split(os.path.realpath(__file__))[0]  # os.path.split()获取的集合
        #configPath = os.path.join(porDir, "config.ini")

        #获取配置文件内容
        with open(configPath,"r") as f:
            data=f.read()

            if data[:3]==codecs.BOM_UTF8:
                data=data[3:]
                file=codecs.open(configPath,"w")
                file.write(data)
                file.close()
            f.close()
    #创建实例对象获取配置文件内容
        self.read_Config=configparser.ConfigParser()
        self.read_Config.read(configPath)

    #获取对应配置信息
    def get_HTTP(self,name):
        http_Value=self.read_Config.get("http",name)
        return http_Value
    def get_DATA(self,name):
        data_Value=self.read_Config.get("DATABASE",name)
        return data_Value





