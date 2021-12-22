from tkinter import *
from tkinter.ttk import Combobox
from drawPCI import DrawPCI

count_words = 6


def clicked():
    print(combo1.current())
    print(combo2.current())
    print(combo3.current())
    print(combo4.current())
    print(num_input.get())
    print("Общее количество тактов: ")
    print(tact() + is_read() + address())
    DrawPCI(window, count_words, address(), data_length(), type_operation=type_operation(), is_read=is_read(),
            count_bites=count_bites(), is_64=is_64())


def data_length() -> list:
    a = []
    if combo4.current() == 0:
        a = [1]
    if combo4.current() == 1:
        a = [3]
    if combo4.current() == 2:
        a = [4]
    if combo4.current() == 3:
        a = [7]
    if combo4.current() == 4:
        a = [3, 1, 1, 1]
    if combo4.current() == 5:
        a = [2, 1, 1, 1]
    if combo4.current() == 6:
        a = [3, 1, 3, 1]
    if combo4.current() == 7:
        a = [4, 2, 2, 2]
    if combo4.current() == 8:
        a = [2, 1, 1, 1]
    return a


def tact() -> int:
    a = data_length()
    sum = 0
    for i in range(count_words):
        sum += a[i % len(a)]
    return sum


def address() -> int:
    if combo2.current() == 1:
        return 2
    else:
        return 1


def type_operation() -> str:
    if combo1.current() == 0:
        return "0110"
    if combo1.current() == 1:
        return "0111"
    if combo1.current() == 2:
        return "0010"
    if combo1.current() == 3:
        return "0011"


def is_read() -> int:
    return int(combo1.current() == 0 or combo1.current() == 2)


def count_bites() -> str:
    if combo3.current() == 0 or combo3.current() == 1:
        return "0000"
    if combo3.current() == 2:
        return "1100"
    if combo3.current() == 3:
        return "1110"


def is_64() -> int:
    if combo3.current() == 0:
        return 1


window = Tk()
window.title("Graphic PCI")
window.geometry('900x400')

lb1 = Label(window, text="Выберите операцию на шине: ")
lb1.grid(column=0, row=0)

combo1 = Combobox(window)
combo1['values'] = ("Чтение из памяти", "Запись в память", "Чтение с УВВ", "Запись в УВВ")
combo1.current(0)
combo1.grid(column=0, row=1)

lb2 = Label(window, text="Выберите разрядность адреса(бит): ")
lb2.grid(column=0, row=2)

combo2 = Combobox(window)
combo2['values'] = (32, 64)
combo2.current(0)
combo2.grid(column=0, row=3)

lb3 = Label(window, text="Выберите разрядность слова(бит): ")
lb3.grid(column=0, row=4)

combo3 = Combobox(window)
combo3['values'] = (64, 32, 16, 8)
combo3.current(0)
combo3.grid(column=0, row=5)

lb4 = Label(window, text="Выберите время доступа(нс): ")
lb4.grid(column=0, row=6)

combo4 = Combobox(window)
combo4['values'] = (30, 70, 100, 200, "3-1-1-1, 1-25 ns", "3-1-1-1, 1-20 ns",
                    "4-1-4-1, 1-20 ns", "5-2-2-2, 1-20 ns", "3-2-2-2, 1-15 ns")
combo4.current(0)
combo4.grid(column=0, row=7)

btn2 = Button(window, text="Вывести схему шины PCI.", command=clicked)
btn2.grid(column=2, row=1)

lb5 = Label(window, text="Введите количество слов: ")
lb5.grid(column=0, row=8)
num_input = Entry(window, width=10)
num_input.grid(column=0, row=9)
window.mainloop()
