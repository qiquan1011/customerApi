import json
import unittest

import paramunittest

from common import commom,  configHTTP
from common.Log import Log


local_Config_Http=configHTTP.Config_Http()
evaluationConfigSave_excel=commom.get_excel("testCase.xlsx","evaluationConfigSave")
@paramunittest.parametrized(*evaluationConfigSave_excel)
class evaluationConfigSave(unittest.TestCase):
    def setUp(self):
        pass

    def setParameters(self,case_name,method,url,parameter,code,status,message):
        self.case_name=str(case_name)
        self.method=str(method)
        self.url=str(url)
        self.parameter=str(parameter)
        self.code=str(code)
        self.message=str(message)

    def test_evaluationConfigSave(self):
        login_cookies=commom.get_chatbot_login()
        local_Config_Http.get_cookies(login_cookies)
        header={"Content-type":"application/json;charset=UTF-8","Cookie":login_cookies[0]}
        local_Config_Http.get_Heardes(header)
        local_Config_Http.get_Path(self.url)
        date=json.loads(self.parameter.encode("utf-8"))
        json_date=json.dumps(date)
        local_Config_Http.get_data(json_date)
        self.reponse=local_Config_Http.set_post()
        print(self.reponse.text)
        self.checkResult()

    def checkResult(self):
        commom.show_return_msg(self.reponse)

        self.header = self.reponse.headers
        print(self.header)
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
    def tearDown(self):
        pass
if __name__=="__main__":
    unittest.main()




