import csv
from datetime import datetime
from threading import Lock
import time

import random


class Logger:

    def __init__(self, fields, id):
        self.sub = None  # rospy topic subscriber
        self.handler = None
        self.id = id
        self.fields = fields
        self.data = []
        self.datalock = Lock()
        print('hello')

    def make_log(self, folder: str):
        date_obj = datetime.now()
        log_name = f'{folder}/{self.id}-{date_obj.date()} {date_obj.hour:02d}-{date_obj.minute:02d}-{date_obj.second:02d}'
        with open(log_name, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['time'] + self.fields)
            writer.writeheader()
            with self.datalock:
                t0 = self.data[0]['time']
                for d in self.data:
                    d['time'] = d['time'] - t0
                writer.writerows(self.data)
                self.data = []

    def set_handler(self, handler, topic, message_type):
        # self.sub = rospy.Subscriber(topic, message_type, handler)
        self.handler = handler


def main():
    log_interval = 5  # seconds

    fieldnames1 = ['a', 'b', 'c']
    fieldnames2 = ['d', 'e', 'f']
    logger1 = Logger(fieldnames1, 'Logger #1')
    logger2 = Logger(fieldnames2, 'Logger #2')

    def handler1(msg):
        # Format the message as a dictionary. Example below
        data = {k: random.randint(0, 100) for k in logger1.fields}
        data['time'] = time.time()
        with logger1.datalock:
            logger1.data.append(data)

    def handler2(msg):
        # Format the message as a dictionary. Example below
        data = {k: random.randint(0, 100) for k in logger2.fields}
        data['time'] = time.time()
        with logger2.datalock:
            logger2.data.append(data)

    logger1.set_handler(handler1, 'fsd', 'asdfa')
    logger2.set_handler(handler2, 'fsd', 'asdfa')

    t0 = time.time()
    while True:  # while not rospy.is_shutdown():
        logger1.handler('some_msg')  # For testing
        logger2.handler('some_msg')  # For testing
        time.sleep(0.01)             # For testing
        if time.time() > t0 + log_interval:
            logger1.make_log('logs')
            logger2.make_log('logs')
            break
    # logger1.make_log('logs')
    # logger2.make_log('logs')


if __name__ == '__main__':
    main()
