import sqlite3

con = ''
cur = ''

def connect(host):
    global con
    global cur
    try:
        con = sqlite3.connect(host)
        cur = con.cursor()
        return True
    except:
        print('数据库连接失败！')
        return False


def query(sql):
    global cur
    return cur.execute(sql)


def update(table, cname, cvalue, name, value, commit=True):
    global con
    sql = 'update ' + table + ' set ' + name + "='" + value + "' where " + cname + "='" + cvalue + "'"
    try:
        query(sql)
        if commit==True:
            con.commit()
        return True
    except:
        return False


# 添加一行，value为一个字典表
def insert(table, value, commit=True):
    global con
    sql = 'insert into '+table+'('
    i = 0
    for n in value.keys():
        i = i+1
        if i is not len(value):
            sql = sql+n+','
        else:
            sql = sql+n+')values('
    i = 0
    for n in value.values():
        i = i + 1
        if i is not len(value):
            sql = sql + "'" + n + "'" + ','
        else:
            sql = sql + "'" + n + "'" + ')'
    try:
        query(sql)
        if commit == True:
            con.commit()
        return True
    except:
        return False


def select(table, name, vname, vvalue):
    global cur
    sql='select '+name+' from '+table+' where '+vname+"='"+vvalue+"'"
    try:
        query(sql)
    except:
        return None
    try:
        re=cur.fetchall()
        return str(re[0][0])
    except:
        return None


def delete(table, vname, vvalue, commit=True):
    global con
    sql='DELETE FROM '+table+' WHERE '+vname+"='"+vvalue+"'"
    try:
        query(sql)
        if commit == True:
            con.commit()
        return True
    except:
        return False


def close():
    global con
    global cur
    cur.close()
    con.commit()
    con.close()
