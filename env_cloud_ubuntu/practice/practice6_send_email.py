import smtplib

gmail_user = 'jiaweitang828@gmail.com'
gmail_password = 'mWGSQwu9YzCJ9sv'
email_text = 'Hallo'

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail("Dr. Who", "jiawei.bremen@gmail.com", email_text)
    server.close()

    print ('Email sent!')
except:
    print ('Error')
