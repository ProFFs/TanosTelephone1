import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def open_search_dialog(self):
        Search()

    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute(
            '''SELECT * FROM db WHERE name LIKE ?''', name
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    #удаление записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE id=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def update_record(self, name, tel, email, plata):
        self.db.c.execute("""UPDATE db SET name=?, tel=?, email=?, plata=?
        WHERE ID=?""",(name, tel, email, plata, self.tree.set(
            self.tree.selection()[0], '#1')
        ))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def records(self, name, tel, email, plata):
        self.db.insert_date(name, tel, email, plata)
        self.view_records()

    def init_main(self):
        #Создаем панель инструментов
        toolbar = tk.Frame(bg='#d7d8eD', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='img/add.png')
        btn_open_dialog = tk.Button(toolbar, text="добавить позицию", command=self.open_dialog, bg='#d7d8e0',
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'plata'), height=45, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("plata", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')
        self.tree.heading("plata", text='Заработная плата')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, text="Редактировать позицию", command=self.open_update_dialog, bg='#d7d8e0',
                                    compound=tk.TOP, image=self.update_img )
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления данных
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, text="Удалить", bg='#d7d8e0', compound=tk.TOP, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, text="Поиск", bg='#d7d8e0', compound=tk.TOP, image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

    def open_dialog(self):
        Child(self.db)

    def view_records(self):
        self.db.c.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

class Child(tk.Toplevel):
    def __init__(self, db):
        super().__init__(root)
        self.init_child()
        self.view = app
        self.db = db

    def init_child(self):
        #Заголовок окна
        self.title('Добавить')
        self.geometry('400x400')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)        
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_plata = tk.Label(self, text='Заработная плата')
        label_plata.place(x=50, y=140)

        # добавляем строку ввода для наименования
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        # добавляем строку ввода для e-mail
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        # добавляем строку ввода для телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        # добавляем строку ввода для заработной платы
        self.entry_plata = ttk.Entry(self)
        self.entry_plata.place(x=200, y=140)

        # кнопка для закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        # кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)

        # срабатывание по ЛКМ
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_plata.get()))

class Update(Child):
    def __init__(self):
        super().__init__(db)
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                        self.entry_email.get(),
                                                                        self.entry_tel.get(),
                                                                        self.entry_plata.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',
                          (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_plata.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('380x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=105, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB():
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS DB (
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT,
        plata TEXT
        );
        """)
        self.conn.commit()

    def insert_date(self, name, tel, email, plata):
        self.c.execute("""INSERT INTO db (name, tel, email, plata)
        VALUES (?,?,?,?)
        """, (name, tel, email, plata))
        self.conn.commit()

if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    # Заголовок окна
    root.title('Телефонная книга')
    # Размер окна
    root.geometry('1000x450')
    # Ограничение изменения размеров окна
    root.resizable(False, False)
    root.mainloop()
