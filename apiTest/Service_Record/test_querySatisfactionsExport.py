import unittest

import paramunittest

import common
from common import commom, configHTTP
from common.Log import Log

local_cinfig_Http=configHTTP.Config_Http()

querySatisfactionsExport_excel=commom.get_excel("testCase.xlsx","querySatisfactionsExport")





@paramunittest.parametrized(*querySatisfactionsExport_excel)
class querySatisfactionsExport(unittest.TestCase):
    def setUp(self):
        pass
    def setParameters(self,case_name,method,url,parameter,code,status,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        self.status=str(status)
        self.message=str(message)


    def test_querySatisfactionsExport(self):
        login_cookie=commom.get_chatbot_login()
        headers={"Content-Type":"application/json;charset=UTF-8","cookie":login_cookie[0]}
        local_cinfig_Http.get_Heardes(headers)
        #local_cinfig_Http.get_cookies(login_cookie)
        local_cinfig_Http.get_Path(self.url)
        #self.parameter.encode("utf-8")
        local_cinfig_Http.get_data(self.parameter)
        self.reponse=local_cinfig_Http.set_post()
        self.checkResult()

    def checkResult(self):
        self.header=self.reponse.headers

        if self.header["Content-Type"] == "application/octet-stream;charset=UTF-8":
            self.info = self.reponse.text
            self.assertIsNotNone(self.info, msg=None)
        elif self.header["Content-Type"] == "application/json;charset=UTF-8":
            self.info = self.reponse.json()
            print(self.info)
            print("self.info是", self.info)
            if self.reponse.status_code == 200 and self.info["success"] == True:
                self.assertEqual(self.info["code"], int(float(self.code)))
                self.assertEqual(self.info["message"], self.message)
            elif self.reponse.status_code == 200 and self.info["success"] == False:
                self.assertEqual(self.info["code"], int(float(self.code)))
                self.assertIn(self.info["message"], self.message)


if __name__== "__main__":
    unittest.main()














