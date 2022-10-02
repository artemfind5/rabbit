import pika
import smtplib
import traceback
import sys
import telebot
import threading

def send_mail(body):
    smtpObj = smtplib.SMTP('smtp.mail.ru', 25) # gmail - 587, ya - 465 (no tls), mail - 465 \ 25
    if smtpObj.starttls():
        try:
            smtpObj.login('sender@mail.ru', 'password')
            smtpObj.sendmail("sender@mail.ru", "recipient@mail.ru", "Error: " + body)
        except smtplib.SMTPServerDisconnected:
            return "smtplib.SMTPServerDisconnected"
        except smtplib.SMTPSenderRefused:
            return "smtplib.SMTPSenderRefused"
        except smtplib.SMTPDataError:
            return "smtplib.SMTPDataError"
        except smtplib.SMTPConnectError:
            return "smtplib.SMTPConnectError"
        except smtplib.SMTPHeloError:
            return "smtplib.SMTPHeloError"
        except smtplib.SMTPAuthenticationError:
            return "smtplib.SMTPAuthenticationError"
        except smtplib.SMTPResponseException:
            return "smtplib.SMTPResponseException"
        except smtplib.SMTPRecipientsRefused:
            return "smtplib.SMTPRecipientsRefused"
        except Exception:
            return "Exception, " + str(traceback.format_exc()) + str(sys.exc_info()[0])
    else:
        return "No transport layer security"
    smtpObj.quit()
    return True

def send_tg(body):
    TOKEN = '000000:AAAAAAAAAAAAAAAAAAA'
    bot = telebot.TeleBot(TOKEN)
    bot.config['api_key'] = TOKEN
    chat = '000000000'  # Chat ID, куда отправлять уведомление в телеграм
    send = bot.send_message(chat, "Error: " + body)
    return str(send).split("{'ok': ")[1].split(",")[0] # True/False

def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    body_str = body.decode("utf-8")
    #output = send_mail(body)
    output = send_tg(body_str)
    if output != True:
        threading.Timer(60.0*60, callback, args=[ch, method, properties, body]).start() # error handler (в случае ошибки оповещения - повтор через час)
    print(output)


def errors():
    #callback(1,1,1,"/gdfhdfh/gzzяяяfdg/22/test/22/1.trt".encode())
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Errors')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume('Errors', callback, auto_ack=True)
    channel.start_consuming()

def main():
    errors()

if __name__ == "__main__":
    main()