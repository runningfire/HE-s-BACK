import tkinter as tk
from tkinter import ttk
import threading
from tkinter.constants import NORMAL
from model_related_table import WordPairs, MarkedUpPairs
from base import Session
from sqlalchemy import update
from ruaccent import RUAccent


class App(tk.Tk):
    button_translator = {
        1: "not_r",
        2: "ex_r",
        3: "low",
        4: "mid",
        5: "high",
        6: "left select last",
        7: "left select two",
        8: "right select last",
        9: "right select two",
    }
    vowels = ("а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я")

    @classmethod
    def get_vowels(cls) -> tuple:
        return tuple(vowel.upper() for vowel in cls.vowels) + cls.vowels

    def __init__(self, word_list: list, marked_pair_list: list):
        """
        Инициализация класса App.

        Параметры:
        - word_list: список словосочетаний для разметки
        - marked_pair_list: список размеченных словосочетаний
        """

        super().__init__()
        self.selected_item_id = None
        self.accentizer = RUAccent()
        self.accentizer.load(
            omograph_model_size="medium",
            dict_load_startup=False,
            disable_accent_dict=False,
        )
        self.event = threading.Event()
        self.word_list = word_list
        self.title("MarkUp-er")
        self.current_index = 0

        try:
            self.current_choise = App.convert_stress_representation(
                self.accentizer.process_all(self.word_list[self.current_index])
            )
        except:
            self.current_choise = self.word_list[self.current_index]

        self.letter_labels = []
        self.frame = ttk.Frame(self)
        self.frame.grid(row=0, column=0, sticky="n")

        # Создаем холст
        self.canvas = tk.Canvas(self.frame, width=700, height=150)
        self.canvas.grid(row=1, column=0, sticky="n")

        # Создаем лейблы для splitted left и splitted right
        self.splitted_left_label = ttk.Label(self.frame)
        self.splitted_left_label.grid(row=2, column=0, sticky="w")

        self.splitted_right_label = ttk.Label(self.frame)
        self.splitted_right_label.grid(row=2, column=1, sticky="w")

        self.create_labels()
        self.addition = 0
        self.grid_rowconfigure(0, weight=2)
        self.buttons_frame = ttk.Frame(self.frame)
        self.buttons_frame.grid(row=3, column=0, sticky="n")
        self.marked_pair_list = marked_pair_list
        self.buttons = []
        self.splitted_left, self.splitted_right = None, None
        self.selected_button = None
        self.selected_text = None
        self.button_style = ttk.Style()
        self.button_style.configure("My.TButton", background="SystemButtonFace")
        self.checkbutton_style = ttk.Style()
        self.checkbutton_style.configure(
            "My.TCheckbutton", background="lightgray", foreground="black"
        )
        self.initialize_buttons()
        self.restorator = (
            lambda index, string, space_tab: string[: space_tab[0]]
            + string[space_tab[0] : index].lower()
            + string[index].upper()
            + string[(index + 1) : (space_tab[1])].lower()
            + string[space_tab[1] :]
        )

        # Стиль для фрейма
        style = ttk.Style()
        style.configure("My.TFrame", background="lightgray", relief="solid")

        style = ttk.Style()
        style.configure("TButton", background="SystemButtonFace")
        style.configure("Toggled.TButton", foreground="green", background="green")

        # Стиль для выбора (флажков)
        style.configure("My.TCheckbutton", background="lightgray", foreground="black")
        self.geometry("950x380")
        self.resizable(width=False, height=False)

    def initialize_buttons(self):
        """
        Инициализация кнопок для выбора класса разметки.
        """

        for i in range(5):
            translate = App.button_translator[i + 1]
            button = ttk.Button(
                self.buttons_frame,
                text=translate,
                style="My.TButton",
                command=lambda text=translate: self.toggle_button(text),
                state=NORMAL,
            )
            button.pack(side=tk.TOP, anchor=tk.W, padx=10)
            self.buttons.append(button)

        self.left_select_var = tk.IntVar()

        left_select_last_button = ttk.Checkbutton(
            self.buttons_frame,
            text="left select last",
            style="My.TCheckbutton",
            variable=self.left_select_var,
            onvalue=1,
            offvalue=0,
            command=lambda: self.select_left_option(self.left_select_var.get()),
        )
        left_select_last_button.pack(side=tk.LEFT, anchor=tk.N)
        self.buttons.append(left_select_last_button)

        left_select_two_button = ttk.Checkbutton(
            self.buttons_frame,
            text="left select two",
            style="My.TCheckbutton",
            variable=self.left_select_var,
            onvalue=2,
            offvalue=0,
            command=lambda: self.select_left_option(self.left_select_var.get()),
        )
        left_select_two_button.pack(side=tk.LEFT, anchor=tk.N)
        self.buttons.append(left_select_two_button)

        self.right_select_var = tk.IntVar()

        right_select_last_button = ttk.Checkbutton(
            self.buttons_frame,
            text="right select last",
            style="My.TCheckbutton",
            variable=self.right_select_var,
            onvalue=1,
            offvalue=0,
            command=lambda: self.select_right_option(self.right_select_var.get()),
        )
        right_select_last_button.pack(side=tk.LEFT, anchor=tk.N)
        self.buttons.append(right_select_last_button)

        right_select_two_button = ttk.Checkbutton(
            self.buttons_frame,
            text="right select two",
            style="My.TCheckbutton",
            variable=self.right_select_var,
            onvalue=2,
            offvalue=0,
            command=lambda: self.select_right_option(self.right_select_var.get()),
        )
        right_select_two_button.pack(side=tk.LEFT, anchor=tk.N)
        self.buttons.append(right_select_two_button)

        button = ttk.Button(
            self.buttons_frame,
            text="skip",
            style="My.TButton",
            command=self.update_label,
        )
        button.pack(side="right", anchor=tk.S)
        self.buttons.append(button)

        button = ttk.Button(
            self.buttons_frame,
            text="commit",
            style="My.TButton",
            command=self.commiter,
        )
        button.pack(side="right", anchor=tk.S, padx=10)
        self.buttons.append(button)

    def create_labels(self):
        """
        Создание лейблов для отображения букв словосочетания на холсте.
        """

        word = self.current_choise
        x = 50
        self.text_id = 1
        self.item_ids = []
        for i, letter in enumerate(word):
            text_id = self.text_id
            self.text_id += 1
            text = self.canvas.create_text(
                x, 100, text=letter, font=("Arial", 15), fill="black"
            )
            self.canvas.tag_bind(text, "<Button-1>", self.letter_click)
            self.letter_labels.append({"index": i, "text_id": text_id})
            self.item_ids.append(text)
            x += 12

    def letter_click(self, event):
        """
        Обработка клика на букву на холсте.
        """

        for label in self.letter_labels:
            self.canvas.itemconfig(label["text_id"], fill="black")

        item_ids = self.canvas.find_withtag(tk.CURRENT)
        for item_id in item_ids:
            index = self.letter_labels[item_id - self.addition - 1]["index"]
            letter = self.canvas.itemcget(item_id, "text")

            if letter in App.get_vowels():
                spaces = App.get_space_indices(self.current_choise)
                word_in_spaces = App.search_word(index, spaces)
                self.current_choise = self.restorator(
                    index, self.current_choise, word_in_spaces
                )
                self.canvas.itemconfig(item_id, fill="yellow", text=letter.upper())
                self.selected_item_id = item_id

                for label in self.letter_labels:
                    if label["text_id"] + self.addition != self.selected_item_id:
                        index = label["index"]
                        if word_in_spaces[0] < index < word_in_spaces[1]:
                            self.canvas.itemconfig(
                                label["text_id"] + self.addition,
                                fill="black",
                                text=self.current_choise[index].lower(),
                            )
            else:
                self.messager("You've got to select a vowel to mark the stress.")

    @staticmethod
    def get_space_indices(string: str) -> list:
        """
        Возвращает список индексов пробелов в строке исключая первый и последний символы.

        Параметры:
        - string: строка

        Возвращает:
        - list_space: список кортежей с индексами пробелов
        """

        space_indices = [0]  # добавляем первый индекс, равный 0
        for i, char in enumerate(string):
            if char == " ":
                space_indices.append(i)
        space_indices.append(len(string))  # добавляем последний индекс
        list_space = [
            (space_indices[i], space_indices[i + 1])
            for i in range(len(space_indices) - 1)
        ]
        return list_space

    @staticmethod
    def search_word(index: int, list_space: list) -> tuple:
        """
        Ищет слово, содержащее заданный индекс, в списке пробелов.

        Параметры:
        - index: индекс
        - list_space: список кортежей с индексами пробелов

        Возвращает:
        - spaces: кортеж с индексами пробелов, в котором находится индекс
        """

        for spaces in list_space:
            if (index > spaces[0]) and (index < spaces[1]):
                return spaces

    def select_left_option(self, value: int):
        """
        Обновляет значение переменной self.splitted_left в зависимости от выбранной опции "left select last" или "left select two".

        Параметры:
        - value: выбранное значение опции
        """

        splitted, dash_index = self.splitter()[1], self.splitter()[0]
        if value == 1:
            self.splitted_left = splitted[dash_index - 1]
        elif value == 2:
            self.splitted_left = splitted[(dash_index - 2) : dash_index]
            self.splitted_left = f"{self.splitted_left[0]} {self.splitted_left[1]}"

        label_text = f"Splitted Left: {self.splitted_left}\n"
        self.splitted_left_label.config(text=label_text, font=("Comic Sans MS", 12))

    def select_right_option(self, value: int):
        """
        Обновляет значение переменной self.splitted_right в зависимости от выбранной опции "right select last"
        или "right select two".

        Параметры:
        - value: выбранное значение опции
        """
        splitted, dash_index = self.splitter()[1], self.splitter()[0]
        if value == 1:
            self.splitted_right = splitted[-1]
        elif value == 2:
            self.splitted_right = splitted[-2:]
            self.splitted_right = f"{self.splitted_right[0]} {self.splitted_right[1]}"

        label_text = f"Splitted Right: {self.splitted_right}\n"
        self.splitted_right_label.config(text=label_text, font=("Comic Sans MS", 12))

    @property
    def return_marked_list(self):
        """
        Возвращает список размеченных словосочетаний.
        """
        return self.marked_pair_list

    @staticmethod
    def messager(text: str):
        """
        Создает окно с сообщением об ошибке.

        Параметры:
        - text: текст сообщения об ошибке
        """

        top_level = tk.Toplevel()
        top_level.title("Exceptional")
        top_level.geometry("300x150")
        label = tk.Label(top_level, text=text)
        label.pack(pady=20)
        close_button = tk.Button(top_level, text="Close", command=top_level.destroy)
        close_button.pack(pady=10)

    def toggle_button(self, text: str):
        """
        Переключает стиль кнопки выбора класса разметки.

        Параметры:
        - text: текст кнопки
        """

        index = list(App.button_translator.values()).index(text)
        button = self.buttons[index]

        if self.selected_button == button:
            button.configure(style="TButton")
            self.selected_button = None
        else:
            if self.selected_button:
                self.selected_button.configure(style="TButton")
            button.configure(style="Toggled.TButton")
            self.selected_button = button
            self.selected_text = text

    @classmethod
    def convert_stress_representation(cls, text: str) -> str:
        """
        Преобразует представление ударения в слове.

        Параметры:
        - text: слово со знаками ударения

        Возвращает:
        - renew: слово с преобразованным представлением ударения
        """

        splitted = text.split(" ")
        new_splitted = []
        for word in splitted:
            vowel_count = 0
            if word == "-":
                new_splitted.append(word)
                continue
            for index, char in enumerate(word):
                if char in cls.get_vowels():
                    vowel_count += 1

                if index == 0:
                    continue

                if word[index - 1] == "+":
                    new_word = word[:index] + word[index].upper() + word[(index + 1) :]
                    new_word = new_word.replace("+", "")

            if vowel_count == 1:
                for char in word:
                    if char in cls.get_vowels():
                        new_word = new_word.replace(char, char.upper())

            new_splitted.append(new_word)

        renew = " ".join(new_splitted).strip()

        return renew

    def splitter(self):
        """
        Разделяет текущее словосочетание на две части: перед и после дефиса.

        Возвращает:
        - dash_index: индекс дефиса
        - splitted: список слов после разделения
        """
        splitted = self.current_choise.split(" ")
        dash_index = splitted.index("-")
        return dash_index, splitted

    def commiter(self):
        """
        Сохраняет выбранные значения класса разметки в списке размеченных словосочетаний и обновляет отображение.
        """

        if self.splitted_left and self.splitted_right and self.selected_text:
            data = (self.splitted_left, self.splitted_right, self.selected_text)
            self.marked_pair_list.append(data)
            self.update_label()
            print(self.return_marked_list)
        else:
            self.messager("Should've choisen left, right and class parameters")

    def update_label(self):
        """
        Обновляет отображение словосочетания на холсте и сбрасывает значения выбранных параметров.
        """

        self.addition += len(self.current_choise)
        self.current_index += 1

        if self.current_index < len(self.word_list):
            try:
                self.current_choise = App.convert_stress_representation(
                    self.accentizer.process_all(self.word_list[self.current_index])
                )
            except:
                self.current_choise = self.word_list[self.current_index]

            self.splitted_left, self.splitted_right, self.selected_text = (
                None,
                None,
                None,
            )

            self.splitted_left_label.config(text="")
            self.splitted_right_label.config(text="")
            self.canvas.delete("all")  # Удаляем все элементы на холсте
            self.letter_labels = []
            self.create_labels()

            for button in self.buttons:
                if isinstance(button, ttk.Checkbutton):
                    self.left_select_var.set(0)
                    self.right_select_var.set(0)
                else:
                    button.configure(style="TButton")

        else:
            self.event.set()
            self.destroy()

    def start(self):
        self.mainloop()


def iterate_list():
    marked_pair_list = []
    session = Session()
    data = session.query(WordPairs).filter(WordPairs.is_valid.is_(None)).all()
    session.close()
    for record in data:
        session = Session()
        app = App(
            record.word_pair, marked_pair_list
        )  # передача word_list и marked_pair_list в класс App
        app.start()

        app.event.wait()
        session.execute(
            update(WordPairs).where(WordPairs.id == record.id).values(is_valid=True)
        )

        session.commit()
        for marked in app.return_marked_list:
            marked_record = MarkedUpPairs(
                poem_relate_id=record.id,
                word_pair=(marked[0], marked[1]),
                class_name=marked[2],
            )
            session.add(marked_record)
        session.commit()
        session.close()
        app.event.clear()


if __name__ == "__main__":
    iterate_list()
