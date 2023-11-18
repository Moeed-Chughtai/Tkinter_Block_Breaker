from tkinter import *
from PIL import ImageTk, Image
from block import Block
from ball import Ball
from paddle import Paddle

class Game:

    def __init__(self, window, windowX, windowY):
        self.window = window
        self.windowX = windowX
        self.windowY = windowY
        self.canvas = Canvas(self.window, width=self.windowX, height=self.windowY)
        self.backgroundImg = ImageTk.PhotoImage(Image.open("background.jpg")) # Loads img
        self.blocks = []
        self.ball = Ball(self.canvas, "white", windowX // 2, windowY // 2, 10, 3)
        self.paddle = Paddle(self.canvas, "black", 150, 20, windowX // 2, windowY - 30, 8)
        self.score = 0
        self.paused = False
        
    def setup(self):
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.backgroundImg) # Set background of canvas as an image
        self.scoreLabel = Label(self.window, text="Score: 0", font=("Helvetica", 16), fg="white", bg="black")
        self.scoreLabel.place(x=10, y=self.windowY - 60)
        self.canvas.create_rectangle(5, 5, self.windowX - 5, self.windowY - 5, outline="red", width=2)

    def display_blocks(self):
        xGap = self.windowX / 6
        yGap = 80
        topLeftX, topLeftY = 0, 0

        for _ in range(3):
            for _ in range(6):
                bottomRightX = topLeftX + xGap
                bottomRightY = topLeftY + yGap
                block = Block(self.canvas, topLeftX, topLeftY, bottomRightX, bottomRightY)
                self.blocks.append(block)
                block.draw()
                topLeftX += xGap
            topLeftX = 0
            topLeftY += yGap

    def update(self):
        if not self.paused:
            self.ball.move()
            self.ball.check_paddle_collision(self.paddle)
            self.ball.check_wall_collision(self.windowX)

            blocks_to_remove = []
            for block in self.blocks:
                if block.check_collision(self.ball):
                    if block.hit(self.ball):
                        blocks_to_remove.append(block)
                    self.score += 1

            for block in blocks_to_remove:
                self.blocks.remove(block)

            self.scoreLabel.config(text=f"Score: {self.score}")
        self.window.after(10, self.update)

    def bind_controls(self):
        self.window.bind("<Left>", lambda event: self.paddle.move_left())
        self.window.bind("<Right>", lambda event: self.paddle.move_right())
        self.window.bind("<space>", self.toggle_pause)
    
    def toggle_pause(self, event):
        self.paused = not self.paused
        if not self.paused:
            self.update()

    def start_game(self):
        self.setup()
        self.display_blocks()
        self.ball.draw()
        self.paddle.draw()
        self.bind_controls()
        self.update()
        self.window.mainloop()
