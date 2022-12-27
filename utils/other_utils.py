from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from tqdm import tqdm
#if os.name == 'nt':
#    import win32com.client as win32

def dummy_progress_bar(text):
    print(text)
    b = [a for a in tqdm(range(1, 1000000))]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def myfunc(*args):
    # do something with data
    pass

def my_threading(data_to_process:list):
    result_data = dict()
    with tqdm(total=len(data_to_process)) as progress_bar:
        with ThreadPoolExecutor(max_workers=len(data_to_process)) as executor:
            futures = [executor.submit(myfunc, data, progress_bar, result_data) for data in data_to_process]
            for future in as_completed(futures):
                result = future.result()

    return result_data
"""
class email:
    params_default = dict()

    def __init__(self, mail_to, subject):
        self.outlook = win32.Dispatch('outlook.application')
        self.mail = self.outlook.CreateItem(0)
        self.mail_to = mail_to
        self.subject = subject

    def add_attachments(self, attachments):
        for attachment in attachments:
            self.mail.Attachments.Add(os.path.abspath(attachment))

    def prepare_email(self, params):
        if 'mail_to' in params:
            self.mail.To = params['mail_to']
        else:
            self.mail.To = self.mail_to

        if 'subject' in params:
            self.mail.Subject = params['subject']
        else:
            self.mail.Subject = self.subject

        if 'body' in params:
            self.mail.Body = params['body']

        if 'cc' in params:
            self.mail.CC = params['cc']

    def send_report_by_email(self):
        self.mail.Send()
"""