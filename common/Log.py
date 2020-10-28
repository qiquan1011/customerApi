import logging
import os
from datetime import datetime

import readConfig


porDit = readConfig.porDir

resultPath = os.path.join(porDit, "result")
print(resultPath)
# 创建日志文件夹

# 判断是否存在，不存在就创建result文件
if not os.path.exists(resultPath):
    os.mkdir(resultPath)
# 创建log日志文件
logPath = os.path.join(resultPath, str(datetime.now().strftime("%Y%m%d")))
print(logPath)
if not os.path.exists(logPath):
    os.mkdir(logPath)


class Log():
    def __init__(self):

        #创建logger实力
        self.logger=logging.getLogger()
        #设置日志等级
        self.logger.setLevel(logging.DEBUG)
        #hander处理器
        hander=logging.FileHandler(os.path.join(logPath,"outlog.log"),encoding="utf-8")
        print(hander)

        #formatter格式化器，指明输出日志规则
        formatter= logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s")
        #设置输出日志规则，格式和内容
        hander.setFormatter(formatter)

        #给logger实例增加处理器
        self.logger.addHandler(hander)

        #获取信息
    def get_logger(self):
       return self.logger

    def build_start_line(self,case_no):
        self.logger.info("....................." + case_no + "START...................." )

    def build_case_line(self,case_name,code,msg):
        self.logger.info(case_name + "-Code:" + code + "-msg:" +msg)

    def build_end_line(self,case_no):
        self.logger.info("......................" + case_no + "END......................")

    def get_report_path(self):
        report_path=os.path.join(logPath,"report.html")
        return report_path






