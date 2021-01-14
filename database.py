import sqlite3


def records():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT name, record FROM player_record ORDER BY record DESC""").fetchall()
    s = [list(i) for i in result]
    con.close()
    return s


def names():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute("""SELECT name FROM player_record""").fetchall()
    s = [i[0] for i in result]
    con.close()
    return s


def clear_all():
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    cur.execute("""UPDATE player_record SET record = 0""")
    con.commit()
    con.close()


def my_record(name):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    result = cur.execute(f"""SELECT record FROM player_record WHERE name = '{name}'""").fetchone()
    con.close()
    return result[0]


def my_clear(name):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    cur.execute(f"""UPDATE player_record 
                    SET record = 0 
                    WHERE name = '{name}'""")
    con.commit()
    con.close()


def set_record(name, record):
    con = sqlite3.connect("players.db")
    cur = con.cursor()
    if record > my_record(name):
        cur.execute(f"""UPDATE player_record 
                            SET record = {record} 
                            WHERE name = '{name}'""")
    con.commit()
    con.close()
