import sqlite3
con = sqlite3.connect("/home/silaederregolimpiadas/mysite/database.db", check_same_thread=False)
cur = con.cursor()
def add_new_user(name,klass):
    global cur,con
    tmp = cur.execute('SELECT max(id) FROM users')
    max_id=tmp.fetchone()[0]
    cur.execute("""INSERT INTO users
                              (id, FIO,class, score)
                              VALUES (?, ?,?, ?);""",[max_id+1,name,klass,0])
    con.commit()
def get_user(name):
    tmp=cur.execute(f"SELECT FIO,score FROM users WHERE FIO=='{name}'")
    return tmp.fetchone()
def get_user_class(name):
    return cur.execute(f"SELECT class FROM users WHERE FIO=='{name}'").fetchone()[0]
def get_all_users():
    tmp=cur.execute(f"SELECT FIO,score FROM users WHERE ID!=0 ORDER BY score")
    return tmp.fetchall()
def update_score(name,score):
    cur.execute(f"UPDATE users SET score={score} WHERE FIO = '{name}'")
    con.commit()
