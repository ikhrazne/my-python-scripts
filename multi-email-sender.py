import argparse
import datetime
import smtplib as smtp


def send_email(rec_email):
    msg = f'From: {email} \nTo: {rec_email}\nSubject: {subject}\n\n{msg}'
    print(msg)

    class_to_send = smtp.SMTP('smtp.gmail.com', 587)
    class_to_send.set_debuglevel(1)
    class_to_send.starttls()
    class_to_send.login(email, password)
    class_to_send.sendmail(email, rec_email, msg)

    file.write(f"{datetime.datetime.now().strftime('YYYY-MM-DD %HH:%MM:%ss')} {rec_email} {subject} {msg}")
    print('mail sent')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="multi-email sender")

    parser.add_argument("-r", "--receivers", dest="receivers", help="Give the receivers", default="", type=str)
    parser.add_argument("-s", "--subject", dest="subject", help="give the subject", default="", type=str)
    parser.add_argument("-m", "--message", dest="message", help="give message", default="", type=str)

    args = parser.parse_args()

    receivers = args.receivers
    subject = args.subject
    msg = args.message

    file = open('logs.txt', 'a', encoding='utf8')

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if "," in receivers:
        receivers = receivers.split(',')

    if type(receivers) == list:
        for receiver in receivers:
            send_email(rec_email=receiver)
    else:
        send_email(receivers)

    file.close()
