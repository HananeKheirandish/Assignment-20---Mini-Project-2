import sqlite3

con = sqlite3.connect('To Do.db')
my_cursor = con.cursor()

def add(id, title, description, time, date):
    my_cursor.execute(f'INSERT INTO tasks(id, title, description, done, time, date, priority) VALUES({id} , "{title}", "{description}", 0 , "{time}", "{date}", 0)')
    con.commit()

def getAll():
    my_cursor.execute('SELECT * FROM tasks')
    results = my_cursor.fetchall()
    return results

def update(do, title):
    my_cursor.execute(f'UPDATE tasks SET done = {do} WHERE title = "{title}" ')
    con.commit()

def delete(title):
    my_cursor.execute(f'DELETE FROM tasks WHERE title = "{title}"')
    con.commit()

def update_priority(prio, title):
    my_cursor.execute(f'UPDATE tasks SET priority = {prio} WHERE title = "{title}" ')
    con.commit()