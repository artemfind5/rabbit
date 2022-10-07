# rabbit (directory monitor +)
RabbitMQ (pika), Watchdog, MySQL, Telebot, smtplib, traceback, sys, threading, re, time, logging

### Компоненты:
1. Отправитель - send.py
2. Обработчик «Parser» - parser.py
3. Обработчик «Error Handler» - errors.py
4. Чтец - reader.py

### Перед запуском программ:
```
sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.10-management
```
## Обёртывание в docker-контейнер реализовано на примере компонента "Отправитель"
### Сборка образа 
```
sudo docker build -t sender .
```
### Запуск образа 
```
sudo docker run -d --restart=always -e DIRECTORY='/tmp/test' -v /tmp/:/tmp/ sender
```
> где --e DIRECTORY= — передача при помощи переменных окружения каталога, который нужно отслеживать
