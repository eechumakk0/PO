import tkinter as imsit_krd
import pandas as pd
import webbrowser
import sqlite3

# Настройки главной страницы
root = imsit_krd.Tk()
root.title('Главная страница Имсита')  # Добавляем новое название окна
root.configure(background='white')
screen_width = 1000
screen_height = 600
canvas = imsit_krd.Canvas(root, width=screen_width, height=screen_height)
canvas.pack(fill='both', expand=True)
bg_image = imsit_krd.PhotoImage(file="Imsit.png").zoom(2,2) # Увеличиваем фотографию на главном экране
bg_label = imsit_krd.Label(canvas, image=bg_image)
bg_label.place(relwidth=1, relheight=1)
bg_label.lower()








def event1():
    import os
    """Функция для добавления студентов"""
    manage_window = imsit_krd.Toplevel()
    manage_window.title("Добавить студента")

    def add_student_to_db(name, birth_date, phone, education, grade, year, group_name, group_number):
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()

        # Создание таблицы студентов, если она не существует
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS students (name TEXT, birth_date TEXT, phone TEXT, education TEXT, grade TEXT, year_of_admission TEXT, group_name TEXT)')

        # Проверка на существование папки с названием group_name (например, sisa)
        group_folder = os.path.join(os.getcwd(), str(year), group_name)
        if not os.path.exists(group_folder):
            os.makedirs(group_folder)

        # Путь к файлу базы данных
        db_name = f"{group_number}{group_name}_{year}.db"
        db_path = os.path.join(group_folder, db_name)

        # Подключение к базе данных или создание новой
        conn_db = sqlite3.connect(db_path)
        cursor_db = conn_db.cursor()
        cursor_db.execute(
            'CREATE TABLE IF NOT EXISTS student_data (name TEXT, birth_date TEXT, phone TEXT, education TEXT, grade TEXT)')

        # Вставка данных студента в базу данных
        cursor_db.execute(
            'INSERT INTO student_data (name, birth_date, phone, education, grade) VALUES (?, ?, ?, ?, ?)',
            (name, birth_date, phone, education, grade))

        # Сохранение изменений и закрытие соединения
        conn_db.commit()
        conn_db.close()
        conn.commit()
        conn.close()

    name_label = imsit_krd.Label(manage_window, text="ФИО поступающего:")
    name_label.grid(row=0, column=0, padx=10, pady=10)
    name_entry = imsit_krd.Entry(manage_window)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    age_label = imsit_krd.Label(manage_window, text="Дата рождения:")
    age_label.grid(row=1, column=0, padx=10, pady=10)
    age_entry = imsit_krd.Entry(manage_window)
    age_entry.grid(row=1, column=1, padx=10, pady=10)

    grade_label = imsit_krd.Label(manage_window, text="Телефон:")
    grade_label.grid(row=2, column=0, padx=10, pady=10)
    grade_entry = imsit_krd.Entry(manage_window)
    grade_entry.grid(row=2, column=1, padx=10, pady=10)

    student_id_label = imsit_krd.Label(manage_window, text="Текущее образование:")
    student_id_label.grid(row=3, column=0, padx=10, pady=10)
    student_id_entry = imsit_krd.Entry(manage_window)
    student_id_entry.grid(row=3, column=1, padx=10, pady=10)

    grade_att_entry_label = imsit_krd.Label(manage_window, text="Аттестационная оценка:")
    grade_att_entry_label.grid(row=4, column=0, padx=10, pady=10)
    grade_att_entry = imsit_krd.Entry(manage_window)
    grade_att_entry.grid(row=4, column=1, padx=10, pady=10)

    def open_new_window(text):
        new_window = imsit_krd.Toplevel()
        # Панель 1: Год
        year_label = imsit_krd.Label(new_window, text="Год поступления:")
        year_label.grid(row=0, column=0)
        year_entry = imsit_krd.Entry(new_window)
        year_entry.grid(row=0, column=1)

        group_label = imsit_krd.Label(new_window, text="Группа:")
        group_label.grid(row=1, column=0)
        group_entry = imsit_krd.Entry(new_window)
        group_entry.grid(row=1, column=1)

        group_name_label = imsit_krd.Label(new_window, text="Номер группы (1-6):")
        group_name_label.grid(row=2, column=0)
        group_name_entry = imsit_krd.Entry(new_window)
        group_name_entry.grid(row=2, column=1)

        save_btn = imsit_krd.Button(new_window, text="Сохранить", command=lambda: continue_button_handler(year_entry, group_entry, group_name_entry))
        save_btn.grid(row=3, column=0, padx=10, pady=10)

    def continue_button_handler(year_entry, group_entry, group_name_entry):
        from tkinter import messagebox
        name = name_entry.get()
        birth_date = age_entry.get()
        phone = grade_entry.get()
        grade = grade_att_entry.get()
        education = student_id_entry.get()
        year = year_entry.get()
        group_name = group_entry.get()
        group_number = group_name_entry.get()

        # Проверка диапазона данных для Номера группы
        if int(group_number) < 1 or int(group_number) > 6:
            messagebox.showerror("Ошибка", "Номер группы должен быть от 1 до 6")
            root.after(5000, lambda: messagebox.destroy())
            return

        # Проверка диапазона данных для Года поступления и остальные действия
        if int(year) < 2020 or int(year) > 2024:
            messagebox.showerror("Ошибка", "Год поступления должен быть в диапазоне от 2020 до 2024")
            root.after(5000, lambda: messagebox.destroy())
            return

        valid_groups = ['isip', 'sisa', 'pd', 'grd']
        if group_name not in valid_groups:
            messagebox.showerror("Ошибка", "Группа должна быть одной из: isip, sisa, pd, grd")
            root.after(5000, lambda: messagebox.destroy())
            return

        add_student_to_db(name, birth_date, phone, education, grade, year, group_name, group_number)
    add_btn = imsit_krd.Button(manage_window, text="Продолжить",  command=lambda: open_new_window("Студент успешно добавлен в базу данных!"))
    add_btn.grid(row=6, column=0, padx=10, pady=10)


    def cancel_add(text):
        new_window = imsit_krd.Toplevel()
        new_label = imsit_krd.Label(new_window, text=text)
        new_label.pack()
        def close_new_window():
            new_window.destroy()

    cancel_btn = imsit_krd.Button(manage_window, text="Отменить", command=lambda: cancel_add("Пользователь не добавлен в базу данных!"))
    cancel_btn.grid(row=6, column=1, padx=10, pady=10)

# Кнопка Добавление студентов
students_button = imsit_krd.Button(root, text='Добавление студентов', command=lambda: event1(), borderwidth=7, relief=imsit_krd.RIDGE)
students_button.place(x=50, y=50, width=200, height=50)


def event2():
    current_event = 1

    """Функция для Событий Колледжа Имсит"""
    manage_window = imsit_krd.Toplevel()
    manage_window.title("Назначения")

    button_width = 80 # Ширина кнопок
    text_wraplength = 100 # Максимальная длина перед переносом текста

    def func1():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass
    # Добавьте код для события 1

    event1_button = imsit_krd.Button(manage_window, text='Проведение встреч и собраний', command=func1, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event1_button.pack()

    def func2():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 2

    event2_button = imsit_krd.Button(manage_window, text='Выдача распоряжений и указаний', command=func2, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event2_button.pack()

    def func3():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 3

    event3_button = imsit_krd.Button(manage_window, text='Организация мероприятий', command=func3, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event3_button.pack()

    def func4():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 4

    event4_button = imsit_krd.Button(manage_window, text='Предоставление информации', command=func4, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event4_button.pack()

    def func5():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 5

    event5_button = imsit_krd.Button(manage_window, text='Отслеживание дисциплинарной стороны', command=func5, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event5_button.pack()

    def func6():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 6

    event6_button = imsit_krd.Button(manage_window, text='Отслеживание дисциплинарной стороны', command=func5, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event6_button.pack()

    def func7():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 5

    event7_button = imsit_krd.Button(manage_window, text='Отслеживание дисциплинарной стороны', command=func7, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event7_button.pack()

    def func8():
        webbrowser.open('http://eios.imsit.krasnodar')
        pass  # Добавьте код для события 6

    event8_button = imsit_krd.Button(manage_window, text='Обеспечение связи между студентами и преподавателями', command=func8, width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#E6E6FA", fg="black")
    event8_button.pack()

    page1_functions = [func1, func2, func3, func4, func5, func6]
    page2_functions = [func7, func8]
    current_event = 1

    def go_to_previous_event():
        global current_event
        if current_event > 1:
            current_event -= 1
            manage_window.destroy()
            if current_event == 1:
                event2(page1_functions)
            elif current_event == 2:
                event2(page2_functions)

    def go_to_next_event():
        global current_event
        if current_event < 2:
            current_event += 1
            manage_window.destroy()
            if current_event == 1:
                event2(page1_functions)
            elif current_event == 2:
                event2(page2_functions)

    previous_button = imsit_krd.Button(manage_window, text='Предыдущая', command=go_to_previous_event,
                                       width=button_width, wraplength=text_wraplength, padx=5, pady=15, bg="#D3D3D3",
                                       fg="black" if current_event > 1 else "#C0C0C0")
    previous_button.pack()
    previous_button.pack(side='left', anchor='s')

    next_button = imsit_krd.Button(manage_window, text='Следующая', command=go_to_next_event, width=button_width,
                                   wraplength=text_wraplength, padx=5, pady=15, bg="#D3D3D3",
                                   fg="black" if current_event < 2 else "#C0C0C0")
    next_button.pack()
    next_button.pack(side='right', anchor='s')

# Функции для каждого события
students_button = imsit_krd.Button(root, text='Назначения', command=lambda: event2(), borderwidth=7, relief=imsit_krd.RIDGE)
students_button.place(x=50, y=120, width=200, height=50)


def event3():
    from tkinter.ttk import Treeview
    root = imsit_krd.Tk()
    root.title("Главное окно")

    def show_data_window(year):
        data_window = imsit_krd.Toplevel(root)
        data_window.title(f"Данные из базы {year}")
        conn = sqlite3.connect(f'{year}_schedule.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Schedule")
        rows = cursor.fetchall()
        headers = ["ID", "Группа", "Название предмета", "Дата", "Время", "Аудитория"]
        tree = Treeview(data_window, columns=headers, show="headings")
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.pack()

    def create_db_for_year(year):
        conn = sqlite3.connect(f'{year}_schedule.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Schedule (
                            id INTEGER PRIMARY KEY,
                            title TEXT,
                            group_name TEXT,
                            date TEXT,
                            time TEXT,
                            room TEXT
                            )''')

    def show_data_window(year):

        data_window = imsit_krd.Toplevel(root)
        data_window.title(f"Данные из базы {year}")

        conn = sqlite3.connect(f'{year}_schedule.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Schedule")
        rows = cursor.fetchall()

        headers = ["ID", "Группа", "Название предмета", "Дата", "Время", "Аудитория"]
        tree = Treeview(data_window, columns=headers, show="headings")

        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor="center")

        for row in rows:
            tree.insert("", "end", values=row)


        tree.pack()

        button_export = imsit_krd.Button(data_window, text="Export Data", command=None, borderwidth=7, relief="ridge")
        button_export.pack(side="left", padx=10)

        button_import = imsit_krd.Button(data_window, text="Import Data", command=None, borderwidth=7, relief="ridge")
        button_import.pack(side="left", padx=10)

        root.update()
        root.after(0, lambda: data_window.focus_force())

        tree.bind("<Button-1>", increase_table_size)
        tree.bind("<Button-3>", decrease_table_size)


    # Добавление данных в базу данных
    def insert_data(year, title, group_name, date, time, room):
        conn = sqlite3.connect(f'{year}_schedule.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO Schedule (title, group_name, date, time, room) 
                          VALUES (?, ?, ?, ?, ?)''', (title, group_name, date, time, room))
        conn.commit()
        conn.close()

    # Функция для обработки нажатия на кнопку и добавления записи
    def add_data_and_show_window(year, title, group_name, date, time, room):
        insert_data(year, title, group_name, date, time, room)
        show_data_window(year)

    years = [2020, 2021, 2022, 2023, 2024]

    for year in years:
        create_db_for_year(year)

    def add_data_window(year):
        add_data_window = imsit_krd.Toplevel(root)
        add_data_window.title(f"Добавить данные для {year}")

        title_entry = imsit_krd.Entry(add_data_window)
        title_entry.grid(row=0, column=1)
        title_label = imsit_krd.Label(add_data_window, text='Группа')
        title_label.grid(row=0, column=0)

        group_entry = imsit_krd.Entry(add_data_window)
        group_entry.grid(row=1, column=1)
        group_label = imsit_krd.Label(add_data_window, text='Название предмета')
        group_label.grid(row=1, column=0)

        date_entry = imsit_krd.Entry(add_data_window)
        date_entry.grid(row=2, column=1)
        date_label = imsit_krd.Label(add_data_window, text='Дата')
        date_label.grid(row=2, column=0)

        time_entry = imsit_krd.Entry(add_data_window)
        time_entry.grid(row=3, column=1)
        time_label = imsit_krd.Label(add_data_window, text='Время')
        time_label.grid(row=3, column=0)

        room_entry = imsit_krd.Entry(add_data_window)
        room_entry.grid(row=4, column=1)
        room_label = imsit_krd.Label(add_data_window, text='Аудитория')
        room_label.grid(row=4, column=0)

        button_bottom = imsit_krd.Button(add_data_window, text="Добавить", command=lambda: add_data_and_show_window(year, title_entry.get(), group_entry.get(), date_entry.get(), time_entry.get(), room_entry.get()))
        button_bottom.grid(row=5, column=0, columnspan=2)

    button20 = imsit_krd.Button(root, text="20", command=lambda year=year: add_data_window('2020'), borderwidth=7, relief=imsit_krd.RIDGE)
    button20.place(x=100, y=120, width=50, height=50)

    button21 = imsit_krd.Button(root, text="21", command=lambda year=year: add_data_window('2021'), borderwidth=7, relief=imsit_krd.RIDGE)
    button21.place(x=200, y=120, width=50, height=50)

    button22 = imsit_krd.Button(root, text="22", command=lambda year=year: add_data_window('2022'), borderwidth=7, relief=imsit_krd.RIDGE)
    button22.place(x=300, y=120, width=50, height=50)

    button23 = imsit_krd.Button(root, text="23", command=lambda year=year: add_data_window('2023'), borderwidth=7, relief=imsit_krd.RIDGE)
    button23.place(x=400, y=120, width=50, height=50)

    button24 = imsit_krd.Button(root, text="24", command=lambda year=year: add_data_window('2024'), borderwidth=7, relief=imsit_krd.RIDGE)
    button24.place(x=500, y=120, width=50, height=50)

groups_button = imsit_krd.Button(root, text="Расписание", command=lambda: event3(), borderwidth=7, relief=imsit_krd.RIDGE)
groups_button.place(x=50, y=190, width=200, height=50)


def event4():
    from tkinter import ttk
    journal_page = imsit_krd.Toplevel(root)

    # Функция для отображения данных по указанному году
    # Функция для отображения данных по указанному году
    def display_schedule(year):
        db_name = f'{year}_schedule.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('SELECT * FROM schedule')
        rows = cur.fetchall()
        for row in rows:
            table.insert('', 'end', values=row)
        pass

    def year20(db_name):
        # Подключение к базе данных
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Выборка данных из базы
        cur.execute('SELECT group_name FROM schedule')
        rows = cur.fetchall()

        # Возвращение данных из столбца group_name
        return rows

    def year21(db_name):
        # Подключение к базе данных
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Выборка данных из базы
        cur.execute('SELECT * FROM schedule')
        rows = cur.fetchall()

        # Добавление данных в таблицу
        for row in rows:
            table.insert('', 'end', values=row)

            # Пример вызова функции при нажатии на кнопку
            db_name = '2021_schedule.db'  # Имя нужной базы данных
            year21(db_name)
        pass

    def year22(db_name):
        # Подключение к базе данных
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Выборка данных из базы
        cur.execute('SELECT * FROM schedule')
        rows = cur.fetchall()

    def year23(db_name):
        # Подключение к базе данных
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Выборка данных из базы
        cur.execute('SELECT * FROM schedule')
        rows = cur.fetchall()

        # Добавление данных в таблицу
        for row in rows:
            table.insert('', 'end', values=row)

            # Пример вызова функции при нажатии на кнопку
            db_name = '2023_schedule.db'  # Имя нужной базы данных
            year23(db_name)
        pass

    def year24(db_name):
        # Подключение к базе данных
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        # Выборка данных из базы
        cur.execute('SELECT * FROM schedule')
        rows = cur.fetchall()

        # Добавление данных в таблицу
        for row in rows:
            table.insert('', 'end', values=row)

            # Пример вызова функции при нажатии на кнопку
            db_name = '2024_schedule.db'  # Имя нужной базы данных
            year24(db_name)
        pass

    functions_dict = {
        'year1': year20('2020_schedule.db'),
        'year2': year21('2021_schedule.db'),
        'year3': year22('2022_schedule.db'),
        'year4': year23('2023_schedule.db'),
        'year5': year24('2024_schedule.db')
    }

    # Создание списка кнопок для каждого года
    button_year_list = []
    for i in range(5):
        button = imsit_krd.Button(journal_page, text=f"Год {2020 + i}", command=functions_dict[f'year{i + 1}'])
        button_year_list.append(button)

    # Функция для переключения списка кнопок
    def toggle_list(button_to_hide, button_list_to_show):
        for button in button_list_to_show:
            button.pack()
        button_to_hide.pack_forget()

    # Создание кнопки "Год"
    button_year = imsit_krd.Button(journal_page, text="Год", command=lambda: toggle_list(button_year, button_year_list))
    button_year.place(x=30, y=20)

    global group1, group2, group3, group4, group5

    def toggle_list(button, button_list):
        if button.cget("relief") == "sunken":
            button.config(relief="raised")
            for btn in button_list:
                btn.place_forget()
        else:
            button.config(relief="sunken")
            for i, btn in enumerate(button_list):
                btn.place(x=50, y=i * 30 + 50)
        pass

    global function1, function2, function3, function4, function5

    def function1(data):
        print('Function 1:', data)

    def function2(data):
        print('Function 2:', data)

    def function3(data):
        print('Function 3:', data)

    def function4(data):
        print('Function 4:', data)

    def function5(data):
        print('Function 5:', data)

    db_name = '2020_schedule.db'
    data = year20(db_name)

    function1(data)
    function2(data)
    function3(data)
    function4(data)
    function5(data)

    button_group_list = []
    for i in range(5):
        button = imsit_krd.Button(journal_page, text=f"Function {i + 1}", command=globals()[f'function{i + 1}'])
        button_group_list.append(button)

    button_group = imsit_krd.Button(journal_page, text="Группа",
                                    command=lambda: toggle_list(button_group, button_group_list))
    button_group.place(x=130, y=20)

    entry_search = imsit_krd.Entry(journal_page)
    entry_search.place(x=250, y=23)

    def search():
        search_text = entry_search.get()
        result_label.config(text="Найдено" if search_text and any(
            btn.cget("relief") == "sunken" for btn in button_group_list) else "Неудача")

    button_search = imsit_krd.Button(journal_page, text="Искать", command=search)
    button_search.place(x=390, y=20)

    result_label = imsit_krd.Label(journal_page, text="")
    result_label.place(x=450, y=20)

    # Создание таблицы
    table = ttk.Treeview(journal_page, columns=("ID", "Имя", "Дата рождения", "Предмет", "Аттестация", "Зачет"),
                         show="headings")
    table.heading("ID", text="ID")
    table.heading("Имя", text="Имя")
    table.heading("Дата рождения", text="Дата рождения")
    table.heading("Предмет", text="Предмет")
    table.heading("Аттестация", text="Аттестация")
    table.heading("Зачет", text="Зачет")
    table.place(x=55, y=210)

    # Добавление данных в таблицу
    data = [
        (1, "Чумак Е.Г.", "17.09.2006", "Обеспечение качества функционирования компьютерных систем", "4", "Да")
    ]

    for row in data:
        table.insert("", "end", values=row)


grades_button = imsit_krd.Button(root, text="Журнал", command=event4, borderwidth=7, relief=imsit_krd.RIDGE)
grades_button.place(x=50, y=260, width=200, height=50)


def clear_database():

    import os
    try:
        os.remove("students.db")
        os.remove("2020_schedule.db")
        os.remove("2021_schedule.db")
        os.remove("2022_schedule.db")
        os.remove("2023_schedule.db")
        os.remove("2024_schedule.db")
    except FileNotFoundError as e:
        print("File not found:", e)

# код для создания кнопки в tkinter
clear_button = imsit_krd.Button(root, text='Очистить данные', command=clear_database, borderwidth=7)
clear_button.place(x=50, y=330, width=200, height=50)


# здесь можно добавить код для работы со студентами, например, редактирование информации о студенте pass
def event6():
    def edit_page():
        global edit_window
        edit_window = imsit_krd.Toplevel()
        edit_window.title("Редактирование")

        # Создание элементов для изменения стилей страницы
        color_label = imsit_krd.Label(edit_window, text="Выберите цвет (RGB):")
        color_label.pack()
        r_entry = imsit_krd.Entry(edit_window, width=5)
        r_entry.pack()
        g_entry = imsit_krd.Entry(edit_window, width=5)
        g_entry.pack()
        b_entry = imsit_krd.Entry(edit_window, width=5)
        b_entry.pack()

        bold_label = imsit_krd.Label(edit_window, text="Выберите жирность текста:")
        bold_label.pack()
        bold_entry = imsit_krd.Entry(edit_window, width=5)
        bold_entry.pack()

        # Кнопка для применения изменений
        apply_button = imsit_krd.Button(edit_window, text="Применить",
                                        command=lambda: apply_changes(r_entry.get(), g_entry.get(), b_entry.get(),
                                                                    bold_entry.get()))
        apply_button.pack()

    def apply_changes(r, g, b, bold):
        bg_label.configure(bg=f"#{r}{g}{b}")
        bg_label.configure(font=("Arial", int(bold)))


    edit_page()
students_button = imsit_krd.Button(root, text='Редактирование', command=lambda: event6(), borderwidth=7, relief=imsit_krd.RIDGE)
students_button.place(x=50, y=400, width=200, height=50)
root.mainloop()
