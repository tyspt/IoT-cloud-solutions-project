import threading
import random
from time import sleep
from rx.subject import Subject
from rx import operators as ops

mysubject = Subject()


def callback(r):
    print(r)
    mysubject.on_next(r)
    return r


def incoming():
    for i in range(0, 1000):
        value = random.randint(0, 10)
        delay = random.randint(0, 3)
        sleep(float(delay))
        callback(value)


x = threading.Thread(target=incoming)
x.start()

searcher = mysubject.pipe(
    ops.buffer_with_time(1)
    #ops.map(lambda x: x*2), \
    #ops.filter(lambda i : i > 10)
)


# called every buffer interval
def send_response(x):
    print("send response", x)


def on_error(ex):
    print("E", ex)


searcher.subscribe(send_response, on_error)
