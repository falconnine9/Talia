import math

from Utils import abc


def load_timer(name, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM timers WHERE name = ?", (name,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.Timer(timerinfo[0], timerinfo[1], timerinfo[2], timerinfo[3])


def new_timer(timer, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO timers VALUES (?, ?, ?, ?)", (
        timer.name, timer.time, timer.user, timer.meta
    ))

    if write:
        conn.commit()


def load_edu_timer(user_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM edu_timers WHERE id = ?", (user_id,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.EduTimer(timerinfo[0], timerinfo[1], timerinfo[2])


def new_edu_timer(timer, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO edu_timers VALUES (?, ?, ?)", (
        timer.id, timer.time, timer.level
    ))

    if write:
        conn.commit()


def load_invest_timer(user_id, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM invest_timers WHERE id = ?", (user_id,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.InvestTimer(timerinfo[0], timerinfo[1], timerinfo[2], timerinfo[3])


def new_invest_timer(timer, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO invest_timers VALUES (?, ?, ?, ?)", (
        timer.id, timer.time, timer.coins, timer.multiplier
    ))

    if write:
        conn.commit()


def load_time(time):
    send_str = ""

    if time >= 86400:
        days = math.floor(time / 86400)
        send_str += f"{days}d"
        time -= days * 86400

    if time >= 3600:
        hours = math.floor(time / 3600)
        send_str += f"{hours}h"
        time -= hours * 3600

    if time >= 60:
        minutes = math.floor(time / 60)
        send_str += f"{minutes}m"
        time -= minutes * 60

    if time != 0:
        send_str += f"{time}s"

    return send_str