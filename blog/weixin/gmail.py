#!/usr/bin/python
#coding: utf-8
import imaplib
import config
import email

from formatter import AbstractFormatter,NullWriter
from htmllib import HTMLParser

class MyWriter(NullWriter):
    def __init__(self):
        NullWriter.__init__(self)
        self._bodyText=[]
    def send_flowing_data(self, data):
        self._bodyText.append(data)
    def _get_bodyText(self):
        return '\n'.join(self._bodyText)
    bodyText=property(_get_bodyText,None,None,'plain text from body')
class MyHtmlParser(HTMLParser):
    def do_meta(self, attrs):
        self.metas=attrs
class Gmail:
    def __init__(self, uid, pwd):
        self.uid = uid
        self.pwd = pwd

    def _html2txt(self, html):
        mywriter = MyWriter()
        myformatter = AbstractFormatter(mywriter)
        parser = MyHtmlParser(myformatter)
        parser.feed(html)
        return parser.formatter.writer.bodyText
    def _body2txt(self, body):
        result=''
        for part in body.walk():
            if part.is_multipart():
                continue
            ch=part.get_content_charset()
            if ch:
                html = unicode(part.get_payload(decode=True), ch).encode('utf-8')
            else:
                html = part.get_payload(decode=True).decode('gb2312').encode('utf-8')
            result += self._html2txt(html)
        return result

    def _getOne(self, conn, mid):
        tp,data=conn.fetch(mid, '(RFC822)')
        mail = email.message_from_string(data[0][1])
        mbody = self._body2txt(mail)
        return 'Subject:%s\nFrom:%s\nData:%s\n' % (
            mail['subject'],
            mail['from'],
            mbody)

    def getNew(self):
        conn = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        conn.login(self.uid, self.pwd)
        ret,ids=conn.select('Inbox')
        mails=[]
        for mid in ids[0].split():
            mails.append(self._getOne(conn, mid))
        return mails

def getMails():
    gmail = Gmail(config.GMAIL_ID, config.GMAIL_PWD)
    mails = gmail.getNew()
    result=''
    idx=0
    for mail in mails:
        result+='%d:%s' % (idx, mail)
        idx+=1
    return result
if __name__=='__main__':
    print getMails()
   
