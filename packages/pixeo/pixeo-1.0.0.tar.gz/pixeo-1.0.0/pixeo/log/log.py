# logutils.py
import logging
import logging.handlers
import multiprocessing
import os
import sys
import traceback
from datetime import datetime


def worker_configurator(queue):
    root = logging.getLogger()
    h = logging.handlers.QueueHandler(queue)
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def listener_configurator(queue):
    h = logging.handlers.QueueHandler(queue)
    root = logging.getLogger()
    root.addHandler(h)
    root.setLevel(logging.DEBUG)


def listener_process(queue):
    listener_configurator(queue)

    if not os.path.exists('logs/'):
        os.makedirs('logs/')
    # Create a default log_file name with the current date
    log_file = 'logs/' + datetime.now().strftime("%Y-%m-%d") + '.log'
    # Create FileHandler
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Create QueueListener with FileHandler
    listener = logging.handlers.QueueListener(queue, file_handler)
    listener.start()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            logger.handle(record)  # No level or filter logic applied - just do it!
        except Exception:
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


def setup_logger(queue):
    worker_configurator(queue)


def setup_listener(queue):
    listener = multiprocessing.Process(target=listener_process, args=(queue,))
    listener.start()
    return listener


def get_logger(name):
    # Define a Handler and set a format which outputs to sys.stdout
    console = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Tell the handler to use this format
    console.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.addHandler(console)
    return logger
