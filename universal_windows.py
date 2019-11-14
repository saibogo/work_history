import datetime
import tkinter as tk
from tkinter import messagebox as mb

import config
import functions
from scroll_frame import VerticalScrolledFrame

left_mouse_but = '<Button-1>'
functions.info_string(__name__)


def print_table_window(name_table: str, header_ls: list, data: list) -> None:
    """Function create window-table"""

    table = tk.Toplevel()
    table.title(name_table)
    lines = [header_ls] + [elem for elem in data]
    max_sizes = [0 for _ in lines[0]]
    for line in lines:
        for j in range(len(line)):
            max_sizes[j] = min(max(max_sizes[j], len(line[j])), config.max_size_column)

    heights = [1 for _ in lines]
    for i in range(len(lines)):
        heights[i] = max([len(elem) for elem in lines[i]]) // max(max_sizes) + 1

    mainframe = VerticalScrolledFrame(table, height=sum(heights) * config.rows_pxls)
    frames = [tk.Frame(mainframe.interior) for _ in lines]
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            elem = lines[i][j]
            tmp = tk.Label(frames[i], text=functions.str_to_str_n(str(elem), max_sizes[j]),
                           width=max_sizes[j], bd=1, relief=config.relief, height=heights[i] + 1)
            tmp.pack(side=tk.LEFT)
        frames[i].pack()
    mainframe.pack()


def input_window(name_win: str, header_ls: list) -> list:
    """Function create input window and return list new data"""

    result = []
    table = tk.Toplevel()
    table.title(name_win)
    max_size = max([len(elem) for elem in header_ls])
    frames = [tk.Frame(table) for _ in header_ls]
    entrys = []

    for i in range(len(header_ls)):
        tmp_lab = tk.Label(frames[i], text=header_ls[i], width=max_size)
        tmp_entr = tk.Entry(frames[i])
        entrys.append(tmp_entr)
        tmp_lab.pack(side=tk.LEFT)
        tmp_entr.pack(side=tk.LEFT)
        frames[i].pack()

    def close_win(self) -> None:
        """Function to button cancel"""

        table.quit()
        table.destroy()

    def return_new_data(self) -> None:
        """Function to good button"""

        table.result = [elem.get() for elem in entrys]
        table.quit()
        table.destroy()

    frames.append(tk.Frame(table))
    but_good = tk.Button(frames[-1], text='Готово')
    but_cancel = tk.Button(frames[-1], text='Закрыть')

    but_good.bind(left_mouse_but, func=return_new_data)
    but_cancel.bind(left_mouse_but, func=close_win)

    but_good.pack(side=tk.LEFT)
    but_cancel.pack(side=tk.LEFT)
    frames[-1].pack()

    table.result = result
    table.mainloop()
    return table.result


def select_window(name_select: str, data: list) -> str:
    """Function create window to select in list-data and return number selected element"""

    sw = tk.Toplevel()
    sw.title(name_select)
    sw.win_result = '0'
    max_size = max([len(elem) for elem in data])

    def interrupted(self) -> None:
        """Function to button Interrupted"""

        sw.win_result = config.str_interrupted
        sw.quit()
        sw.destroy()

    def return_selected(self) -> None:
        """Function return selected element or 0 if not selected any"""

        select = box.curselection()[0] if len(box.curselection()) > 0 else -1
        sw.win_result = box.get(select) if select >= 0 else "0"
        sw.quit()
        sw.destroy()

    frame_box = tk.Frame(sw)
    box = tk.Listbox(frame_box, width=max_size)
    for elem in data:
        box.insert(tk.END, str(elem))
    box.pack()
    frame_box.pack()

    frame_but = tk.Frame(sw)
    but_select = tk.Button(frame_but, text='Выбрать')
    but_interrupt = tk.Button(frame_but, text='Прервать')

    but_select.bind(left_mouse_but, func=return_selected)
    but_interrupt.bind(left_mouse_but, func=interrupted)

    but_select.pack(side=tk.LEFT)
    but_interrupt.pack(side=tk.LEFT)
    frame_but.pack()

    sw.mainloop()
    return sw.win_result


def select_date_and_time() -> str:
    """Function create simple window to select date and time"""

    date = datetime.datetime.now()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minut = date. minute

    dw = tk.Toplevel()
    dw.title('Выберите дату и время')
    mainframe = tk.Frame(dw)
    frame_neaders = tk.Frame(mainframe)
    labels = [tk.Label(frame_neaders, text=item, width=config.max_width_for_date, bd=1, relief=config.relief)
              for item in ['Год', 'Месяц', 'День', 'Час', 'Минут']]
    for label in labels:
        label.pack(side=tk.LEFT)

    frame_input = tk.Frame(mainframe)

    year_frame = tk.Frame(frame_input, width=config.max_width_for_date, bd=1, relief=config.relief)
    y_var = tk.StringVar()
    y_var.set(str(year))
    year_buttons = [tk.Radiobutton(year_frame, text=str(i),variable=y_var ,value=str(i))
                    for i in range(year - 2, year + 3)]
    for but in year_buttons:
        but.pack()

    month_frame = tk.Frame(frame_input, width=config.max_width_for_date, bd=1, relief=config.relief)
    m_var = tk.StringVar()
    m_var.set(functions.num_to_time_str(month))
    month_buttons = [tk.Radiobutton(month_frame, text=functions.num_to_time_str(i), variable=m_var,
                                    value=functions.num_to_time_str(i)) for i in range(1, 13)]
    for but in month_buttons:
        but.pack()

    day_frame = tk.Frame(frame_input, width=config.max_width_for_date, bd=1, relief=config.relief)
    d_var = tk.StringVar()
    d_var.set(functions.num_to_time_str(day))
    days_buttons = [tk.Radiobutton(day_frame, text=functions.num_to_time_str(i), variable=d_var,
                                   value=functions.num_to_time_str(i)) for i in range(1, 32)]
    for but in days_buttons:
        but.pack()

    hourse_frame = tk.Frame(frame_input, width=config.max_width_for_date, bd=1, relief=config.relief)
    h_var = tk.StringVar()
    h_var.set(functions.num_to_time_str(hour))
    hours_buttons = [tk.Radiobutton(hourse_frame, text=functions.num_to_time_str(i), variable=h_var,
                                   value=functions.num_to_time_str(i)) for i in range(24)]
    for but in hours_buttons:
        but.pack()

    minut_frame = tk.Frame(frame_input, width=config.max_width_for_date, bd=1, relief=config.relief)
    min_var = tk.StringVar()
    min_var.set(functions.num_to_time_str(minut))
    minut_buttons = [tk.Radiobutton(minut_frame, text=functions.num_to_time_str(i), variable=min_var,
                                    value=functions.num_to_time_str(i)) for i in range(0, 60, 5)]
    for but in minut_buttons:
        but.pack()

    def done(self)-> None:
        """Function to button Done"""

        try:
            datetime.date(int(y_var.get()), int(m_var.get()) ,int(d_var.get()))
            dw.quit()
            dw.destroy()
        except:
            mb.showerror('Ошибка','Дата некорректна!')

    button_frame = tk.Frame(mainframe)
    button_done = tk.Button(button_frame, text='Выбрать')
    button_done.bind(left_mouse_but, func=done)
    button_done.pack()

    year_frame.pack(side=tk.LEFT)
    month_frame.pack(side=tk.LEFT)
    day_frame.pack(side=tk.LEFT)
    hourse_frame.pack(side=tk.LEFT)
    minut_frame.pack(side=tk.LEFT)
    frame_neaders.pack()
    frame_input.pack()
    button_frame.pack()
    mainframe.pack()

    dw.mainloop()
    return y_var.get() + "-" + m_var.get() + "-" + d_var.get() + " " + h_var.get() + ":" + min_var.get() + ":00"

