from tkinter import *
import random

FONT = ("Helvetica", 24, "bold")
BACKGROUND = "#EEEEEE"
GAME_BUTTONS = "#F5F5F5"
BUTTON_PADDING = 7
BUTTON_FG_X = "blue"
BUTTON_FG_O = "green"
BUTTON_BORDER_COLOR = "#79E0EE"
O_WON_COLOR = "#A2FF86"
X_WON_COLOR = "#79E0EE"
state = True
DELAY_SECOND = 2000
# X turn
clicked_x = True
# O turn
clicked_y = True

count = 0
time_delay = None
draw_state = False
# Game ui
game = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
       ]
places = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
turn = 0


class MultiPageApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Create a container to hold all the frames
        container = Frame(self)
        container.config(padx=5, pady=30, bg=BACKGROUND)
        container.pack(fill="both", expand=True)

        self.frames = {}  # Dictionary to store all frames

        # Create multiple frames and add them to the dictionary
        for PageClass in (HomePage, Versus_bot, Play_Friend):
            frame = PageClass(container, self)
            self.frames[PageClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame(HomePage)

    def show_frame(self, page):
        # Raise the specified frame to the top
        frame = self.frames[page]
        frame.tkraise()


class Game_UI(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BACKGROUND)

        self.label = Label(self, text="Tic Tac Toe", font=("Helvetica", 24, "bold"), bg=BACKGROUND, fg=BUTTON_FG_X)
        self.label.grid(column=1, row=0)
        # Buttons
        reset_button_border = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        menu_button_border = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_1 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_2 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_3 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_4 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_5 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_6 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_7 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_8 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        button_border_9 = Frame(self, highlightbackground=BUTTON_BORDER_COLOR, highlightthickness=7, bd=0)
        reset_button_border.grid(column=1, row=4, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        menu_button_border.grid(column=2, row=4, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_1.grid(column=0, row=1, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_2.grid(column=1, row=1, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_3.grid(column=2, row=1, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_4.grid(column=0, row=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_5.grid(column=1, row=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_6.grid(column=2, row=2, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_7.grid(column=0, row=3, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_8.grid(column=1, row=3, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        button_border_9.grid(column=2, row=3, padx=BUTTON_PADDING, pady=BUTTON_PADDING)
        b1 = Button(button_border_1, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, disabledforeground="",
                    bg=GAME_BUTTONS, command=lambda: self.b_click(b1, 0, 0))
        b2 = Button(button_border_2, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b2, 0, 1))
        b3 = Button(button_border_3, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b3, 0, 2))

        b4 = Button(button_border_4, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b4, 1, 0))
        b5 = Button(button_border_5, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b5, 1, 1))
        b6 = Button(button_border_6, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b6, 1, 2))

        b7 = Button(button_border_7, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b7, 2, 0))
        b8 = Button(button_border_8, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b8, 2, 1))
        b9 = Button(button_border_9, text=" ", font=("Helvetica", 22, "bold"), height=3, width=6, bg=GAME_BUTTONS,
                    command=lambda: self.b_click(b9, 2, 2))
        self.buttons = [(b1, b2, b3), (b4, b5, b6), (b7, b8, b9)]

        reset_button = Button(reset_button_border, text="Reset", fg=BUTTON_FG_X, font=("Helvetica", 22, "bold"),
                              height=1, width=6, bg=GAME_BUTTONS, command=self.reset)
        menu_button = Button(menu_button_border, text="Menu", fg=BUTTON_FG_X, font=("Helvetica", 22, "bold"),
                             height=1, width=6, bg=GAME_BUTTONS,
                             command=lambda: [controller.show_frame(HomePage), self.reset()])

        # Button placing
        reset_button.grid(column=1, row=4)
        menu_button.grid(column=2, row=4)
        b1.grid(column=0, row=1)
        b2.grid(column=1, row=1)
        b3.grid(column=2, row=1)

        b4.grid(column=0, row=2)
        b5.grid(column=1, row=2)
        b6.grid(column=2, row=2)

        b7.grid(column=0, row=3)
        b8.grid(column=1, row=3)
        b9.grid(column=2, row=3)


class HomePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=BACKGROUND, padx=150)

        label_1 = Label(self, text="Tic", font=("Helvetica", 48, "bold"), bg=BACKGROUND, fg="#FBD85D")
        label_1.grid(row=0, column=0, pady=5)
        label_2 = Label(self, text="Tac", font=("Helvetica", 48, "bold"), bg=BACKGROUND, fg="#D864A9")
        label_2.grid(row=1, column=0, pady=5)
        label_3 = Label(self, text="Toe", font=("Helvetica", 48, "bold"), bg=BACKGROUND, fg="#78C1F3")
        label_3.grid(row=2, column=0, pady=5)

        button1 = Button(self, text="Play Friend", font=FONT, bg=BACKGROUND, fg=BUTTON_FG_X, command=lambda: controller.show_frame(Play_Friend))
        button1.grid(row=3, column=0, pady=15)

        button2 = Button(self, text="Versus Bot", font=FONT, bg=BACKGROUND, fg=BUTTON_FG_X, command=lambda: controller.show_frame(Versus_bot))
        button2.grid(row=4, column=0, pady=15)


class Play_Friend(Game_UI):
    def __init__(self, parent, controller):
        Game_UI.__init__(self, parent, controller)
        self.clicked_x = True
        self.clicked_y = True

    def check(self):
        global state, draw_state
        r_x = 0
        c_x = 0
        r_o = 0
        c_o = 0
        # print(game)
        for row in range(0, 3):
            for column in range(0, 3):
                if game[row][column] == "X":
                    r_x += 1
                else:
                    r_x = 0
                if game[row][column] == "O":
                    r_o += 1
                else:
                    r_o = 0
            if r_x == 3:
                for column in range(0, 3):
                    self.buttons[row][column]["bg"] = X_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="X won")
                print("X row won")  # working
            if r_o == 3:
                for column in range(0, 3):
                    self.buttons[row][column]["bg"] = O_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="O won")
                print("O row won")  # working
        for column in range(0, 3):
            for row in range(0, 3):
                if game[row][column] == "X":
                    c_x += 1
                else:
                    c_x = 0
                if game[row][column] == "O":
                    c_o += 1
                else:
                    c_o = 0
            if c_x == 3:
                for row in range(0, 3):
                    self.buttons[row][column]["bg"] = X_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="X won")
                print("X column won")  # working
            if c_o == 3:
                for row in range(0, 3):
                    self.buttons[row][column]["bg"] = O_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="O won")
                print("O column won")  # working
        if game[0][0] == "X" and game[1][1] == "X" and game[2][2] == "X":
            for row in range(0, 3):
                for column in range(0, 3):
                    if row == column:
                        self.buttons[row][column]["bg"] = X_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="X won")
            print("X won")  # working
        elif game[0][2] == "X" and game[1][1] == "X" and game[2][0] == "X":
            self.buttons[0][2]["bg"] = X_WON_COLOR
            self.buttons[1][1]["bg"] = X_WON_COLOR
            self.buttons[2][0]["bg"] = X_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="X won")
            print("X won")  # working
        elif game[0][0] == "O" and game[1][1] == "O" and game[2][2] == "O":
            for row in range(0, 3):
                for column in range(0, 3):
                    if row == column:
                        self.buttons[row][column]["bg"] = O_WON_COLOR
            state = False
            draw_state = False
            print("O won")  # working
            self.label.config(text="O won")
        elif game[0][2] == "O" and game[1][1] == "O" and game[2][0] == "O":
            self.buttons[0][2]["bg"] = O_WON_COLOR
            self.buttons[1][1]["bg"] = O_WON_COLOR
            self.buttons[2][0]["bg"] = O_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="O won")
            print("O won")  # working
        if not state:
            for row in range(0, 3):
                for column in range(0, 3):
                    self.buttons[row][column]["state"] = DISABLED
        not_empty = 0
        for row in range(0, 3):
            for column in range(0, 3):
                if self.buttons[row][column]["state"] == DISABLED:
                    not_empty += 1
        if not_empty == 9:
            draw_state = True
        if self.label["text"] != "X won" and self.label["text"] != "O won" and draw_state == True:
            self.label.config(text="Draw")

    def opponent_click(self, row, col):
        button = self.buttons[row][col]
        if button["text"] == " " and self.clicked_y:
            self.label.config(text="X's turn")
            game[row][col] = "O"
            button["text"] = "O"
            button["state"] = DISABLED
            button["disabledforeground"] = BUTTON_FG_O
            self.clicked_x = True
            self.clicked_y = False
            self.check()

    def b_click(self, b, row, col):
        global turn, count
        turn += 1
        if b["text"] == " " and self.clicked_x:
            # print(self.clicked_x)
            game[row][col] = "X"
            b["text"] = "X"
            b["state"] = DISABLED
            b["disabledforeground"] = BUTTON_FG_X
            count += 1
            self.clicked_y = True
            self.clicked_x = False
            # print("hello")
        if count < 5:
            self.label.config(text="O's turn")
            self.opponent_click(row, col)
        if turn >= 2:
            self.check()

    def reset(self):
        global game, turn, count, places, state, time_delay, draw_state
        # Resetting constants
        count = 0
        time_delay = None
        state = True
        places = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        game = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
        turn = 0
        self.clicked_x = True
        self.clicked_y = True
        draw_state = False
        # Clearing buttons
        for row in range(0, 3):
            for column in range(0, 3):
                self.buttons[row][column].config(text=" ", bg=GAME_BUTTONS)
        # Respond buttons
        for row in range(0, 3):
            for column in range(0, 3):
                self.buttons[row][column]["state"] = ACTIVE
        self.label.config(text="Tic Tac Toe")


class Versus_bot(Game_UI):
    def __init__(self, parent, controller):
        Game_UI.__init__(self, parent, controller)

    def reset(self):
        global game, turn, clicked_y, clicked_x, count, places, state, time_delay, draw_state
        # Resetting constants
        count = 0
        time_delay = None
        state = True
        places = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        game = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
        ]
        turn = 0
        clicked_x = True
        clicked_y = False
        draw_state = False
        # Clearing buttons
        for row in range(0, 3):
            for column in range(0, 3):
                self.buttons[row][column].config(text=" ", bg=GAME_BUTTONS)
        # Respond buttons
        for row in range(0, 3):
            for column in range(0, 3):
                self.buttons[row][column]["state"] = ACTIVE
        self.label.config(text="Tic Tac Toe")

    def check(self):
        global state, draw_state
        r_x = 0
        c_x = 0
        r_o = 0
        c_o = 0
        # print(game)
        for row in range(0, 3):
            for column in range(0, 3):
                if game[row][column] == "X":
                    r_x += 1
                else:
                    r_x = 0
                if game[row][column] == "O":
                    r_o += 1
                else:
                    r_o = 0
            if r_x == 3:
                for column in range(0, 3):
                    self.buttons[row][column]["bg"] = X_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="X won")
                print("X row won")  # working
            if r_o == 3:
                for column in range(0, 3):
                    self.buttons[row][column]["bg"] = O_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="O won")
                print("O row won")  # working
        for column in range(0, 3):
            for row in range(0, 3):
                if game[row][column] == "X":
                    c_x += 1
                else:
                    c_x = 0
                if game[row][column] == "O":
                    c_o += 1
                else:
                    c_o = 0
            if c_x == 3:
                for row in range(0, 3):
                    self.buttons[row][column]["bg"] = X_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="X won")
                print("X column won")  # working
            if c_o == 3:
                for row in range(0, 3):
                    self.buttons[row][column]["bg"] = O_WON_COLOR
                state = False
                draw_state = False
                self.label.config(text="O won")
                print("O column won")  # working
        if game[0][0] == "X" and game[1][1] == "X" and game[2][2] == "X":
            for row in range(0, 3):
                for column in range(0, 3):
                    if row == column:
                        self.buttons[row][column]["bg"] = X_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="X won")
            print("X won")  # working
        elif game[0][2] == "X" and game[1][1] == "X" and game[2][0] == "X":
            self.buttons[0][2]["bg"] = X_WON_COLOR
            self.buttons[1][1]["bg"] = X_WON_COLOR
            self.buttons[2][0]["bg"] = X_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="X won")
            print("X won")  # working
        elif game[0][0] == "O" and game[1][1] == "O" and game[2][2] == "O":
            for row in range(0, 3):
                for column in range(0, 3):
                    if row == column:
                        self.buttons[row][column]["bg"] = O_WON_COLOR
            state = False
            draw_state = False
            print("O won")  # working
            self.label.config(text="O won")
        elif game[0][2] == "O" and game[1][1] == "O" and game[2][0] == "O":
            self.buttons[0][2]["bg"] = O_WON_COLOR
            self.buttons[1][1]["bg"] = O_WON_COLOR
            self.buttons[2][0]["bg"] = O_WON_COLOR
            state = False
            draw_state = False
            self.label.config(text="O won")
            print("O won")  # working
        if not state:
            for row in range(0, 3):
                for column in range(0, 3):
                    self.buttons[row][column]["state"] = DISABLED
        not_empty = 0
        for row in range(0, 3):
            for column in range(0, 3):
                if self.buttons[row][column]["state"] == DISABLED:
                    not_empty += 1
        if not_empty == 9:
            draw_state = True
        if self.label["text"] != "X won" and self.label["text"] != "O won" and draw_state == True:
            self.label.config(text="Draw")

    def computer_click(self):
        global clicked_x, time_delay, state
        self.after_cancel(time_delay)
        if state:
            self.label.config(text="X's turn")
            x = None
            y = None
            random_place = random.choice(places)
            # print(random_place)
            x = random_place[0]
            y = random_place[1]
            game[x][y] = "O"
            places.remove((x, y))
            button = self.buttons[x][y]
            button["text"] = "O"
            button["state"] = DISABLED
            button["disabledforeground"] = BUTTON_FG_O
            clicked_x = True
            self.check()

    def b_click(self, b, row, col):
        global clicked_x, count, clicked_y, p_c_time, turn, time_delay
        turn += 1
        # print(f"Turn -> {turn}")
        if b["text"] == " " and clicked_x:
            game[row][col] = "X"
            places.remove((row, col))
            # print(places)
            b["text"] = "X"
            b["state"] = DISABLED
            b["disabledforeground"] = BUTTON_FG_X
            clicked_x = False
            count += 1
            # print(game)
        if count < 5:
            self.label.config(text="O's turn")
            time_delay = self.after(DELAY_SECOND, self.computer_click)
        if turn >= 2:
            # print("checking...")
            self.check()


class ContactPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        label = Label(self, text="Contact Page", font=("Helvetica", 18))
        label.pack(pady=10)

        button1 = Button(self, text="Go to Home Page", command=lambda: controller.show_frame(HomePage))
        button1.pack()

        button2 = Button(self, text="Go to About Page", command=lambda: controller.show_frame(Versus_bot))
        button2.pack()

