import pika
import time
# import logging
from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class EventHandler(FileSystemEventHandler):
    # вызывается на событие создания файла или директории
    def on_created(self, event):
        print(event.event_type, event.src_path)
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
    path = r"/home/user/PycharmProjects/test_av/files"  # отслеживаемая директория с нужным файлом
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
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