"""
Talia Discord Bot
GNU General Public License v3.0
timer.py (Utils)

Utilities for managing the main timer, edu timer and investment timer
"""
import math
from Utils import abc


def load_timer(name, conn):
    """
    Loads a timer from the main timer table

    1. Creates a new cursor and selects everything from the timer
    2. Returns a new timer object from the information it got
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM timers WHERE name = %s", (name,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.Timer(timerinfo[0], timerinfo[1], timerinfo[2], timerinfo[3])


def new_timer(timer, conn, write=True):
    """
    Creates a new timer in the main timer table

    1. Creates a new cursor and inserts a new entry into the
     main timer table
    2. Commits if the write parameter is true
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO timers VALUES (%s, %s, %s, %s)", (
        timer.name, timer.time, timer.user, timer.meta
    ))

    if write:
        conn.commit()


def load_edu_timer(user_id, conn):
    """
    Loads a timer from the edu timer table

    1. Creates a new cursor and selects everything from the timer
    2. Returns a new edu timer object from the information it got
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM edu_timers WHERE id = %s", (user_id,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.EduTimer(timerinfo[0], timerinfo[1], timerinfo[2])


def new_edu_timer(timer, conn, write=True):
    """
    Creates a new timer in the edu timer table

    1. Creates a new cursor and inserts a new entry into the
     edu timer table
    2. Commits if the write parameter is true
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO edu_timers VALUES (%s, %s, %s)", (
        timer.id, timer.time, timer.level
    ))

    if write:
        conn.commit()


def load_invest_timer(user_id, conn):
    """
    Load a timer from the invest timer table

    1. Creates a new cursor and selects everything from the timer
    2. Returns a new invest timer object from the information it got
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM invest_timers WHERE id = %s", (user_id,))
    timerinfo = cur.fetchone()

    if timerinfo is None:
        return None

    return abc.InvestTimer(
        timerinfo[0], timerinfo[1],
        timerinfo[2], timerinfo[3],
        timerinfo[4], timerinfo[5]
    )


def new_invest_timer(timer, conn, write=True):
    """
    Creates a new timer in the edu timer table

    1. Creates a new cursor and inserts a new entry into the
     invest timer table
    2. Commits if the write parameter is true
    """
    cur = conn.cursor()
    cur.execute("INSERT INTO invest_timers VALUES (%s, %s, %s, %s, %s, %s)", (
        timer.id,
        timer.time,
        timer.coins,
        timer.multiplier,
        timer.failed,
        timer.loss
    ))

    if write:
        conn.commit()


def load_time(time):
    """
    Converts time in seconds into a readable string (Ex. 2h30m40s)

    1. Creates a new string to add everything int
    2. Checks for days, then hours, then minutes
    3. Any remaining seconds are added on
    4. Returns the new string
    """
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