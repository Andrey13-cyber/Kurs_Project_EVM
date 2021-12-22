from tkinter import *


class DrawPCI(Toplevel):
    def __init__(self, root, count_words, count_address, data_length, type_operation, is_read, count_bites, is_64):
        super(DrawPCI, self).__init__(root)

        self.is_64 = is_64  # то что передается 64 бита
        self.tact_length = 80  # длина одного такта
        self.x_start = 120  # координаты начала отрисовки по х
        self.y_start = 1  # координаты начала отрисовки по y
        self.y_height = 80  # высота одной линии
        self.count_lines = 7  # кол-во горизонтальных линий
        self.count_words = count_words  # количество слов
        self.shift = 0  # смещение линии вниз
        self.count_address = count_address  # количество блоков с адресом
        self.data_length = data_length  # длина блока данных
        self.type_operation = type_operation  # тип операции на шину
        self.is_read = is_read  # если операция - это чтение
        self.count_bites = count_bites  # разрядность слова
        self.init_count_tact(data_length, count_address, is_read)  # количество нужных тактов шины
        self.c = Canvas(self, bg='white', highlightthickness=0)
        self.title("Шина PCI")
        self.geometry("1600x800")
        self.grab_set()
        self.focus_set()
        self.initView()

    def init_count_tact(self, data_length, count_address, is_read):
        self.tact = 0
        for i in range(self.count_words):
            self.length_last_data = data_length[i % len(data_length)]
            self.tact += self.length_last_data
        self.tact_data = self.tact
        self.tact += count_address
        self.tact += is_read
        self.tact += 1

    def initView(self):
        x = 55
        y = 40
        self.c.pack(fill="both", expand=True)
        self.c.create_text(x, y, text="CLK", font="Verdana 10")
        y += self.y_height
        self.c.create_text(x, y, text="FRAME#", font="Verdana 10")
        y += self.y_height
        self.c.create_text(x, y, text="AD[0-31]", font="Verdana 10")
        y += self.y_height
        if self.is_64:
            self.c.create_text(x, y, text="AD[63-32]", font="Verdana 10")
            y += self.y_height
        self.c.create_text(x, y, text="C/BE[3-0]#", font="Verdana 10")
        y += self.y_height
        if self.is_64:
            self.c.create_text(x, y, text="C/BE[7-4]#", font="Verdana 10")
            y += self.y_height
        self.c.create_text(x, y, text="IRDY#", font="Verdana 10")
        y += self.y_height
        self.c.create_text(x, y, text="TRDY#", font="Verdana 10")
        y += self.y_height
        self.c.create_text(x, y, text="DEVSEL#", font="Verdana 10")
        y = self.y_height
        if self.is_64:
            self.count_lines = 9
        for i in range(self.count_lines):
            self.c.create_line(self.x_start, y, self.y_height * (self.tact + 2), y, dash=(4, 2))
            y += self.y_height
        self.c.create_line(self.x_start, self.y_start, self.x_start, self.y_height * self.count_lines)

        self.draw_tact()
        self.draw_frame()
        self.draw_data()
        self.draw_cbe()
        self.draw_address()
        if self.is_64:
            self.shift = 2
        self.draw_irdy_devsel(5 + self.shift)
        self.draw_irdy_devsel(7 + self.shift)
        self.draw_trdy()

    def polygon(self, length, first_tact, line, text):
        x = self.x_start + self.tact_length * first_tact - self.tact_length / 2
        y = self.y_height * line
        self.c.create_polygon(x, y - 20, x + 20, y - 40, x + 60 + 80 * (length - 1), y - 40, x + 80 * length, y - 20,
                              x + 60 + 80 * (length - 1), y, x + 20, y,
                              fill='#fff', outline='#000')
        self.c.create_text((x + 40 + 80 * (length - 1) / 2), y - 20, text=text,
                           justify=CENTER, font="Verdana 8")

    def draw_address(self):
        start = 1
        line = 3
        x = self.x_start  # 100
        y = self.y_height * line - 20
        for i in range(self.count_address):
            self.polygon(1, start, line, "Адрес")
            start += 1
        self.c.create_line(x, y, x + self.tact_length / 2, y)
        self.c.create_line(x + (self.tact - 1) * self.tact_length + self.tact_length / 2, y,
                           x + self.tact * self.tact_length + self.tact_length / 2, y)
        if self.is_read:
            self.c.create_line(x + self.count_address * self.tact_length + self.tact_length / 2, y,
                               x + (self.count_address + 1) * self.tact_length + self.tact_length / 2, y)

    def draw_tact(self):
        x = self.x_start
        y = self.y_start
        for i in range(self.tact):
            self.c.create_line(x, self.y_start, x + 30, y, x + 40, 80, x + 70, 80, x + 80, y)
            x += self.tact_length  # 80
            self.c.create_line(x, y, x, self.y_height * self.count_lines, dash=(4, 2))

    def draw_frame(self):
        x = self.x_start
        x_end = x + self.tact_length * (self.tact - self.length_last_data - 1) + self.tact_length / 2
        line = 2
        y = self.y_height * line
        self.c.create_line(x, y - 40, x + self.tact_length / 2, y - 40, x + self.tact_length / 2 + 10, y,
                           x_end, y, x_end + 10, y - 40, x + self.tact_length * (self.tact + 1), y - 40)

    def draw_cbe(self):
        start = 1
        line = 4
        if self.is_64:
            line = 5
        x = self.x_start
        y = self.y_height * line - 20
        if self.count_address == 1:
            self.polygon(1, start, line, self.type_operation)
            start += 1
        else:
            self.polygon(1, start, line, "1101")
            self.polygon(1, start + 1, line, self.type_operation)
            start += 2

        self.polygon(self.tact_data, start + self.is_read, line, self.count_bites)
        self.c.create_line(x, y, x + self.tact_length / 2, y)
        self.c.create_line(x + (self.tact - 1) * self.tact_length + self.tact_length / 2, y,
                           x + self.tact * self.tact_length + self.tact_length / 2, y)
        if self.is_read:
            self.c.create_line(x + self.count_address * self.tact_length + self.tact_length / 2, y,
                               x + (self.count_address + 1) * self.tact_length + self.tact_length / 2, y)
        if self.is_64:
            line += 1
            y = self.y_height * line - 20
            self.polygon(self.tact_data, start + self.is_read, line, self.count_bites)
            self.c.create_line(x, y,
                               x + self.tact_length * (self.count_address + self.is_read) + self.tact_length / 2, y)
            self.c.create_line(x + (self.tact - 1) * self.tact_length + self.tact_length / 2, y,
                               x + self.tact * self.tact_length + self.tact_length / 2, y)

    def draw_data(self):
        start = self.count_address + 1 + self.is_read
        line = 3
        x = self.x_start
        for i in range(self.count_words):
            length = self.data_length[i % len(self.data_length)]
            self.polygon(length, start, line, "Данные")
            start += length

        if self.is_64:
            line += 1
            start = self.count_address + 1 + self.is_read
            y = self.y_height * line - 20
            self.c.create_line(x, y,
                               x + self.tact_length * (self.count_address + self.is_read) + self.tact_length / 2, y)
            self.c.create_line(x + (self.tact - 1) * self.tact_length + self.tact_length / 2, y,
                               x + self.tact * self.tact_length + self.tact_length / 2, y)
            for i in range(self.count_words):
                length = self.data_length[i % len(self.data_length)]
                self.polygon(length, start, line, "Данные")
                start += length

    def draw_irdy_devsel(self, line):
        x = self.x_start
        x_end = x + self.tact_length * (self.tact - 1) + self.tact_length / 2
        y = self.y_height * line
        self.c.create_line(x, y - 40, x + self.tact_length * self.count_address + self.tact_length / 2, y - 40,
                           x + self.tact_length * self.count_address + self.tact_length / 2 + 10, y,
                           x_end + self.length_last_data, y, x_end + 10 + self.length_last_data, y - 40,
                           x + self.tact_length * (self.tact + 1) + self.length_last_data, y - 40)

    def draw_trdy(self):
        x = self.x_start
        line = 6 + self.shift
        y = self.y_height * line
        self.c.create_line(x, y - 40,
                           x + self.tact_length * (self.count_address + self.is_read + 1) - self.tact_length / 2,
                           y - 40)
        start = self.count_address + self.is_read + self.data_length[0] - 1
        for i in range(self.count_words):
            is_up = 0
            is_down = 0
            length = self.data_length[i % len(self.data_length)]
            if self.data_length[(i + 1) % len(self.data_length)] > 1 or i == (self.count_words - 1):
                is_up = 1
            if i == 0 or length > 1:
                is_down = 1
            self.draw_block_data(start, length, is_up, is_down)
            start += self.data_length[(i + 1) % len(self.data_length)]
        self.c.create_line(x + self.tact_length * (self.tact - 1) + self.tact_length / 2, y - 40,
                           x + self.tact_length * self.tact + self.tact_length / 2,
                           y - 40)

    def draw_block_data(self, start, length, is_up, is_down):
        incline_length = 10
        x = self.tact_length * start + self.x_start + self.tact_length / 2
        line = 6 + self.shift
        y = self.y_height * line
        if is_down:
            self.c.create_line(x - self.tact_length * (length - 1), y - 40, x, y - 40, x + incline_length, y)
        else:
            self.c.create_line(x, y, x + incline_length, y)

        self.c.create_line(x + incline_length, y,
                           x + self.tact_length - incline_length, y)

        if is_up:
            self.c.create_line(x + self.tact_length - incline_length, y, x + self.tact_length, y - 40)
        else:
            self.c.create_line(x + self.tact_length - incline_length, y, x + self.tact_length, y)
