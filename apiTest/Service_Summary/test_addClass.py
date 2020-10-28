import json
import unittest
from urllib import parse

import paramunittest

from common import commom, configHTTP
from common.commom import logger

local_config_http=configHTTP.Config_Http()
addclass_excel=commom.get_excel("testCase.xlsx","newAddClass")
@paramunittest.parametrized(*addclass_excel)
class addClass(unittest.TestCase):
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
        print(self.parameter)

    def test_addClass(self):
        login_cookies=commom.get_chatbot_login()
        header={"content-Type":"application/x-www-form-urlencoded,charset=UTF-8","Accept":"application/json, text/plain, */*","cookie":login_cookies[0]}
        local_config_http.get_Heardes(header)
        send_param={"className":"开心的一笔","parentClassId":"0"}
        print(self.data_dase())



        #date=json.dumps(self.parameter)
        #json_data=json.loads(date)
        #print(json_data)
        local_config_http.get_data(send_param)
        local_config_http.get_Path(self.url)
        try:
            if self.method=="POST":
                self.reponse=local_config_http.set_post()
            elif self.method== "GET":
                self.reponse=local_config_http.set_get()
            else:
                logger.warning("请求方式不对")
        except Exception as e:
            msg = "【%s】接口调用失败，%s" % (self.url, e)
            logger.error(msg)


        self.checkResult()

    def description(self):
        return  self.case_name
    def data_dase(self):
        conn=local_config_http.get_datebase()
        couur=conn.cursor()
        sql="select * from public_customer"
        a=couur.executemany(sql)
        print(a[0])

    def checkResult(self):
        self.header = self.reponse.headers
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


if __name__=="__main__":
    unittest.main()



