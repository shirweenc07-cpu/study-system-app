import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,status TEXT,due_date DATE)')


def add_data(task,status,due_date):
	c.execute('INSERT INTO taskstable(task,status,due_date) VALUES (?,?,?)',(task,status,due_date))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data

def view_unique_task():
    c.execute('SELECT DISTINCT task FROM taskstable')
    data = c.fetchall()
    return data

def get_task(task):
    c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
    data = c.fetchall()
    return data

def edit_task(new_task,new_status,new_due_date,task,status,due_date):
    c.execute("UPDATE taskstable SET task=?,status=?, due_date=? WHERE task=? and status=? and due_date=?",(new_task,new_status,new_due_date,task,status,due_date))
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(task):
    c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
    conn.commit()