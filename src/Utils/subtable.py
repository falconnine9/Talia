"""
Talia Discord Bot
GNU General Public License v3.0
subtable.py (Utils)

Utilities for managing info in sub tables
"""
import json


def new_job(user_id, job, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO job_info VALUES (%s, %s, %s, %s, %s, %s)", (
        user_id, job.name, job.xp, job.level,
        json.dumps(job.salary), json.dumps(job.cooldown)
    ))

    if write:
        conn.commit()


def remove_job(user_id, conn, write=True):
    cur = conn.cursor()
    cur.execute("DELETE FROM job_info WHERE id = %s", (user_id,))

    if write:
        conn.commit()


def set_job_attr(user_id, attr, val, conn, write=True):
    if type(val) == list or type(val) == dict:
        val = json.dumps(val)

    cur = conn.cursor()
    cur.execute(f"UPDATE job_info SET {attr} = %s WHERE id = %s", (val, user_id))

    if write:
        conn.commit()


def new_pickaxe(user_id, pickaxe, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO pickaxe_info VALUES (%s, %s, %s, %s, %s)", (
        user_id, pickaxe.name, pickaxe.worth, pickaxe.speed, pickaxe.multiplier
    ))

    if write:
        conn.commit()


def remove_pickaxe(user_id, conn, write=True):
    cur = conn.cursor()
    cur.execute("DELETE FROM pickaxe_info WHERE id = %s", (user_id,))

    if write:
        conn.commit()


def new_showcase(user_id, item, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO showcase_info VALUES (%s, %s, %s, %s, %s)", (
        user_id, item.name, item.worth, item.type,
        json.dumps(item.stats)
    ))

    if write:
        conn.commit()


def remove_showcase(user_id, conn, write=True):
    cur = conn.cursor()
    cur.execute("DELETE FROM showcase_info WHERE id = %s", (user_id,))

    if write:
        conn.commit()


def new_pet(user_id, pet, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO pet_info VALUES (%s, %s, %s, %s, %s)", (
        user_id, pet.name, pet.worth, pet.type, pet.breed
    ))

    if write:
        conn.commit()


def remove_pet(user_id, conn, write=True):
    cur = conn.cursor()
    cur.execute("DELETE FROM pet_info WHERE id = %s", (user_id,))

    if write:
        conn.commit()


def set_pet_attr(user_id, attr, val, conn, write=True):
    if type(val) == list or type(val) == dict:
        val = json.dumps(val)

    cur = conn.cursor()
    cur.execute(f"UPDATE pet_info SET {attr} = %s WHERE id = %s", (val, user_id))

    if write:
        conn.commit()


def new_item(user_id, item, conn, write=True):
    cur = conn.cursor()
    cur.execute("INSERT INTO items (owner, name, worth, type, stats) VALUES (%s, %s, %s, %s, %s)", (
        user_id, item.name, item.worth,
        item.type, json.dumps(item.stats)
    ))

    if write:
        conn.commit()


def remove_item(item_id, conn, write=True):
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE id = %s", (item_id,))

    if write:
        conn.commit()