import sqlite3
from datetime import datetime

today = datetime.today()
conn = sqlite3.connect("db/vaccidate.db")
c = conn.cursor()


def delete_record(record):
    sql = "DELETE FROM USERS WHERE username=?"
    c.execute(sql, (record,))
    conn.commit()


def create_record(record):
    sql = """ INSERT INTO USERS(username,first_name,last_name,chat_id,district,age_group,timestamp)
              VALUES(?,?,?,?,?,?,?) """
    c.execute(sql, record)
    conn.commit()


def update_dist_record(record):
    sql = """ UPDATE USERS
              SET district=?
              WHERE username=?"""
    c.execute(sql, record)
    conn.commit()


def update_age_group(record):
    sql = """ UPDATE USERS
              SET age_group=?
              WHERE username=?"""
    c.execute(sql, record)
    conn.commit()


def store_data(district_id, user_data):
    print(user_data)
    first_name = user_data.message.from_user.first_name
    last_name = user_data.message.from_user.last_name
    username = user_data.message.from_user.username
    chat_id = user_data.message.from_user.id
    if username is None:
        username = f"{first_name}_{chat_id}"
    c.execute("SELECT * FROM USERS WHERE username=?", (username,))
    rows = c.fetchall()
    if len(rows) > 0:
        row = rows[0]
        print(type(row))
        username, f_name, l_name, chat_id, district, age_g, time = row
        print(district)
        print(len(district))
        if len(district) == 0:
            print("new")
            update_dist_record((district_id, username))
        else:
            dist_list = [district for district in district.split(",")]
            print(dist_list)
            if district_id not in dist_list:
                dist_list.append(district_id)
                dist_data = ",".join(dist_list)
                print(dist_data)
                update_dist_record((dist_data, username))
    else:
        create_record(
            (username, first_name, last_name, chat_id, district_id, "", today)
        )


def store_age_group(age_group, user_data):
    print(user_data)
    first_name = user_data.message.from_user.first_name
    chat_id = user_data.message.from_user.id
    age_group = age_group.split("+")[0]
    username = user_data.message.from_user.username
    if username is None:
        username = f"{first_name}_{chat_id}"
    c.execute("SELECT * FROM USERS WHERE username=?", (username,))
    rows = c.fetchall()
    if len(rows) > 0:
        row = rows[0]
        username, f_name, l_name, chat_id, district, age_g, time = row
        print(age_g)
        print(len(age_g))
        if len(age_g) == 0:
            update_age_group((age_group, username))
        else:
            age_list = [age for age in age_g.split(",")]
            # print(age_list)
            print(age_group)
            if age_group not in age_list:
                age_list.append(age_group)
                print(age_list)
                age_data = ",".join(age_list)
                print(age_data)
                update_age_group((age_data, username))


def remove_record(user_data):
    print(user_data)
    username = user_data.message.from_user.username
    if username is None:
        first_name = user_data.message.from_user.first_name
        chat_id = user_data.message.from_user.id
        username = f"{first_name}_{chat_id}"
    delete_record(username)