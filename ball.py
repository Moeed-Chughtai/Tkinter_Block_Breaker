'''
The ball class provides a blueprint for all ball objects. The draw function will display the ball on the canvas.
The collision detection checks for collision with the paddle and wall. The consequence of the collision is calculated
using pythagoras to give a realistic effect. Then, there are functions for the effect of powerups such as slowing or
speeding up the ball.
'''

import math
import random

class Ball:

    def __init__(self, canvas, colour, x, y, size, speed, ballId=None):
        self.canvas = canvas
        self.colour = colour
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.ballId = ballId
        self.dx = self.speed
        self.dy = -2
        self.slowMotionFactor = 0.75
        self.powerupTimer = None
        self.newBalls = []
        self.originalSpeed = self.speed


    # Draw the ball onto the canvas with the specified coordinates
    def draw(self):
        x0, y0 = self.x - self.size, self.y - self.size
        x1, y1 = self.x + self.size, self.y + self.size
        self.ballId = self.canvas.create_oval(x0, y0, x1, y1, fill=self.colour)


    def move(self):
        # Add to the x and y in the direction the ball is moving
        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.ballId, self.dx, self.dy)
    

    def check_paddle_collision(self, paddle):
        ballX, ballY = self.get_position()
        paddleX, paddleY = paddle.get_position()
        # Check collision of paddle and ball by seeing if their positions overlap
        if (
            paddleX - paddle.width / 2 < ballX < paddleX + paddle.width / 2
            and paddleY - paddle.height / 2 < ballY < paddleY + paddle.height / 2
        ):  
            relative_position = (ballX - paddleX) / (paddle.width / 2)
            maxReflectionAngle = math.radians(60) # Set the maximum angle for reflection in radians
            reflectionAngle = relative_position * maxReflectionAngle # Calculate the new angle based on the relative position
            reflectionAngle = max(-maxReflectionAngle, min(reflectionAngle, maxReflectionAngle))
            # Calculate new velocities using trigonometry
            self.dx = self.speed * math.sin(reflectionAngle)
            self.dy = -self.speed * math.cos(reflectionAngle)
    

    def check_wall_collision(self, windowX):
        ballX, ballY = self.get_position()

        # Check if the ball hits the left or right wall
        if ballX - self.size <= 0 or ballX + self.size >= windowX:
            incidence_angle = math.atan2(self.dy, self.dx)
            reflectionAngle = math.pi - incidence_angle
            # Calculate new velocities using trigonometry
            self.dx = self.speed * math.cos(reflectionAngle)
            self.dy = self.speed * math.sin(reflectionAngle)

        # Check if the ball hits the top wall
        if ballY - self.size <= 0:
            reflectionAngle = -math.atan2(self.dy, self.dx)
            self.dx = self.speed * math.cos(reflectionAngle)
            self.dy = self.speed * math.sin(reflectionAngle)
    

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.ballId, x - self.size, y - self.size, x + self.size, y + self.size)


    def get_position(self):
        return self.x, self.y
    

    def split_ball(self):
        angle = random.uniform(0, 2 * math.pi)  # Random angle in radians
        # Set the dx and dy for the new ball
        dx = self.speed * math.cos(angle)
        dy = -self.speed * math.sin(angle)
        newBall = Ball(self.canvas, self.colour, self.x, self.y, self.size, self.speed)
        newBall.dx = dx
        newBall.dy = dy
        return newBall


    def slow_motion(self, duration=5): # Reset after 5 seconds
        self.originalSpeed = self.speed
        self.speed *= self.slowMotionFactor # Decrease speed by defined factor
        self.start_powerupTimer(duration)


    def speed_up_ball(self, duration=5):
        self.originalSpeed = self.speed
        self.speed *= 1.5 # Increase speed by defined factor
        self.start_powerupTimer(duration)

    
    def decrease_speed(self):
        self.speed -= 1.2


    def start_powerupTimer(self, duration):
        if self.powerupTimer is not None:
            self.canvas.after_cancel(self.powerupTimer)
        self.powerupTimer = self.canvas.after(int(duration * 1000), self.reset_powerup_effect)


    def reset_powerup_effect(self):
        self.speed = self.originalSpeed  # Reset speed to its original value


    # Store to json
    def serialize(self):
        return {
            'colour': self.colour,
            'x': self.x,
            'y': self.y,
            'speed': self.speed,
            'size': self.size,
            'ballId': self.ballId
        }


    # Load from json
    @classmethod
    def deserialize(cls, data, canvas):
        return cls(
            canvas=canvas,
            colour=data['colour'],
            x=data['x'],
            y=data['y'],
            speed=data['speed'],
            size=data['size'],
            ballId=data['ballId'],
        )
