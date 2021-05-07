import sqlite3

conn = sqlite3.connect("vaccidate.db")
c = conn.cursor()
print(c)
# Create table - USERS
c.execute(
    """CREATE TABLE USERS
             ([username] text PRIMARY KEY,[first_name] text, [last_name] text,[chat_id] integer, [district] text,[age_group] text, [timestamp] date)"""
)

conn.commit()