import codecs
import hashlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_list import EMAILS

class Generator:
    method = None

    def prep_string(self, hashable_string):
        if type(hashable_string) != str:
            raise ValueError("Password should be a string")
        if not str:
            raise ValueError("Password should not be empty")
        return hashable_string.encode()

    def hash(self, hashable_string, salt=None):
        hashable = self.prep_string(hashable_string)
        if salt:
            hash_result = self.method(hashable)
            hash_result.update(str(salt).encode())
            return hash_result.digest()
        else:
            hash_result = self.method(hashable).digest()
            return hash_result


class Sha512Generator(Generator):
    linux_num = 6
    method = hashlib.sha512


class Sha256Generator(Generator):
    linux_num = 5
    method = hashlib.sha256


class MD5Generator(Generator):
    linux_num = 1
    method = hashlib.md5


class Rot13Generator(Generator):
    linux_num = 0

    def hash(self, hashable_string, salt=None):
        return codecs.encode(hashable_string, "rot13").encode()
    
DATA_FILE = 'scraped_data_file'
from_addr = 'your_email@gmail.com'
to_addr = 'your_email@gmail.com'  #Or any generic email you want all recipients to see
bcc = EMAILS

msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = to_addr
msg['Subject'] = 'Subject Line'

with open(DATA_FILE) as f:
    body = f.read()

msg.attach(MIMEText(body, 'plain'))

smtp_server = smtplib.SMTP('smtp.gmail.com', 587) #Specify Gmail Mail server

smtp_server.ehlo() #Send mandatory 'hello' message to SMTP server

smtp_server.starttls() #Start TLS Encryption as we're not using SSL.

#Login to gmail: Account | Password
smtp_server.login(' your_email@gmail.com ', ' GMAIL APPLICATION ID ')

text = msg.as_string()

#Compile email list: From, To, Email body
smtp_server.sendmail(from_addr, [to_addr] + bcc, text)

#Close connection to SMTP server
smtp_server.quit()

#Test Message to verify all passes
print('Email sent successfully')
