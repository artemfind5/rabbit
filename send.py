import pika
import time
# import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import os
from pika import exceptions

class EventHandler(FileSystemEventHandler):
    # вызывается на событие создания файла или директории
    def on_created(self, event):
        print(event.event_type, event.src_path)
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
            'localhost'))
            channel = connection.channel()
            filename = event.src_path.split(".")
            if filename[len(filename)-1] == "txt" or filename[len(filename)-1] == "text":
                channel.queue_declare(queue='Parsing')
                channel.basic_publish(exchange='',
                                  routing_key='Parsing',
                                  body=event.src_path)
            else:
                channel.queue_declare(queue='Errors')
                channel.basic_publish(exchange='',
                                      routing_key='Errors',
                                      body=event.src_path)
            print(" [x] Sent ", event.src_path)
            connection.close()
        except pika.exceptions.AMQPConnectionError:
            print("Need to start rabbitmq (pika.exceptions.AMQPConnectionError)")
            return

    # вызывается на событие модификации файла или директории
    def on_modified(self, event):
        print(event.event_type, event.src_path)

    # вызывается на событие удаления файла или директории
    def on_deleted(self, event):
        print(event.event_type, event.src_path)

    # вызывается на событие перемещения\переименования файла или директории
    def on_moved(self, event):
        print(event.event_type, event.src_path, event.dest_path)

def main():
    # logging.basicConfig(level=logging.INFO,
    #                    format='%(asctime)s - %(message)s',
    #                    datefmt='%Y-%m-%d %H:%M:%S')
    print("Start of the \"Sender\" module.")
    #directory = r"/home/user/PycharmProjects/test_av/files"  # отслеживаемая директория с нужным файлом
    directory = os.environ.get('DIRECTORY', os.path.join('/tmp')) # load variables from environment variables
    print(directory)
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(event_handler, observer)
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()