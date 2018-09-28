#!/usr/bin/python3
# coding=utf-8
from socket import *
import sys
import getpass


def main():
    if len(sys.argv) < 3:
        print("argv is error")
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    sk = socket()
    try:
        sk.connect((HOST, PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            ==========Welcome=========
            -- 1.注册  2.登录  3.退出
            ==========================
            ''')
        try:
            cmd = int(input("输入选项>> "))
        except Exception as e:
            print("命令错误")
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项")
            sys.stdin.flush()  # 清楚标准输入
            continue
        elif cmd == 1:
            r = do_register(sk)
            if r == 0:
                print("注册成功")
            elif r == 1:
                print("用户名存在")
            else:
                print("注册失败")
        elif cmd == 2:
            name = do_login(sk)
            if name:
                print("登录成功")
                login(sk, name)
            else:
                print("用户名或密码不正确")
        else:
            sys.exit("退出成功，感谢使用")


def do_register(sk):
    while True:
        name = input("Username: ")
        passwd = getpass.getpass()
        passwd1 = getpass.getpass("Again:")

        if (" " in name) or (" " in passwd):
            print("用户名和密码不允许有空格")
            continue
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        msg = "R {} {}".format(name, passwd)
        sk.send(msg.encode())
        data = sk.recv(1024).decode()
        if data == "OK":
            return 0
        elif data == "EXISTS":
            return 1
        else:
            return 2


def do_login(sk):
    while True:
        name = input("Username:")
        passwd = getpass.getpass()
        msg = "L {} {}".format(name, passwd)
        sk.send(msg.encode())
        data = sk.recv(1024).decode()
        if data == "OK":
            return name
        else:
            return


def login(sk, name):
    while True:
        print('''
            ===========查询界面===========
             1.查单词   2.查询记录   3.注销
            =============================
           ''')
        try:
            cmd = int(input("输入选项>> "))
        except Exception as e:
            print("命令错误")
            continue
        if cmd not in [1, 2, 3]:
            print("请输入正确选项")
            sys.stdin.flush()  # 清楚标准输入
            continue
        elif cmd == 1:
            do_query(sk, name)
        elif cmd == 2:
            do_hist(sk, name)
        elif cmd == 3:
            return


def do_query(sk, name):
    while True:
        word = input("world: ")
        if not word:
            return
        msg = "Q {} {}".format(word, name)
        sk.send(msg.encode())
        data = sk.recv(2048).decode()
        print("means : ", data)


def do_hist(sk, name):
    msg = "H " + name
    sk.send(msg.encode())
    while True:
        data = sk.recv(1024).decode()
        if data == "##":
            break
        print(data)


if __name__ == "__main__":
    main()
