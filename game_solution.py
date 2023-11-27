'''
Name: Moeed Chughtai
Resolution: 1280x720
Background Image Ref: https://wallpapers.com/4k-space

The Menu class creates the different menu options. Play will start from level 1 and progress through to level 2 and 3.
The levels options allows the user to pick a specifc level. The leaderboards will display the top 5 scores of all times.
The customisation allows the user to pick the left and right keys for the paddle. The load will load the last saved game
which is stored in a json file.
'''

from tkinter import *
from tkinter import simpledialog, ttk
from PIL import ImageTk, Image
from game import Game

class Menu:

    def __init__(self, windowX, windowY):
        self.window = Tk()
        self.windowX = windowX
        self.windowY = windowY
        self.buttonWidth = 14
        self.fontSize = 23
        self.create_main_menu()


    def create_main_menu(self):
        self.destroy_all_widgets() # Destroy all existing widgets to clear the window before displaying main menu

        # Load and set image as background
        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/menu.jpg"))
        backgroundLabel = Label(self.window, image=self.backgroundImg)
        backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Style for title
        style = ttk.Style()
        style.configure(
            "TitleLabel.TLabel",
            font=("Small Fonts", 80),
            foreground="white",
            background="#00008B",
            padding=(20, 20),
            relief="raised",
        )
        # Title
        titleLabel = ttk.Label(self.window, text="BLOCK BREAKER", style="TitleLabel.TLabel")
        titleLabel.pack(side='top', pady=40)

        # Play button
        playButton = Button(self.window, text="PLAY", command=self.start_game, bg="green", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        playButton.pack(side=TOP, pady=10)

        # Levels button
        levelsButton = Button(self.window, text="LEVELS", command=self.levels_menu, bg="orange", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        levelsButton.pack(side=TOP, pady=10)

        # Leaderboards button
        leaderboardsButton = Button(self.window, text="LEADERBOARDS", command=self.show_leaderboard, bg="red", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        leaderboardsButton.pack(side=TOP, pady=10)

        # Customisation button
        customisationButton = Button(self.window, text="CUSTOMISATION", command=self.customise_controls, bg="red", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        customisationButton.pack(side=TOP, pady=10)

        # Load Button
        loadButton = Button(self.window, text="LOAD", command=self.load_game, bg="orange", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        loadButton.pack(side=TOP, pady=10)

        # Exit button
        exitButton = Button(self.window, text="EXIT", command=self.window.destroy, bg="green", fg="black", font=("Terminal", self.fontSize), width=self.buttonWidth)
        exitButton.pack(side=TOP, pady=10)


    def start_game(self):
        playerName = simpledialog.askstring("Player Name", "Enter your name:") # Popup window to ask user to input their name
        if playerName is not None and playerName.strip() != "": # Make sure name is valid
            self.destroy_all_widgets()
            # Create a game object and start the game
            game = Game(self.window, self.windowX, self.windowY, playerName, self.create_main_menu)
            game.start_game()


    def levels_menu(self):
        self.destroy_all_widgets()

        # Load and set image as background
        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/menu.jpg"))
        self.backgroundLabel = Label(self.window, image=self.backgroundImg)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Level selection style
        style = ttk.Style()
        style.configure(
            "LevelLabel.TLabel",
            font=("Small Fonts", 70),
            foreground="white",
            background="black",
            padding=(20, 20),
            relief="raised",
        )
        levelSelectionLabel = ttk.Label(self.window, text="SELECT LEVEL", style="LevelLabel.TLabel")
        levelSelectionLabel.pack(side=TOP, pady=40)

        level1Button = Button(self.window, text="Level 1", command=lambda: self.level_selection(1), bg="green", fg="black", font=("Terminal", 30))
        level1Button.pack(side=TOP, pady=20)

        level2Button = Button(self.window, text="Level 2", command=lambda: self.level_selection(2), bg="orange", fg="black", font=("Terminal", 30))
        level2Button.pack(side=TOP, pady=20)

        level3Button = Button(self.window, text="Level 3", command=lambda: self.level_selection(3), bg="red", fg="black", font=("Terminal", 30))
        level3Button.pack(side=TOP, pady=20)

        # Return to main menu
        backButton = Button(self.window, text="BACK", command=self.create_main_menu, bg="#2c3e50", fg="black", font=("Terminal", 25))
        backButton.place(x=10, y=10)


    # Play a specific level
    def level_selection(self, level):
        playerName = simpledialog.askstring("Player Name", "Enter your name:")
        self.destroy_all_widgets()

        if level == 1:
            if playerName is not None and playerName.strip() != "":
                game = Game(self.window, self.windowX, self.windowY, playerName, self.create_main_menu)
                game.start_game()
        
        if level == 2:
            if playerName is not None and playerName.strip() != "":
                game = Game(self.window, self.windowX, self.windowY, playerName, self.create_main_menu)
                # Update the level and increase difficulty
                game.currentLevel += 1
                game.levels.increase_level()
                game.start_game()
        
        if level == 3:
            if playerName is not None and playerName.strip() != "":
                game = Game(self.window, self.windowX, self.windowY, playerName, self.create_main_menu)
                game.currentLevel += 2
                game.levels.increase_level()
                game.levels.increase_level()
                game.start_game()


    def show_leaderboard(self):
        self.destroy_all_widgets()

        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/menu.jpg"))
        self.backgroundLabel = Label(self.window, image=self.backgroundImg)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Level selection style
        style = ttk.Style()
        style.configure(
            "LeaderboardsLabel.TLabel",
            font=("Small Fonts", 70),
            foreground="white",
            background="black",
            padding=(20, 20),
            relief="raised",
        )
        levelSelectionLabel = ttk.Label(self.window, text="LEADERBOARDS", style="LeaderboardsLabel.TLabel")
        levelSelectionLabel.pack(side=TOP, pady=40)

        with open("score.txt", "r") as file:
            scores = [line.strip() for line in file.readlines()] # Store the names and scores from the file into list
            scores.sort(key=lambda x: int(x.split(":")[1]), reverse=True) # Take the scores and sort in reverse order
            # Display top 5 scores
            for i, score in enumerate(scores[:5]):
                scoreLabel = Label(self.window, text=f"{i + 1}. {score}", font=("Terminal", 30), fg="black", bg="#ADD8E6")
                scoreLabel.place(x=340, y=280 + i * 50)

        backButton = Button(self.window, text="BACK", command=self.create_main_menu, bg="#2c3e50", fg="black", font=("Terminal", 25))
        backButton.place(x=10, y=10)
    

    def customise_controls(self):
        self.destroy_all_widgets()

        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/menu.jpg"))
        self.backgroundLabel = Label(self.window, image=self.backgroundImg)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        # Customisation style
        style = ttk.Style()
        style.configure(
            "CustomisationLabel.TLabel",
            font=("Small Fonts", 70),
            foreground="white",
            background="black",
            padding=(20, 20),
            relief="raised",
        )
        customisationLabel = ttk.Label(self.window, text="Customise Controls", style="CustomisationLabel.TLabel")
        customisationLabel.pack(side=TOP, pady=40)

        # Keys style
        style = ttk.Style()
        style.configure(
            "KeyLabel.TLabel",
            font=("Terminal", 20),
            foreground="black",
            background="#ADD8E6",
            padding=(5, 5),
            relief="raised",
        )
        leftKeyLabel = ttk.Label(self.window, text="Press a key for Left:", style="KeyLabel.TLabel")
        leftKeyLabel.pack(side=TOP, pady=10)
        leftKeyEntry = Entry(self.window)
        leftKeyEntry.pack(side=TOP, pady=10)

        rightKeyLabel = ttk.Label(self.window, text="Press a key for Right:", style="KeyLabel.TLabel")
        rightKeyLabel.pack(side=TOP, pady=10)
        rightKeyEntry = Entry(self.window)
        rightKeyEntry.pack(side=TOP, pady=10)

        backButton = Button(self.window, text="BACK", command=self.create_main_menu, bg="#2c3e50", fg="black", font=("Terminal", 25))
        backButton.place(x=10, y=10)

         # Fills the entry with the user keyboard input
        self.window.bind("<KeyPress>", lambda event: self.handle_key_input(event, leftKeyEntry, rightKeyEntry))


    def handle_key_input(self, event, leftKeyEntry, rightKeyEntry):
        if leftKeyEntry.get() == "": # Retrieve the user input
            leftKeyEntry.insert(0, event.keysym) # If input in empty wait for next user keyboard click
        elif rightKeyEntry.get() == "" and event.keysym != leftKeyEntry.get():
            rightKeyEntry.insert(0, event.keysym)
        
        # Store the controls selected by user
        with open("controls.txt", "w") as file:
            file.write(f"{leftKeyEntry.get()}\n")
            file.write(f"{rightKeyEntry.get()}\n")
    

    def load_game(self):
        self.destroy_all_widgets()
        # Creates a game object and calls load function which will load data from the json file
        game = Game(self.window, self.windowX, self.windowY, "", self.create_main_menu)
        game.load_game()
    

    def destroy_all_widgets(self):
        # Iterate over any existing widgets and delete them to clear the canvas
        for widget in self.window.winfo_children():
            widget.destroy()


menu = Menu(1280, 720)
menu.window.title("Block Breaker")
menu.window.geometry(f"{menu.windowX}x{menu.windowY}")
menu.window.resizable(False, False) # The screen is fixed to the assigned dimensions
menu.window.mainloop()
