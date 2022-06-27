import sqlite3
conn = sqlite3.connect('datos.db',check_same_thread=False)
c = conn.cursor()


def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS TablaTareas(nombre TEXT,estado TEXT,fecha DATE)')


def add_data(parNombre,parEstado,parFecha):
	c.execute('INSERT INTO TablaTareas(nombre,estado,fecha) VALUES (?,?,?)',(parNombre,parEstado,parFecha))
	conn.commit()


def view_all_data():
	c.execute('SELECT * FROM TablaTareas')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT nombre FROM TablaTareas')
	data = c.fetchall()
	return data

def get_task(parNombre):
	c.execute('SELECT * FROM TablaTareas WHERE nombre="{}"'.format(parNombre))
	data = c.fetchall()
	return data

def get_task_by_status(parEstado):
	c.execute('SELECT * FROM TablaTareas WHERE estado="{}"'.format(parEstado))
	data = c.fetchall()


def edit_task_data(parNuevoNombre,parNuevoEstado,parNuevaFecha,parNombre,parEstado,parFecha):
	c.execute("UPDATE TablaTareas SET nombre =?,estado=?,fecha=? WHERE nombre=? and estado=? and fecha=? ",(parNuevoNombre,parNuevoEstado,parNuevaFecha,parNombre,parEstado,parFecha))
	conn.commit()
	data = c.fetchall()
	return data

def delete_data(parNombre):
	c.execute('DELETE FROM TablaTareas WHERE nombre="{}"'.format(parNombre))
	conn.commit()