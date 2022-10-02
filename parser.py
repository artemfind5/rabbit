import pika
import re
from mysql.connector import connect, Error

def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))
    body = body.decode("utf-8")
    print(body)
    body_words = re.sub(r'[^a-zA-Z0-9а-яА-Я]', ' ', body.replace('\r\n',''))
    print(body_words)
    words_list = body_words.split(' ')
    words = dict()
    print(words_list)
    for w in words_list:
        occurrence = body_words.count(w)
        if w not in words and w != "" and w != " ":
            words[w] = occurrence
    print(words)
    try:
        with connect(
                host="localhost",
                user="root",
                password="12345678",
                database="av_db",
        ) as connection:
            print(connection)
            #create_table_query = "CREATE TABLE words (word VARCHAR(100), count INT, PRIMARY KEY (word))"
            #insert_query = """INSERT INTO words(word, count) VALUES ("test", 19)"""
            #select_query = "SELECT * FROM words"
            for w in words:
                update_query = """INSERT INTO words (word, count) VALUES ('{0}', {1}) ON DUPLICATE KEY UPDATE word=VALUES(word), count=count+{1}
                """.format(w, words[w])
                print(update_query)
                with connection.cursor() as cursor:
                    cursor.execute(update_query)
                    result = cursor.fetchall()
                    for row in result:
                        print(row)
                    connection.commit()
    except Error as e:
        print(e)

def main():
    callback(1,1,1,"/gdfhdfh/gzzяяяfdg/22/test/22/1.trt".encode())
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='Parsing')
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume('Parsing', callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    main()