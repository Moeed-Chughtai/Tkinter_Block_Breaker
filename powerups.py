'''
The PowerUp class defines the powerups and powerdowns in the game. There are 2 powerups: MultipleBalls and SlowMotions and
2 powerdowns: ShrinkPaddle and SpeedUpBall. These are created at random positions on the canvas as images and change
every 10 seconds. The collision detection checks for the ball hitting the images and if detected, activates the powerup.
'''

from tkinter import PhotoImage
import random

class PowerUp:
    
    def __init__(self, canvas, paddle, ball, powerType, id=None):
        self.canvas = canvas
        self.paddle = paddle
        self.ball = ball
        self.powerType = powerType
        self.id = id
        self.active = False
        self.imagePaths = {
            "MultipleBalls": "images/multiple.png",
            "SlowMotion": "images/slower.png",
            "ShrinkPaddle": "images/smaller.png",
            "SpeedUpBall": "images/faster.png",
        }
        self.imagePath = self.imagePaths[powerType]
        self.image = PhotoImage(file=self.imagePath)
        self.imageWidth = 40
        self.imageHeight = 40
        self.image = self.image.subsample(int(self.image.width() / self.imageWidth), int(self.image.height() / self.imageHeight))


    def create_powerup(self):
        # Random coordinates
        x = random.randint(50, 1230)
        y = random.randint(280, 650)
        self.id = self.canvas.create_image(x, y, anchor="center", image=self.image)
        self.active = True
        self.canvas.after(10000, self.remove_powerup) # Remove after 10 secs


    def remove_powerup(self):
        if self.active:
            self.canvas.delete(self.id)
            self.active = False


    def activate_powerup(self):
        if self.active:
            if self.powerType == "MultipleBalls":
                newBalls = [self.ball.split_ball() for _ in range(3)] # Generate 3 new balls
                for ball in newBalls: # Display the 3 balls
                    ball.draw()
                    self.canvas.move(ball.ballId, 0, -10)
                return newBalls
            elif self.powerType == "SlowMotion":
                self.ball.slow_motion()
            elif self.powerType == "ShrinkPaddle":
                self.paddle.shrink_paddle()
            elif self.powerType == "SpeedUpBall":
                self.ball.speed_up_ball()
            self.canvas.delete(self.id)
            self.active = False


    def check_collision(self, ball):
        try:
            powerupX, powerupY = self.canvas.coords(self.id)
        except ValueError: # Handle the case where the power-up has been deleted or not placed on the canvas
            return False

        ballX, ballY = ball.get_position()
        distance = ((powerupX - ballX) ** 2 + (powerupY - ballY) ** 2) ** 0.5 # Calculate distance between the ball and image
        return distance < (ball.size + max(self.imageWidth, self.imageHeight) / 2) # Check if they overlap

    
    # Store to json
    def serialize(self):
        return {
            'powerType': self.powerType,
            'id': self.id,
        }


    # Load from json
    @classmethod
    def deserialize(cls, data, canvas, paddle, ball):
        return cls(
            canvas=canvas,
            paddle=paddle,
            ball=ball,
            powerType=data['powerType'],
            id=data['id'],
        )
