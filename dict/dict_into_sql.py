import re
import pymysql
'''
功能：将单词字典插入到mysql数据库中
'''

db = pymysql.connect(host='localhost', user='root',
                     password='123456', charset='utf8')
cur = db.cursor()
cur.execute("use dict_project")


def insert(a, b):
    sql_insert = "insert into word_dict(words,means) values \
                  (%s,%s);"
    cur.execute(sql_insert, [a, b])
    db.commit()


f = open("dict.txt")
try:
    for line in f:
        # 正则表达式获取单词为是s1
        s1 = re.findall(r"^\S+", line)[0].strip()
        # 正则表达式获取解释s2，当没有解释时设置为nothing
        L = re.findall(r"\s+.+", line)
        if L:
            s2 = L[0].strip()
        else:
            s2 = "nothing"
        # 插入数据库
        insert(s1, s2)
except Exception as e:
    db.rollback()
    print("Failed", e)

f.close()
cur.close()
db.close()
