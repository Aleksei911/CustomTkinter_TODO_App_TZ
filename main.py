import customtkinter
import sqlite3
from tkinter import *
from tkinter import messagebox

app = customtkinter.CTk()
app.title('Todo App')
app.geometry('750x550')
app.config(bg='#a3a3a3')

frame = customtkinter.CTkScrollableFrame(app, width=550, height=350)
frame.pack(padx=100, pady=140)

font1 = ('Arial', 30, 'bold')
font2 = ('Arial', 18, 'bold')
font3 = ('Arial', 10, 'bold')

db = sqlite3.connect('Todo.db')
cursor = db.cursor()
db.execute('CREATE TABLE IF NOT EXISTS TODO (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')

ids = 0


def add_task():
    task = task_entry.get()
    if task:
        cursor.execute('INSERT INTO TODO (name) VALUES (?)', (task,))
        db.commit()
        task_entry.delete(0, END)
        load_tasks()
    else:
        messagebox.showerror('Error', 'Не обнаружено задания для внесения в список')


def delete_task():
    task_to_delete = tasks_list.curselection()
    id_value = cursor.execute('SELECT id FROM TODO WHERE name=?', (tasks_list.get(task_to_delete[0]),))
    if task_to_delete:
        cursor.execute('DELETE FROM TODO WHERE id=?', (id_value.fetchone()[0],))
        db.commit()
        load_tasks()
    else:
        messagebox.showerror('Error', 'Не выбрано ни одного задания для удаления')


def load_tasks():
    task_entry.delete(0, END)
    tasks_list.delete(0, END)
    cursor.execute('SELECT * FROM TODO')
    rows = cursor.fetchall()
    for row in rows:
        tasks_list.insert(0, row[1])


def get_data(event):
    global ids
    task_entry.delete(0, END)
    task_entry.insert(0, tasks_list.get(tasks_list.curselection()))
    cur_id = cursor.execute('SELECT id FROM TODO WHERE name=?', (task_entry.get(),))
    ids = cur_id.fetchone()[0]


def update():
    task_to_update = task_entry.get()
    cursor.execute('UPDATE TODO SET name=? WHERE id=?', (task_to_update, ids))
    db.commit()
    load_tasks()


title_label = customtkinter.CTkLabel(app, font=font1, text='Daily Tasks', text_color='#000', bg_color='#a3a3a3')
title_label.place(x=290, y=40)

task_entry = customtkinter.CTkEntry(frame, font=font2, text_color='#000', fg_color='#fff', border_color='#fff',
                                    width=550,
                                    placeholder_text='Add todo')
task_entry.pack(fill=X)

tasks_list = Listbox(frame, width=78, height=15, font=font3)
tasks_list.bind('<ButtonRelease-1>', get_data)
tasks_list.pack()

add_button = customtkinter.CTkButton(app, command=add_task, font=font2, text_color='#fff', text='Add',
                                     fg_color='#5277ff', hover_color='#5277ff', bg_color='#a3a3a3', cursor='hand2',
                                     corner_radius=5, width=550)
add_button.place(x=100, y=420)

update_button = customtkinter.CTkButton(app, command=update, font=font2, text_color='#fff', text='Update',
                                        fg_color='green', hover_color='green', bg_color='#a3a3a3', cursor='hand2',
                                        corner_radius=5, width=550)
update_button.place(x=100, y=460)

delete_button = customtkinter.CTkButton(app, command=delete_task, font=font2, text_color='#fff', text='Delete',
                                        fg_color='#96061c', hover_color='#96061c', bg_color='#a3a3a3', cursor='hand2',
                                        corner_radius=5, width=550)
delete_button.place(x=100, y=500)

load_tasks()

app.mainloop()
