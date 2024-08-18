# -*- coding: utf-8 -*-
"""
| Created on Sun Aug 26 11:28:09 2018
| @author: olivia
"""

import smtplib,logging,os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase #附件
from email.header import Header
from email import encoders #转码
import sys,re
from lxml import etree
from bs4 import BeautifulSoup
sys.path.append('..')
from base.get_config import get_email_config


class SendEmail:
    
    def get_result(self,content):
        """从输入的html内容中获取测试结果字符串

        :param content: 输入的html内容（为生成的测试报告的内容）

        :return: 测试结果字符串
        """
        html = etree.HTML(content)
        testresult = html.xpath("//html/body/div[@class='heading']/p[3]/text()") #数组

        result_str = testresult[0].strip()

        # pattern = r"(Pass \d+)? ?(Failure \d+)? ?(Error \d+)?"
        # matches = re.match(pattern,result_str)

        # if matches is not None and (matches.group(2) is not None or matches.group(3) is not None):
        #     testpass = False
        # else:
        #     testpass = True

        #return result_str,testpass
        return result_str

    def get_failed_or_error_case_names(self, content):
        """从输入内容中获取失败或错误的用例名称

        :param content: 输入内容，即测试报告内容

        :return:  失败或错误的用例名称列表
        """
        html = etree.HTML(content)
        #print(content)
        rows = html.xpath("//table[@id='result_table']/tr") #content中没有tbody节点，why?
        prefix=""
        fail_or_error_cases=[]
        for row in rows:
            if "class" in row.keys() and row.get("class") is not None and row.get("class") in ["failClass","errorClass"]:
                prefix=row.xpath("./td[1]/text()")[0]
            elif "id" in row.keys() and row.get("id") is not None and row.get("id").startswith('ft'):
                if row.xpath("./td[@class='failCase']")!=[]:
                    fail_or_error_cases.append(prefix + '.' + row.xpath("./td[@class='failCase']/div/text()")[0])
                else:
                    fail_or_error_cases.append(prefix + '.' + row.xpath("./td[@class='errorCase']/div/text()")[0])
        #failed_cases = html.xpath("//html/body/table[@id='result_table']/tbody/tr/td[@class='failCase']/div")  # 数组
        #failed_cases = html.xpath("//tr/td[@class='failCase']/div/text()")  # 数组,content中没有tbody节点，why?
        logging.info(fail_or_error_cases)
        if fail_or_error_cases==[]:
            return ""
        else:
            return '\r\n'+'\r\n'.join(fail_or_error_cases)

    def _remove_script(self,content):
        """

        :param content:
        :return:
        """
        soup = BeautifulSoup(content, 'html.parser')
        soup.find('p', id='show_detail_line').decompose()
        links = soup.find_all('a')
        for n in links:
            n.decompose()
        return str(soup)

    def send_main(self, result_filepath, subject, condition):
        """发送测试报告邮件(将生成的测试报告文件压缩后作为附件)

        :param result_filepath: 生成的测试报告文件路径
        :param subject: 邮件主题
        :param condition: 发送邮件的条件：any-无条件发送邮件，fail-仅当有失败或错误用例时发送邮件

        :return: 无
        """
        email_config = get_email_config()
        email_host = email_config['email_host']
        send_user = email_config['send_user']
        password = email_config['password']
        user_list = email_config['user_list']
        cc_list = email_config['cc_list']
        
        f = open(result_filepath, 'rb')
        content = f.read()
        #f.close
        #self.send_mail(user_list,sub,content)

        # 编写html类型的邮件正文，MIMEtext()用于定义邮件正文
        #msg = MIMEText(content,_subtype='html',_charset='utf-8')
        # 编写带附件的邮件
        msg = MIMEMultipart()
        # 定义邮件正文标题
        result_str = self.get_result(content)
        pattern = r"(Pass \d+)? ?(Failure \d+)? ?(Error \d+)?"
        matches = re.match(pattern,result_str)

        if matches is not None and (matches.group(2) is not None or matches.group(3) is not None):
            testpass = False
        else:
            testpass = True

        msg['Subject'] = Header("%s-%s"%(subject,result_str))
        msg['From'] = send_user
        msg['Cc'] = ";".join(cc_list) #抄送给自己，为解决163邮箱554 DT:SPM问题
        msg['To'] = ";".join(user_list)
        # 邮件正文内容
        #body = MIMEText(self.remove_script(content), "html", "utf-8")
        #msg.attach(body)  # 挂起
        #msg.attach(MIMEText('', 'plain', 'utf-8'))
        body = MIMEText("Failed or Error Cases:\r\n" + self.get_failed_or_error_case_names(content), "html", "utf-8")
        msg.attach(body)  # 挂起

        # 压缩文件
        import zipfile

        result_file_name = result_filepath.split('/')[-1]
        zip_file_path = result_filepath.rstrip("html")+"zip"

        zip_file_name = zip_file_path.split('/')[-1]
        zip_file_obj = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
        zip_file_obj.write(result_filepath, result_file_name)
        zip_file_obj.close()
        # 构造附件，传送zip包
        #att1 = MIMEText(content, 'html', 'utf-8')
        #att1["Content-Type"] = 'application/octet-stream'
        #att1["Content-Disposition"] = 'attachment; filename="%s"' % zip_file_path.split('/')[-1]
        # msg.attach(att1)
        with open(zip_file_path,'rb')  as zip_file:
        #with open('testreport.zip', 'rb')  as zip_file:
            mime = MIMEBase('zip','zip',filename=zip_file_name)
            # 加上必要的头信息
            #mime.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', zip_file_name))
            mime.add_header('Content-Disposition', 'attachment', filename=zip_file_name)
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来
            mime.set_payload(zip_file.read())
            # 用Base64编码
        encoders.encode_base64(mime)
        msg.attach(mime)

        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        server = smtplib.SMTP(email_host,25)
        # server.ehlo()
        # server.starttls()
        server.login(send_user,password)

        if condition.lower()=='any' or (condition.lower()=='fail' and testpass is False):
            #server.sendmail(send_user,user_list+cc_list,msg.as_string())
            #server.send_message(msg,send_user,user_list+cc_list)
            server.send_message(msg)
        server.close()
