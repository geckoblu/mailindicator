TESTCONFIG="""<?xml version='1.0' encoding='ASCII'?>
<mailindicator version="1.0">
  <!--Configuration file for mailindicator-->
  <global>
    <proxy use_proxy="True">
      <http_proxy>http://127.0.0.1:3128</http_proxy>
      <https_proxy>https://127.0.0.1:3128</https_proxy>
    </proxy>
  </global>
  <mailboxes>
    <mailbox typ="GMAILFEED" label="GMAIL" sleep_time="300" username="testusername" userpassword="testusserpassword" enabled="True"/>
    <mailbox typ="LOCALMBOX" label="System" sleep_time="60" mboxpath="/var/spool/mail/testuser" enabled="False"/>
    <mailbox typ="IMAPSTARTTLS" label="Work" sleep_time="65" username="testusername" userpassword="testuserpassword" host="testhost.org"/>
  </mailboxes>
</mailindicator>
"""

MBOX="""From testuser@testhost  Fri Dec  7 08:45:01 2012
Return-Path: <testuser@testhost>
X-Original-To: testuser
Delivered-To: testuser@testhost
Received: by testhost (Postfix, from userid 1000)
    id 992D440418; Fri,  7 Dec 2012 08:45:01 +0100 (CET)
From: testuser@testhost (Test User)
To: testuser@testhost
Subject: This is a test subject
Content-Type: text/plain; charset=ANSI_X3.4-1968
Message-Id: <20121207074501.992D440418@testhost>
Date: Fri,  7 Dec 2012 08:45:01 +0100 (CET)

This is a test body

"""