'''
Background Image Ref: https://wallpapers.com/4k-space
Icon Images Ref: https://www.flaticon.com/

This is the main Game class and handles all the game mechanics. First, the canvas is created and the blocks are displayed.
Then there is the main update function that is called regularly that controls the movement, collisions and powerups.
If the game has not yet started or is paused (space key), the function stops the movement updates. There is also a toggle for a 
boss key which pauses the game when B is pressed and displays an image on top and then unpauses when B is pressed again.
There is also logic for starting the next level by making the game more difficult and logic for ending the game which
displays a scree with the users score and the leaderboards with the top 5 scores. There are also cheat codes which make the paddle
faster, make the paddle bigger and the ball slower. The final logic is to store and load the current state of the game by using a
json file.

'''

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import json
from block import Block
from ball import Ball
from paddle import Paddle
from powerups import PowerUp
from levels import Levels

class Game:

    def __init__(self, window, windowX, windowY, playerName, mainMenuCallback):
        self.window = window
        self.windowX = windowX
        self.windowY = windowY
        self.mainMenuCallback = mainMenuCallback
        self.canvas = Canvas(self.window, width=self.windowX, height=self.windowY)
        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/background.jpg").resize((self.windowX, self.windowY)))
        self.playerName = playerName
        self.blocks = []
        self.ball = Ball(self.canvas, "white", windowX // 2, windowY // 2, 10, 4)
        self.paddle = Paddle(self.canvas, "white", 190, 20, windowX // 2, windowY - 30, 8)
        self.levels = Levels(self.ball, self.paddle)
        self.balls = [self.ball]
        self.currentLevel = 1
        self.movingBlocks = []
        self.blocksToRemove = []
        self.score = 0
        self.paused = True
        self.gameStarted = False
        self.levelChange = False
        self.startMsg = None
        self.powerups = []
        self.bossKeyActive = False
        self.bossKeyImg = ImageTk.PhotoImage(Image.open("images/bossKey.png").resize((self.windowX, self.windowY)))
        self.bossKeyImageId = None
        self.saveButton = Button(self.window, text="Save", command=self.save_game, bg="red", fg="white", font=("Terminal", 16), width=4)
        self.saveButton.place(x=self.windowX - 70, y=self.windowY - 55)
        self.powerupTimerInterval = 10000
        self.start_powerup_timer()
        
    
    def setup(self):
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.backgroundImg) # Set background of canvas as an image
        
        # Score style
        style = ttk.Style()
        style.configure(
            "ScoreLabel.TLabel",
            font=("Terminal", 20),
            foreground="white",
            background="black",
            padding=(5, 5),
            relief="raised",
        )
        self.scoreLabel = ttk.Label(self.window, text="Score: 0", style="ScoreLabel.TLabel")
        self.scoreLabel.place(x=10, y=self.windowY - 50)
        self.canvas.create_rectangle(5, 5, self.windowX - 5, self.windowY - 5, outline="red", width=2)


    def display_blocks(self):
        xGap = self.windowX / 6 # Split the horizontal length into 6 blocks
        yGap = 80
        topLeftX, topLeftY = 0, 0

        for _ in range(3): # 3 iterations of 6 blocks
            for _ in range(6):
                # Add to the x and y before adding next block
                bottomRightX = topLeftX + xGap
                bottomRightY = topLeftY + yGap
                block = Block(self.canvas, topLeftX, topLeftY, bottomRightX, bottomRightY, 1)
                self.blocks.append(block)
                block.draw()
                topLeftX += xGap
            # Reset to left side and add to vertical length to start next row
            topLeftX = 0
            topLeftY += yGap
        
        for _ in range(self.currentLevel): # The number of moving blocks depends on the current level
            topLeftY = random.randint(280, 450)
            movingBlock = Block(self.canvas, 0, topLeftY, 80, topLeftY + 40, 1, random.uniform(1, 4))
            while self.check_collision_with_existing_blocks(movingBlock): # Check overlap
                topLeftY = random.randint(280, 450)
                movingBlock = Block(self.canvas, 0, topLeftY, 80, topLeftY + 40, 1, random.uniform(1, 4))
            self.movingBlocks.append(movingBlock)
            movingBlock.draw()


    def check_collision_with_existing_blocks(self, block):
        # When there are multiple moving blocks, ensure they are not overlapping
        for movingBlock in self.movingBlocks:
            if (
                block.topLeftX < movingBlock.bottomRightX
                and block.bottomRightX > movingBlock.topLeftX
                and block.topLeftY < movingBlock.bottomRightY
                and block.bottomRightY > movingBlock.topLeftY
            ):
                return True # If the blocks are not overlapping
        return False


    # Main game function
    def update(self):
        if self.gameStarted and not self.paused: # Only update if game started and not paused
            for ball in self.balls:
                ball.move()
                
                # If there are multiple balls, delete them once they hit the bottom
                if len(self.balls) != 1:
                    ballY = ball.get_position()[1]
                    if ballY >= self.windowY:
                        self.balls.remove(ball)
                        self.canvas.delete(ball.ballId)
                
                ball.check_paddle_collision(self.paddle)
                ball.check_wall_collision(self.windowX)

            # Check collision of every ball with every block
            for block in self.blocks:
                for ball in self.balls:
                    if block.check_collision(ball):
                        if block.hit(ball):
                            if block not in self.blocksToRemove:
                                self.blocksToRemove.append(block)
                        self.score += 1
            
            # Check collsion of every ball with every moving block
            for block in self.movingBlocks:
                block.move()
                for ball in self.balls:
                    if block.check_collision(ball):
                        block.hit(ball)

            # Check if ball hits the ground
            if len(self.balls) == 1:
                self.check_ball_missed()

            # Check if no blocks are left
            if len(self.blocks) == 0:
                self.end_level()

            # Check if ball collides with powerup
            for powerup in self.powerups:
                if powerup.check_collision(self.ball):
                    result = powerup.activate_powerup()
                    powerup.remove_powerup()
                    if result != None:
                        # If the powerup selected is multiple balls
                        for ball in result:
                            self.balls.append(ball)

            if not any(powerup.active for powerup in self.powerups):
                self.display_powerups()
            
            # Destroyed blocks that need removing
            for block in self.blocksToRemove:
                self.blocks.remove(block)
            self.blocksToRemove = []

            self.scoreLabel.config(text=f"Score: {self.score}")
        
        if not self.levelChange:
            self.window.after(5, self.update) # Call the the update function every 5 milliseconds
    
    
    def check_ball_missed(self):
        for ball in self.balls:
            ballY = ball.get_position()[1]
            # Check if the balls vertical length is bigger than the window
            if ballY >= self.windowY:
                    self.end_game()


    def display_powerups(self):
         for _ in range(random.randint(1, 3)): # Display between 1 and 3 powerups
            powerup = PowerUp(self.canvas, self.paddle, self.ball, random.choice(["MultipleBalls", "SlowMotion", "ShrinkPaddle", "SpeedUpBall"]))
            # Random positions
            powerup.x = random.randint(50, 550)
            powerup.y = random.randint(250, 500)
            # Function that displays the powerup
            powerup.create_powerup()
            self.powerups.append(powerup)


    def start_powerup_timer(self):
        if self.gameStarted and not self.paused:
            # Schedule the display_powerups method to be called at random intervals
            self.powerupTimerInterval = random.randint(5000, 15000)  # Random interval between 5 and 15 seconds
            self.window.after(self.powerupTimerInterval, self.display_powerups)
            self.window.after(self.powerupTimerInterval, self.start_powerup_timer)


    def bind_controls(self):
        with open("controls.txt") as file:
            left = file.readline()
            right = file.readline()

        # Bind the users selected controls to the left and right
        self.window.bind("<"+left+">", lambda event: self.paddle.move_left())
        self.window.bind("<"+right+">", lambda event: self.paddle.move_right())
        self.window.bind("<space>", self.toggle_pause)
        self.window.bind("b", self.toggle_boss_key)
        # Cheat codes
        self.window.bind("<Control_L>c", self.handle_cheat_codes)
        self.window.bind("<Control_L>d", self.handle_cheat_codes)
        self.window.bind("<Control_L>s", self.handle_cheat_codes)
    

    def toggle_boss_key(self, event):
        # Toggles pause
        self.paused = not self.paused
        if not self.paused:
            # Toggles boss key and resumes is not active
            if not self.bossKeyActive:
                self.update(event)
            self.resume_game()
            self.update(event)
        else:
            self.show_boss_key()


    def show_boss_key(self):
        self.bossKeyActive = True
        self.paused = True # Pause game
        self.bossKeyImageId = self.canvas.create_image(0, 0, anchor=NW, image=self.bossKeyImg) # Display image on top of game
        self.scoreLabel.place_forget()
        self.saveButton.place_forget()
        

    def resume_game(self):
        self.bossKeyActive = False
        self.paused = False
        self.canvas.delete(self.bossKeyImageId) # Delete the boss key image
        self.scoreLabel.place(x=10, y=self.windowY - 60)
        self.saveButton.place(x=self.windowX - 70, y=self.windowY - 55)
    

    def toggle_pause(self, event):
        self.paused = not self.paused
        if not self.paused:
            self.update(event)


    def toggle_game(self, event):
        self.gameStarted = True
        self.paused = False
        self.startMsg.destroy() # Once game starts destroy the msg


    def end_level(self):
        self.paused = True
        self.gameStarted = False
        self.levelChange = True
        self.currentLevel += 1
        self.score = 0
        self.canvas.delete("all")  # Clear the canvas
        self.levels.increase_level() # Increase difficulty
        self.ball.set_position(self.windowX // 2, self.windowY // 2) # Reset ball
        self.paddle.set_position(self.windowX // 2, self.windowY - 30) # Reset paddle
        self.start_game()


    def end_game(self):
        self.paused = True
        self.movingBlocks = []
        # Clear the canvas
        for widget in self.window.winfo_children():
            widget.destroy()

        # Display image as new background
        self.backgroundImg = ImageTk.PhotoImage(Image.open("images/leaderboard.jpg"))
        self.backgroundLabel = Label(self.window, image=self.backgroundImg)
        self.backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        #Game over style
        style = ttk.Style()
        style.configure(
            "gameOverLabel.TLabel",
            font=("Small Fonts", 70),
            foreground="white",
            background="black",
            padding=(20, 20),
            relief="raised",
        )
        gameOverLabel = ttk.Label(self.window, text="GAME OVER", style="gameOverLabel.TLabel")
        gameOverLabel.pack(side=TOP, pady=10)

        # Your score style
        style2 = ttk.Style()
        style2.configure(
            "yourScoreLabel.TLabel",
            font=("Terminal", 20),
            foreground="black",
            background="#2c3e50",
            padding=(5, 5),
            relief="raised",
        )
        yourScoreLabel = ttk.Label(self.window, text=f"Your Score: {self.score}", style="yourScoreLabel.TLabel")
        yourScoreLabel.pack(side=TOP, pady=20)
        
        # Store user name and scorew
        with open("score.txt", "a") as f:
            f.write(f"{self.playerName}: {self.score}\n")
        self.display_leaderboard()


    def display_leaderboard(self):    
        # Leaderboards style
        style = ttk.Style()
        style.configure(
            "leaderboardLabel.TLabel",
            font=("Small Fonts", 60),
            foreground="white",
            background="black",
            padding=(5, 5),
            relief="raised",
        )
        leaderboardLabel = ttk.Label(self.window, text="Leaderboard", style="leaderboardLabel.TLabel")
        leaderboardLabel.pack(side=TOP, pady=20)
        
        with open("score.txt", "r") as file:
            scores = [line.strip() for line in file.readlines()] # Store the name and scores in a list
            scores.sort(key=lambda x: int(x.split(":")[1]), reverse=True) # Take the scores and sort them in reverse order

            for i, score in enumerate(scores[:5]): # Display top 5 scores
                # Score style
                style2 = ttk.Style()
                style2.configure(
                    "scoreLabel.TLabel",
                    font=("Terminal", 23),
                    foreground="black",
                    background="#ADD8E6",
                    padding=(5, 5),
                    relief="raised",
                )
                scoreLabel = ttk.Label(self.window, text=f"{i + 1}. {score}", style="scoreLabel.TLabel")
                scoreLabel.place(x=440, y=425 + i * 45)

        # Return to main menu
        mainMenuButton = Button(self.window, text="Main Menu", command=self.mainMenuCallback, bg="#2c3e50", fg="black", font=("Terminal", 25))
        mainMenuButton.place(x=10, y=10)


    def handle_cheat_codes(self, event):
        if event.keysym == "c" and event.state == 4: # Check for Ctrl+C combination
            self.paddle.increase_speed()
        elif event.keysym == "d" and event.state == 4: # Check for Ctrl+D combination
            self.ball.decrease_speed()
        elif event.keysym == "s" and event.state == 4: # Check for Ctrl+S combination
            self.paddle.increase_size()


    def save_game(self):
        # Save the current states of all the attributes of the class
        game_state = {
            'playerName': self.playerName,
            'blocks': [block.serialize() for block in self.blocks],
            'ball': self.ball.serialize(),
            'paddle': self.paddle.serialize(),
            'balls': [ball.serialize() for ball in self.balls],
            'currentLevel': self.currentLevel,
            'movingBlocks': [block.serialize() for block in self.movingBlocks],
            'score': self.score,
        }

        # Store into a json file
        with open("save.json", "w") as file:
            json.dump(game_state, file)
        
        # Return to main menu
        self.mainMenuCallback()


    def load_game(self):
        with open("save.json", "r") as file:
            game_state = json.load(file)

        # Restore game state
        self.playerName = game_state['playerName']
        self.blocks = [Block.deserialize(block_data, self.canvas) for block_data in game_state['blocks']]
        self.ball = Ball.deserialize(game_state['ball'], self.canvas)
        self.paddle = Paddle.deserialize(game_state['paddle'], self.canvas)
        self.balls = [Ball.deserialize(ball_data, self.canvas) for ball_data in game_state['balls']]
        self.currentLevel = game_state['currentLevel']
        self.movingBlocks = [Block.deserialize(block_data, self.canvas) for block_data in game_state['movingBlocks']]
        self.score = game_state['score']
        
        # Continue the game
        self.gameStarted = True
        self.paused = False
        self.setup()
        for block in self.blocks:
            block.draw()
        for movingBlock in self.movingBlocks:
            movingBlock.draw()
        for ball in self.balls:
            ball.draw()
        self.paddle.draw()
        self.powerups = []
        self.bind_controls()
        self.update()
        self.window.mainloop()


    def start_game(self):
        self.levelChange = False
        # Display everything on the canvas
        self.setup()
        self.display_blocks()
        for ball in self.balls:
            ball.draw()
        self.paddle.draw()
        self.bind_controls()
        # Call the main game loop
        self.update()

        # Wait for return to be clicked to start game
        self.startMsg = Label(self.window, text="Press RETURN to play", font=("Terminal", 32), fg="white", bg="#A9A9A9")
        self.startMsg.place(x=320, y=400)
        self.window.bind("<Return>", self.toggle_game)
        self.start_powerup_timer()  # Start the power-up timer when the game begins

        self.window.mainloop()
