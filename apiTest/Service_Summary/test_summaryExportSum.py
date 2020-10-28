# -*- coding:utf-8 -*-
import json
import unittest
import urllib
from urllib.parse import urlencode, quote_plus, quote

import paramunittest
import urllib3
from requests import request

from common import commom
from common.Log import Log
from common.commom import logger
from common.configHTTP import Config_Http

local_config_HTTP=Config_Http()

summaryExportSum_excel=commom.get_excel("testCase.xlsx","summaryExportSum")
@paramunittest.parametrized(*summaryExportSum_excel)
class summaryExportSum(unittest.TestCase):
    def setUp(self):
        pass
    def setParameters(self,case_name,method,url,parameter,code,status,message):
        self.case_name = str(case_name)
        self.method = str(method)
        self.url = str(url)
        self.parameter = str(parameter)
        self.code = str(code)
        self.status = str(status)
        self.message = str(message)
    def test_summaryExportSum(self):
        login_cookies=commom.get_chatbot_login()
        hearders={"content-Type":"application/json;charset=UTF-8","Accept":"application/json,text/plain,*/*","Accept-Encoding":"gzip, deflate",
                  "cookie":login_cookies[0]}
        print(hearders)
        local_config_HTTP.get_Heardes(hearders)

        local_config_HTTP.get_Path(self.url)
        date=json.loads(self.parameter.encode("utf-8"))
        json_date=json.dumps(date)

        local_config_HTTP.get_data(json_date)
        print(json_date)
        print(type(json_date))
        try:
            if self.method == "POST":
                self.reponse = local_config_HTTP.set_post()

            elif self.method == "GET":
                self.reponse=local_config_HTTP.set_get()
            else:
                logger.warning("请求方式不支持")
                self.response="该请求方式不支持"
        except Exception as e:
            msg= "【%s】接口调用失败，%s"%(self.url,e)
            logger.error(msg)
            self.response=msg



        self.checkResult()

    def checkResult(self):

            self.header=self.reponse.headers
            if self.header["Content-Type"]=="application/octet-stream;charset=UTF-8":
                self.info=self.reponse.text
                self.assertIsNotNone(self.info,msg=None)
            elif self.header["Content-Type"]=="application/json;charset=UTF-8":
                self.info = self.reponse.json()
                print(self.info)
                print("self.info是", self.info)
                if self.reponse.status_code == 200 and self.info["success"] == True:
                    self.assertEqual(self.info["code"], int(float(self.code)))
                    self.assertEqual(self.info["message"], self.message)
                elif self.reponse.status_code == 200 and self.info["success"] == False:
                    self.assertEqual(self.info["code"], int(float(self.code)))
                    self.assertIn(self.info["message"], self.message)







if __name__=="__main__":
    unittest.main()



