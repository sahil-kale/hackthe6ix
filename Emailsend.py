import smtplib, ssl
# Might be blocked by Gmail security if you log in, need an app password, https://support.google.com/accounts/answer/185833

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "sender.gmail.com"  # Enter your address
receiver_email = "receiver@gmail.com"  # Enter receiver address
password = input("Enter Password")
message = """\
Subject: Mask Warning Alert

An employee without a mask entered your building.

"""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)