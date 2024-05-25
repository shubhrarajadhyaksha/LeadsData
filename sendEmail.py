import smtplib

from leads_package.constants import SERVER_LOGIN_EMAIL, SERVER_LOGIN_PASSWORD




def send_email(receiver_email, subject, message):
    print("sending email", receiver_email)
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        # Start TLS encryption
        server.starttls()
        server.ehlo()

        # Log in to the Gmail SMTP server
        server.login(SERVER_LOGIN_EMAIL, SERVER_LOGIN_PASSWORD)

        msg = 'Subject: {0}\nCc:{1}\n\n{2}'.format(subject, SERVER_LOGIN_EMAIL, message)
        recipients = [receiver_email]
        server.sendmail(receiver_email, recipients, msg)
        print("Sent")
        return

        #Check error on sendMail return.
