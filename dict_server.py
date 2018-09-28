'''
name : Kiolin
date : 2018.09.28
email: *****
this is a dict project by python
'''
from socket import *
import os
import time
import signal
import pymysql
import sys


# 定义需要的全局变量
DICT_PATH = "./dict/dict.txt"
ADDR = ("0.0.0.0", 8000)

# 控制流程


def main():
    # 创建数据库链接
    db = pymysql.connect("localhost", "root", "123456", "dict_project")
    # 创建套接字
    sk = socket()
    sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sk.bind(ADDR)
    sk.listen(5)

    # 忽略子进程信号
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = sk.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sk.close()
            sys.exit("服务器退出")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        pid = os.fork()
        if pid == 0:
            sk.close()
            do_child(c, db)
        else:
            c.close()
            continue


def do_child(c, db):
    # 循环接受客户端请求
    while True:
        data = c.recv(1024).decode()
        print(c.getpeername, ":", data)
        if (not data) or data[0] == "E":
            c.close()
            sys.exit("客户端退出")
        elif data[0] == "R":
            do_register(c, db, data)
        elif data[0] == "L":
            do_login(c, db, data)
        elif data[0] == "Q":
            do_query(c, db, data)
        elif data[0] == "H":
            do_hist(c, db, data)


def do_register(c, db, data):
    # 注册操作
    L = data.split(" ")
    name = L[1]
    passwd = L[2]
    cur = db.cursor()
    sql = "select * from userinfo where name='%s';" % name
    cur.execute(sql)
    r = cur.fetchall()
    if r:
        c.send(b"EXISTS")
        cur.close()
        return

    sql2 = "insert into userinfo (name,passwd) values\
        ('%s','%s');" % (name, passwd)
    try:
        cur.execute(sql2)
        db.commit()
        c.send(b"OK")
    except:
        db.rollback()
        cur.close()
        c.send(b"FALL")
    else:
        cur.close()
        print("%s注册成功" % name)


def do_login(c, db, data):
    L = data.split(" ")
    name = L[1]
    passwd = L[2]
    cur = db.cursor()
    sql = "select passwd from userinfo where name='%s'" % name
    cur.execute(sql)
    r = cur.fetchall()
    if not r:
        c.send("用户名不存在，登录失败".encode())
        cur.close()
        return
    if passwd == r[0][0]:
        c.send(b"OK")
        cur.close()
    else:
        c.send("密码错误,登录失败".encode())
        cur.close()


def do_query(c, db, data):
    L = data.split(" ")
    word = L[1]
    name = L[2]
    cur = db.cursor()
    sql = "select means from word_dict where words='%s'" % word
    cur.execute(sql)
    r = cur.fetchone()
    if r:
        c.send(r[0].encode())
        sql2 = "insert into records (name,word) values('%s','%s')" % (
            name, word)
        cur.execute(sql2)
        db.commit()
    else:
        c.send("词典没有此单词,sorry~".encode())


def do_hist(c, db, data):
    L = data.split(" ")
    name = L[1]
    print(name)
    cur = db.cursor()
    sql = "select name,word,time from records where name='%s'" % name
    cur.execute(sql)
    r = cur.fetchall()
    if not r:
        c.send("历史记录为空".encode())
    else:
        for i in r:
            msg = "%s %s %s" % i
            c.send(msg.encode())
            time.sleep(0.1)
        c.send(b"##")


if __name__ == "__main__":
    main()
