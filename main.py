from tkinter import *
from PIL import ImageTk, Image
from game import Game

class Menu:
    def __init__(self, windowX, windowY):
        self.window = Tk()
        self.windowX = windowX
        self.windowY = windowY
        # Load and display image as background
        self.backgroundImg = ImageTk.PhotoImage(Image.open("menu.jpg"))
        self.background_label = Label(self.window, image=self.backgroundImg)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create and configure Play button
        play_button_font = ("Helvetica", 30)
        self.play_button = Button(self.window, text="Play", command=self.start_game, bg="#4CAF50", fg="white", font=play_button_font)
        self.play_button.pack(side=TOP, pady=20)

        # Create and configure Levels button
        levels_button_font = ("Helvetica", 30)
        self.levels_button = Button(self.window, text="Levels", command=self.levels_action, bg="#3498db", fg="white", font=levels_button_font)
        self.levels_button.pack(side=TOP, pady=20)

        # Create and configure Settings button
        settings_button_font = ("Helvetica", 30)
        self.settings_button = Button(self.window, text="Settings", command=self.settings_action, bg="#e74c3c", fg="white", font=settings_button_font)
        self.settings_button.pack(side=TOP, pady=20)

        # Create and configure Exit button
        exit_button_font = ("Helvetica", 30)
        self.exit_button = Button(self.window, text="Exit", command=self.window.destroy, bg="#808080", fg="white", font=exit_button_font)
        self.exit_button.pack(side=TOP, pady=20)

    def start_game(self):
        self.background_label.destroy()
        self.play_button.destroy()
        self.levels_button.destroy()
        self.settings_button.destroy()
        self.exit_button.destroy()
        game = Game(self.window, self.windowX, self.windowY)
        game.start_game()

    def levels_action(self):
        print("Levels button clicked")

    def settings_action(self):
        print("Settings button clicked")


if __name__ == "__main__":
    menu = Menu(1100, 700)
    menu.window.title("Block Breaker")
    menu.window.geometry(f"{menu.windowX}x{menu.windowY}")
    menu.window.mainloop()
