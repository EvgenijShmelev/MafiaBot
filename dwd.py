import threading

def f(f_stop):
    print ('hello world')
    if not f_stop.is_set():
        # вызывем функцию f каждые 60 секунд
        t = threading.Timer(5, f, [f_stop]).start()

f_stop = threading.Event()

f(f_stop)

f_stop.set()
