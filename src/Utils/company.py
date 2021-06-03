import json

from Utils import abc


def load_company(discrim, conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM companies WHERE discrim = ?", (discrim,))
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
    cur = conn.cursor()
    cur.execute("INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?, ?)", (
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
    if type(val) == bool:
        val = str(val)
    elif type(val) == list or type(val) == dict:
        val = json.dumps(val)

    cur = conn.cursor()
    cur.execute(f"UPDATE companies SET {attr} = ? WHERE discrim = ?", (val, discrim))

    if write:
        conn.commit()