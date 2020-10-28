import json
import unittest

import paramunittest as paramunittest

from common import configHTTP, commom
from parameterized import parameterized

from common.Log import Log

from common.commom import get_chatbot_login, logger

local_config_Http=configHTTP.Config_Http()
queerySatisfaction_excel=commom.get_excel("testCase.xlsx","querySatisfactions")
@paramunittest.parametrized(*queerySatisfaction_excel)
class querySatisfaction(unittest.TestCase):
    def setUp(self):
        pass
    def setParameters(self,case_name,method,url,parameter,code,success,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        print("self.code是：",self.code)
        self.success=str(success)
        self.message=str(message)

    def description(self):
            return self.case_name

    def test_querySatisfaction(self):
        login_cookies = commom.get_chatbot_login()
        print(login_cookies)
        local_config_Http.get_cookies(login_cookies[1])
        local_config_Http.get_Path(self.url)
        local_config_Http.get_parm(self.parameter)
        try:
            if self.method == "POST":
                self.reponse = local_config_Http.set_post()
                print(self.reponse)
            elif self.method == "GET":
                self.reponse =local_config_Http.set_get()
            else:
                logger.warning("请求方式不支持")
                response = "该请求方式不支持"
        except Exception as e:
            msg ="【%S】接口调用失败,%s"%(self.url, e)
            logger.error(msg)
            response = msg
        #print("返回是：",self.repon)
        self.checkResult()


    def checkResult(self):

        self.info = self.reponse.json()


        #print(self.info)
        commom.show_return_msg(self.reponse)

        if self.reponse.status_code == 200 and self.info["success"]==True:
            self.assertEqual(self.info["code"], int(float(self.code)))
            self.assertEqual(self.info["message"], self.message)
        elif self.reponse.status_code == 200 and self.info["success"] ==False:
            self.assertEqual(self.info["code"], int(float(self.code)))
            self.assertIn(self.info["message"], self.message)

    def tearDown(self):
        pass

if __name__=="__main__":
    unittest.main()














