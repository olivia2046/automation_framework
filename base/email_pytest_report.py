# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2020/10/2 20:27
desc: 基于https://github.com/qxf2/qxf2-page-object-model/blob/master/utils/email_pytest_report.py改造，增加邮件正文summary内容
'''

"""
Qxf2 Services: Utility script to send pytest test report email
* Supports both text and html formatted messages
* Supports text, html, image, audio files as an attachment
To Do:
* Provide support to add multiple attachment
Note:
* We added subject, email body message as per our need. You can update that as per your requirement.
* To generate html formatted test report, you need to use pytest-html plugin. To install it use command: pip install pytest-html
* To generate pytest_report.html file use following command from the root of repo e.g. py.test --html = testreport/pytest_report.html
* To generate pytest_report.log file use following command from the root of repo e.g. py.test -k example_form -r F -v > testreport/pytest_report.log
"""
import smtplib, zipfile
import os,sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
from email import encoders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lxml import etree
from lxml.etree import tostring
from base.get_config import get_email_config


class Email_Pytest_Report:
    "Class to email pytest report"

    def __init__(self):

        email_config = get_email_config()

        self.email_host = email_config['email_host']
        self.email_port = email_config['email_port']
        self.username = email_config['send_user']
        self.password = email_config['password']
        self.sender = email_config['send_user']
        self.targets = email_config['user_list']
        self.cc_list = email_config['cc_list']


    def get_test_report_data(self,html_body_flag= True,report_file_path= 'default'):
        "get test report data from pytest_report.html or pytest_report.txt or from user provided file"
        if html_body_flag == True and report_file_path == 'default':
            #To generate pytest_report.html file use following command e.g. py.test --html = log/pytest_report.html
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','testreport','pytest_report.html'))#Change report file name & address here
        elif html_body_flag == False and report_file_path == 'default':
            #To generate pytest_report.log file add ">pytest_report.log" at end of py.test command e.g. py.test -k example_form -r F -v > log/pytest_report.log
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','testreport','pytest_report.log'))#Change report file name & address here
        else:
            test_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),report_file_path))
        #check file exist or not
        if not os.path.exists(test_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file"%test_report_file)

        with open(test_report_file, "r", encoding='utf-8') as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line

        return testdata

    def get_plain_summary(self,html_body_flag= True,report_file_path= 'default'):
        html_data = self.get_test_report_data(html_body_flag, report_file_path)
        html = etree.HTML(html_data)

        xpath_prefix = "//html/body/h2[contains(text(), 'Summary')]/following-sibling::"

        n_pass = html.xpath("%sspan[@class='passed']/text()"%xpath_prefix)[0].strip(" passed")
        n_fail = html.xpath("%sspan[@class='failed']/text()"%xpath_prefix)[0].strip(" failed")
        n_error = html.xpath("%sspan[@class='error']/text()"%xpath_prefix)[0].strip(" errors")

        return n_pass,n_fail,n_error


    def get_test_summary_data(self,html_body_flag= True,report_file_path= 'default'):

        def remove_second_tr(item):
            item.remove(item.xpath("tr[2]")[0])
            return item

        html_data = self.get_test_report_data(html_body_flag,report_file_path)
        html = etree.HTML(html_data)
        # 不支持xpath 2.0的intersect
        #result_summary = html.xpath("//html/body/h2[contains(text(), 'Summary')]/following-sibling::node() intersect //html/body/h2[contains(text(), 'Results')]/preceding-sibling::node()")
        result_summary = html.xpath("//html/body/h2[contains(text(), 'Summary')]/following-sibling::node()"
                                    "[position() <= count(//html/body/h2[contains(text(), 'Results')]/preceding-sibling::node()) - 12]")
        summary_rows = html.xpath("//html/body/table[@id='results-table']/tbody[@class='failed results-table-row' or @class='error results-table-row']")

        with open(os.path.abspath(os.path.join(os.path.dirname(__file__),'pytest_summary_tmpl.html')), "r", encoding='utf-8') as tmpl:
            summary_data = '\n'.join(tmpl.readlines())

        summary_data = summary_data.replace("{result_summary}",'\n'.join([tostring(item,method='html').decode('utf-8') for item in result_summary if isinstance(item,etree._Element)]))
        summary_data = summary_data.replace("{summary_rows}", '\n'.join(
            [tostring(remove_second_tr(item),method='html').decode('utf-8') for item in summary_rows if
             isinstance(item, etree._Element)]))
        return summary_data


    def get_attachment(self,attachment_file_path = 'default',zipped=True):
        if zipped:
            # zip report and attach
            result_file_name = attachment_file_path.split(os.sep)[-1]
            zip_file_path = attachment_file_path.rstrip("html") + "zip"

            zip_file_name = zip_file_path.split(os.sep)[-1]
            zip_file_obj = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)
            zip_file_obj.write(attachment_file_path, result_file_name)
            zip_file_obj.close()
            # 构造附件，传送zip包

            with open(zip_file_path, 'rb')  as zip_file:
                # with open('testreport.zip', 'rb')  as zip_file:
                mime = MIMEBase('zip', 'zip', filename=zip_file_name)
                # 加上必要的头信息
                # mime.add_header('Content-Disposition', 'attachment', filename=('gb2312', '', zip_file_name))
                mime.add_header('Content-Disposition', 'attachment', filename=zip_file_name)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来
                mime.set_payload(zip_file.read())
                # 用Base64编码
            encoders.encode_base64(mime)
            return mime

        else:
            "Get attachment and attach it to mail"
            if attachment_file_path == 'default':
                #To generate pytest_report.html file use following command e.g. py.test --html = log/pytest_report.html
                attachment_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','testreport','pytest_report.html'))#Change report file name & address here
            else:
                attachment_report_file = os.path.abspath(os.path.join(os.path.dirname(__file__),attachment_file_path))
            #check file exist or not
            if not os.path.exists(attachment_report_file):
                raise Exception("File '%s' does not exist. Please provide valid file"%attachment_report_file)

            # Guess encoding type
            #ctype, encoding = mimetypes.guess_type(attachment_report_file)
            #if ctype is None or encoding is not None:
            #    ctype = 'application/octet-stream'  # Use a binary type as guess couldn't made
            ctype = 'application/octet-stream' # 解决邮件附件中文乱码问题

            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(attachment_report_file, encoding='utf-8')
                attachment = MIMEText(fp.read(), subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(attachment_report_file, 'rb')
                attachment = MIMEImage(fp.read(), subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(attachment_report_file, 'rb')
                attachment = MIMEAudio(fp.read(), subtype)
                fp.close()
            else:
                fp = open(attachment_report_file, 'rb')
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(attachment)
            # Set the filename parameter
            attachment.add_header('Content-Disposition',
                       'attachment',
                       filename=os.path.basename(attachment_report_file))

            return attachment


    def send_test_report_email(self,html_body_flag = True,attachment_flag = False,report_file_path = 'default',subject_prefix='test_report'):
        "send test report email"
        #1. Get html formatted email body data from report_file_path file (log/pytest_report.html) and do not add it as an attachment
        if html_body_flag == True and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path) #get html formatted test report data from testreport/pytest_report.html
            message = MIMEText(testdata,"html",_charset = 'utf-8') # Add html formatted test data to email

        #2. Get text formatted email body data from report_file_path file (log/pytest_report.log) and do not add it as an attachment
        elif html_body_flag == False and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path) #get html test report data from testreport/pytest_report.log
            message  = MIMEText(testdata) # Add text formatted test data to email

        #3. Add html formatted email body message along with an attachment file
        elif html_body_flag == True and attachment_flag == True:
            message = MIMEMultipart()
            #add html formatted body message to email
            # html_body = MIMEText('''<p>Hello,</p>
            #                          <p>&nbsp; &nbsp; &nbsp; &nbsp; Please check the attachment to see test built report.</p>
            #                          <p><strong>Note: For best UI experience, download the attachment and open using Chrome browser.</strong></p>
            #                      ''',"html") # Add/Update email body message here as per your requirement

            html_body = MIMEText(self.get_test_summary_data(html_body_flag,report_file_path), "html",_charset = 'utf-8')
            message.attach(html_body)

            #add attachment to email
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)

        #4. Add text formatted email body message along with an attachment file
        else:
            message = MIMEMultipart()
            #add test formatted body message to email
            plain_text_body = MIMEText('''Hello,\n\tPlease check attachment to see test built report.
                                       \n\nNote: For best UI experience, download the attachment and open  using Chrome browser.''')# Add/Update email body message here as per your requirement
            message.attach(plain_text_body)
            #add attachment to email
            attachment = self.get_attachment(report_file_path)
            message.attach(attachment)

        message['From'] = self.sender
        message['To'] = ';'.join(self.targets)
        message['Cc'] = ";".join(self.cc_list)

        n_pass,n_fail,n_error = self.get_plain_summary(html_body_flag,report_file_path)
        message['Subject'] = subject_prefix + "测试报告-Pass: %s Fail: %s Error: %s"%(n_pass,n_fail,n_error) # Update email subject here

        #Send Email
        server = smtplib.SMTP(self.email_host, self.email_port)
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.targets, message.as_string())
        server.quit()


#---USAGE EXAMPLES
if __name__=='__main__':
    print("Start of %s"%__file__)

    #Initialize the Email_Pytest_Report object
    email_obj = Email_Pytest_Report()
    #1. Send html formatted email body message with pytest report as an attachment
    #Here log/pytest_report.html is a default file. To generate pytest_report.html file use following command to the test e.g. py.test --html = log/pytest_report.html
    #email_obj.send_test_report_email(html_body_flag=True,attachment_flag=True,report_file_path= 'default')

    #Note: We commented below code to avoid sending multiple emails, you can try the other cases one by one to know more about email_pytest_report util.
    # 2. Send html formatted pytest report
    #email_obj.send_test_report_email(html_body_flag=True, attachment_flag=False, report_file_path='default')

    # 3. Send plain text formatted pytest report
    email_obj.send_test_report_email(html_body_flag=False, attachment_flag=False, report_file_path='default')

    '''
    
    
    #4. Send plain formatted email body message with pytest reports an attachment
    email_obj.send_test_report_email(html_body_flag=False,attachment_flag=True,report_file_path='default')
    #5. Send different type of attachment
    image_file = ("C:\\Users\\Public\\Pictures\\Sample Pictures\\Koala.jpg") # add attachment file here
    email_obj.send_test_report_email(html_body_flag=False,attachment_flag=True,report_file_path= image_file)
    '''
 