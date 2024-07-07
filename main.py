import tkinter as tk
from tkinter import filedialog as fd
from requests import get
from bs4 import BeautifulSoup as BS
from pandas import DataFrame as DF
from pathlib import Path

address = "http://weather.uwyo.edu/cgi-bin/sounding? \
         region=europe&TYPE=TEXT%3ALIST&YEAR={p[YEAR]}&MONTH={p[MONTH]}&FROM={p[FROM]}&TO={p[TO]}&STNM={p[STNM]}"



def parameters_are_correct(path, name, parametrs):
    if not Path(path).exists():
        return "Не существует такого каталога"
    try:
        parametrs["FROM"] = parametrs["FROM"].replace("/", "")
    except:
        return "Неверно введено время 'от дня/время'"
    try:
        parametrs["TO"] = parametrs["TO"].replace("/", "")
    except:
        return "Неверно введено время 'до дня/время'"
    if str(BS(get(address.format(p=parametrs)).text, 'lxml')).find("Description") == 101:
        return "Нет данных на сайте"
    else: return True


def saved_data(path, name, soup):
    data = []
    for stat_table in soup.find_all("pre")[::2]:
        half_day_data = []
        for data_string in str(stat_table)[319:-7].split("\n")[1:]:
            line_data = data_string.split()
            if len(line_data) == 11:
                half_day_data.append(line_data)
        data += half_day_data
    if name == ".xlsx":
        name = str(soup.h2)[10:-5].replace(" ", "_").replace(".", "_") + ".xlsx"
    else:
        if name.endswith(".xlsx"):
            pass
        else:
            name += ".xlsx"
    try:
        DF(data).to_excel(path + "/" + name,
                     header=["PRES", "HGHT", "TEMP", "DWPT", "RELH", "MIXR", "DRCT", "SKNT", "THTA", "THTE", "THTV"],
                     index=False)
    except:
        return "Введена неверная дата"


def run(path, name, parametrs, label):
    check = parameters_are_correct(path, name, parametrs)
    if check == True:
        full_text = get(address.format(p=parametrs)).text
        result = saved_data(path, name, BS(full_text, 'lxml'))
        if result is not None:
            label.config(text=result)
        else:
            label.config(text="Сохранено")
    else:
        label.config(text=check)
















window = tk.Tk()
window.title("Скачать данные с сайта с погодой")
window.geometry("720x300")

FONT = "Helvetica 12"

# ROW 0
label_title = tk.Label(window, text="Скачать метеоданные с сайта weather.uwyo.edu",
                       font="TimesNewRoman 18", padx=30, pady=30)
label_title.grid(row=0, column=0, columnspan=5)

# ROW 1
frame_path = tk.Frame(window, width=700, height=50, padx=53)
entry_path_input = tk.Entry(frame_path, width=30)
entry_path_input.place(relx=0, rely=0.1)
button_find_folder = tk.Button(frame_path, height=1, width=14, text="Обзор",
                               command=lambda: entry_path_input.insert(0, fd.askdirectory()))
button_find_folder.place(relx=0.4, rely=0)
label_path_print = tk.Label(frame_path, text="Полный путь до папки загрузки", font=FONT).place(relx=0.6, rely=0)
frame_path.grid(row=1, column=0, columnspan=5)

# ROW 2
frame_file_name = tk.Frame(window, width=700, height=50, padx=53)
entry_file_name_input = tk.Entry(frame_file_name, width=30)
entry_file_name_input.insert(0, ".xlsx")
entry_file_name_input.place(relx=0, rely=0.1)
label_file_name_print = tk.Label(frame_file_name, text="Название файла (необязательно)", font=FONT)
label_file_name_print.place(relx=0.5, rely=0)
frame_file_name.grid(row=2, column=0, columnspan=5)

# ROW 3
# Column 0
frame_metadate_year = tk.Frame(window, width=70, height=100, padx=30)
entry_metadate_input_year = tk.Entry(frame_metadate_year, width=10)
entry_metadate_input_year.insert(0, 2021)
entry_metadate_input_year.pack()
label_metadate_print_year = tk.Label(frame_metadate_year, text="Год", font=FONT).pack()
frame_metadate_year.grid(row=3, column=0)
# Column 1
frame_metadate_month = tk.Frame(window, width=70, height=100)
entry_metadate_input_month = tk.Entry(frame_metadate_month, width=10)
entry_metadate_input_month.insert(0, "5")
entry_metadate_input_month.pack()
label_metadate_print_month = tk.Label(frame_metadate_month, text="Месяц", font=FONT).pack()
frame_metadate_month.grid(row=3, column=1)
# Column 2
frame_metadate_from = tk.Frame(window, width=70, height=100)
entry_metadate_input_from = tk.Entry(frame_metadate_from, width=10)
entry_metadate_input_from.insert(0, "3/00")
entry_metadate_input_from.pack()
label_metadate_print_from = tk.Label(frame_metadate_from, text="От дня / время", font=FONT).pack()
frame_metadate_from.grid(row=3, column=2)
# Column 3
frame_metadate_to = tk.Frame(window, width=70, height=100)
entry_metadate_input_to = tk.Entry(frame_metadate_to, width=10)
entry_metadate_input_to.insert(0, "15/12")
entry_metadate_input_to.pack()
label_metadate_print_to = tk.Label(frame_metadate_to, text="До дня / время", font=FONT).pack()
frame_metadate_to.grid(row=3, column=3)
# Column 4
frame_metadate_station_number = tk.Frame(window, width=50, height=100)
entry_metadate_input_station_number = tk.Entry(frame_metadate_station_number, width=10)
entry_metadate_input_station_number.insert(0, "26075")
entry_metadate_input_station_number.pack()
label_metadate_print_station_number = tk.Label(frame_metadate_station_number, text="Номер станции", font=FONT).pack()
frame_metadate_station_number.grid(row=3, column=4)

# ROW 4
# Column 0
button_submit = tk.Button(window, text="Скачать данные", pady=10, font=FONT,
                          command=lambda: run(entry_path_input.get(),
                                              entry_file_name_input.get(),
                                              {"YEAR": entry_metadate_input_year.get(),
                                               "MONTH": entry_metadate_input_month.get(),
                                               "FROM": entry_metadate_input_from.get(),
                                               "TO": entry_metadate_input_to.get(),
                                               "STNM": entry_metadate_input_station_number.get()
                                               }, label_result
                                              )
                          )
button_submit.grid(row=4, column=0, columnspan=3)
# Column 1
label_result = tk.Label(window, text="", font=FONT)
label_result.grid(row=4, column=3, columnspan=2)

window.mainloop()
