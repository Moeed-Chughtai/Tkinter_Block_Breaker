'''
The paddle class is responible for displaying the paddle and providing movement left and right.
There are also functions for the effect of powerups and cheat codes such as changing the size and speed
of the paddle.
'''

class Paddle:
    
    def __init__(self, canvas, colour, width, height, x, y, speed, paddleId=None):
        self.canvas = canvas
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.paddleId = paddleId
        self.originalWidth = width
        self.powerupTimer = None

    # Draw the paddle onto the canvas with the specified coordinates
    def draw(self):
        x0, y0 = self.x - self.width / 2, self.y - self.height / 2
        x1, y1 = self.x + self.width / 2, self.y + self.height / 2
        if self.paddleId is not None:
            self.canvas.delete(self.paddleId) # Delete existing paddle
        self.paddleId = self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colour)


    def move_left(self):
        if self.x - self.width / 2 > 0:  # Check if paddle has hit left wall
            self.x -= self.speed
            self.canvas.move(self.paddleId, -self.speed, 0)


    def move_right(self):
        if self.x + self.width / 2 < self.canvas.winfo_reqwidth(): # Check if paddle has hit right wall
            self.x += self.speed
            self.canvas.move(self.paddleId, self.speed, 0)


    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.canvas.coords(self.paddleId, x - self.width / 2, y - self.height / 2, x + self.width / 2, y + self.height / 2)


    def get_position(self):
        return self.x, self.y


    def shrink_paddle(self, duration=5):  # Reset after 5 seconds
        self.width //= 2  # Halve the width of the paddle
        self.draw()
        self.start_powerup_timer(duration)


    def increase_speed(self):
        self.speed += 2


    def increase_size(self):
        self.width *= 1.2
        self.draw()


    def start_powerup_timer(self, duration):
        if self.powerupTimer is not None:
            self.canvas.after_cancel(self.powerupTimer)
        self.powerupTimer = self.canvas.after(int(duration * 1000), self.reset_powerup_effect)


    def reset_powerup_effect(self):
        self.width = self.originalWidth
        self.draw()


    # Store to json
    def serialize(self):
        return {
            'colour': self.colour,
            'width': self.width,
            'height': self.height,
            'x': self.x,
            'y': self.y,
            'speed': self.speed,
            'paddleId': self.paddleId,
        }


    # Load from json
    @classmethod
    def deserialize(cls, data, canvas):
        return cls(
            canvas=canvas,
            colour=data['colour'],
            width=data['width'],
            height=data['height'],
            x=data['x'],
            y=data['y'],
            speed=data['speed'],
            paddleId=data['paddleId'],
        )
