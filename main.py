import customtkinter as ctk
import json
import random
from threading import Thread
from time import sleep


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')

        self.geometry('1000x600')
        self.minsize(1000, 600)
        self.title('Typing Speed Test')

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.frame = ctk.CTkFrame(master=self)
        self.frame.grid(column=0, row=0, sticky='nsew')
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=4)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.words = []
        self.correct_words = []
        self.counter = 0
        self.input = ctk.StringVar()
        self.input.trace_add("write", callback=self.check_input)
        self.input_box = ctk.CTkEntry(master=self.frame, textvariable=self.input, width=880, height=20, font=("Arial", 30))
        self.input_box.focus_set()
        self.input_box.grid(row=2, column=0, columnspan=2, sticky="n", pady=10)
        self.create_word_list(open("data/words"))
        self.display_words()
        self.score_label = ctk.CTkLabel(master=self.frame, text=f"WPM: 0", font=("Arial", 30))
        self.score_label.grid(row=0, column=0, sticky="se", padx=20)
        self.time_left = 60
        self.timer_thread = Thread(target=self.timer)
        self.timer_thread.start()

        self.mainloop()

    def create_word_list(self, file):
        data = json.load(file)
        for word in data["commonWords"]:
            self.words.append(word)
            random.shuffle(self.words)

    def display_words(self):
        self.text_box = ctk.CTkTextbox(master=self.frame, width=880, height=390, wrap="word", font=("Arial", 30))
        self.text_box.grid(row=1, column=0, columnspan=2, sticky="s", pady=20)
        self.text_box.insert(index="0.0", text=self.words[:200])
        self.text_box.configure(state="disabled")

    def check_input(self, var, index, mode):
        user_word_list = self.input.get().split()
        current_word = user_word_list[len(user_word_list) - 1]
        current_word_goal = self.words[len(user_word_list) - 1]
        length_of_input = len(self.input.get())
        self.text_box.tag_config("correct", foreground="green")
        self.text_box.tag_config("incorrect", foreground="red")
        self.text_box.tag_remove("correct", f"1.{length_of_input - 1}", f"1.{length_of_input}")
        self.text_box.tag_remove("incorrect", f"1.{length_of_input - 1}", f"1.{length_of_input}")
        try:
            if current_word[len(current_word) - 1] == current_word_goal[len(current_word) - 1]:
                self.text_box.tag_add("correct", f"1.{length_of_input - 1}", f"1.{length_of_input}")
            else:
                self.text_box.tag_add("incorrect", f"1.{length_of_input - 1}", f"1.{length_of_input}")
        except IndexError as e:
            print(f"{e}")
        if current_word == current_word_goal:
            self.counter += 1
            if self.counter % 2 == 0:
                self.correct_words.append(current_word_goal)
                self.update_score()

    def update_score(self):
        self.cpm = sum([len(word) for word in self.correct_words])
        self.wpm = self.cpm / (60 - self.time_left) * 60 / 5
        self.score_label.configure(text=f"WPM: {int(self.wpm)}")

    def timer(self):
        timer_label = ctk.CTkLabel(master=self.frame, text=f"Time: {self.time_left}", font=("Arial", 30))
        timer_label.grid(row=0, column=1, sticky="sw", padx=20)
        while self.time_left != 0:
            sleep(1)
            self.time_left -= 1
            timer_label.configure(text=f"Time: {self.time_left}")
        if self.time_left == 0:
            self.show_score()

    def show_score(self):
        self.frame.grid_forget()
        self.score_board = ctk.CTkFrame(master=self)
        self.score_board.columnconfigure(0, weight=1)
        self.score_board.rowconfigure(0, weight=5)
        self.score_board.rowconfigure(1, weight=1)
        self.score_board.grid(column=0, row=0, sticky="nsew")
        self.final_score = ctk.CTkLabel(master=self.score_board, text=f"Time's up! Final score:\n\nCPM: {self.cpm}\nWPM: {int(self.cpm / 5)}", font=("Arial", 30))
        self.final_score.grid(column=0, row=0, sticky='nsew')
        self.legend = ctk.CTkLabel(master=self.score_board, text="CPM - Characters Per Minute is the number of characters in correctly typed words.\n WPM - Words Per Minute is CPM divided by 5.", font=("Arial", 20))
        self.legend.grid(column=0, row=1, sticky='nsew')


App()
