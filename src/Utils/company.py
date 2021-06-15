"""
Talia Discord Bot
GNU General Public License v3.0
company.py (Utils)

Utilities for the management of companies within the database
"""
import json
from Utils import abc


def load_company(discrim, conn):
    """
    Loads a company from the database

    1. Looks for the company with a certain discriminator
    2. Takes the returned list and assigns each value to it's
     spot in a company object
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE discrim = %s", (discrim,))
    companyinfo = cur.fetchone()

    if companyinfo is None:
        return None

    new_company = abc.Company(companyinfo[0])
    new_company.name = companyinfo[1]
    new_company.ceo = companyinfo[2]
    new_company.members = json.loads(companyinfo[3])
    new_company.invites = json.loads(companyinfo[4])
    new_company.date_created = companyinfo[5]
    new_company.multiplier_boost = companyinfo[6]

    return new_company


def write_company(obj, conn, write=True):
    """
    Creates a new company entry in the database

    1. Creates a new cursor and inserts the company into the database
    2. Commits if the write parameter is true
    """
    cur = conn.cursor()
    cur.execute(f"INSERT INTO companies VALUES (%s, %s, %s, %s, %s, %s, %s)", (
        obj.discrim,
        obj.name,
        obj.ceo,
        json.dumps(obj.members),
        json.dumps(obj.invites),
        obj.date_created,
        obj.multiplier_boost
    ))

    if write:
        conn.commit()


def set_company_attr(discrim, attr, val, conn, write=True):
    """
    Sets a certain attribute of a company in the database

    1. Checks for the value type and converts it to a value
     that sqlite can understand
    2. Creates a new cursor and sets the value
    3. Commits if the write parameter is true
    """
    if type(val) == bool:
        val = str(val)
    elif type(val) == list or type(val) == dict:
        val = json.dumps(val)

    cur = conn.cursor()
    cur.execute(f"UPDATE companies SET {attr} = %s WHERE discrim = %s", (val, discrim))

    if write:
        conn.commit()