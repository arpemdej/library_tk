import psycopg2
import tkinter as tk
from tkinter import font
from tkinter import ttk
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='k.,k.pizza',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()
root = tk.Tk()
def get():
    global cursor
    cursor.execute('SELECT book_id, book_name, book_author, section_name FROM books JOIN sections ON book_section=section_id')
    books=cursor.fetchall()
    return books
def show():
    for i in table.get_children():
        table.delete(i)
    books=get()
    for i in books:
        table.insert('', 'end', values=i)

def selection_window(values):
    modal_window = tk.Toplevel(root)
    modal_window.title('Выберите действие')
    modal_window.transient(root)
    id=values[0]
    label=tk.Label(modal_window, text=f'Выбрано строчку{values}')
    label.pack(pady=10, padx=10)
    update_button = tk.Button(modal_window, text='Изменить', command=lambda :update_book(values))
    update_button.pack(pady=10)
    delete_button = tk.Button(modal_window, text='Удалить', command=lambda:delete_book(id))
    delete_button.pack(pady=10)

def update_book(values):
    modal_window = tk.Toplevel(root)
    modal_window.title('Изменение данных')
    modal_window.transient(root)
    name_label=tk.Label(modal_window, text='Введите новое название')
    name_label.pack(pady=10, padx=10)
    name_entry = ttk.Entry(modal_window)
    name_entry.pack(padx=10, pady=10)
    author_label=tk.Label(modal_window, text='Введите нового автора')
    author_label.pack(pady=10, padx=10)
    author_entry = ttk.Entry(modal_window)
    author_entry.pack(padx=10, pady=10)
    section_label=tk.Label(modal_window, text='Введите новую секцию')
    section_label.pack(pady=10, padx=10)
    section_entry = ttk.Entry(modal_window)
    section_entry.pack(padx=10, pady=10)
    def confirm():
        name = name_entry.get()
        if not name:
            name = values[1]
        author = author_entry.get()
        if not author:
            author = values[2]
        section = section_entry.get()
        if not section:
            section = values[3]
        update(values[0], name, author, get_section(section))
    success = tk.Button(modal_window, text='Подтвердить действия', command=confirm)
    success.pack(pady=20)
def get_section(section):
    cursor.execute(f"SELECT section_id FROM sections WHERE section_name='{section}'")
    section = cursor.fetchone()[0]
    print(section)
    return section
def update(id, name, author, section):
    try:
        cursor.execute(f"UPDATE books SET book_name='{name}', book_author='{author}', book_section={section} WHERE book_id={id}")
        conn.commit()
        print('Успешно изменено')
    except Exception as i:
        print(i)
        conn.rollback()
def exception_window():
    exception_window = tk.Toplevel(root)
    exception_window.title('Ошибка')
    exception_window.transient(root)
def delete_book(id):
    try:
        cursor.execute(f'DELETE FROM books WHERE book_id={id}')
        conn.commit()
    except Exception as i:
        print(i)
        exception_window()
        conn.rollback()
def on_select(event):
    item_number=table.selection()[0]
    values=table.item(item_number, 'values')
    selection_window(values)


table=ttk.Treeview(root, columns=('id', 'name', 'author', 'section'))
table.heading('id', text='id')
table.heading('name', text='Название')
table.heading('author', text='Автор')
table.heading('section', text='Секция')
button=ttk.Button(root, text='Показать книги', command=show)
table.bind('<<TreeviewSelect>>', on_select)
table.pack(pady=10, padx=20)
button.pack(pady=10)
root.mainloop()

# Отправляю тебе сообщение через комментарий в самом низу кода
