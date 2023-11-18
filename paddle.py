class Paddle:
    
    def __init__(self, canvas, colour, width, height, x, y, speed):
        self.canvas = canvas
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = speed
        self.paddle_id = None

    def draw(self):
        x0, y0 = self.x - self.width / 2, self.y - self.height / 2
        x1, y1 = self.x + self.width / 2, self.y + self.height / 2
        self.paddle_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.colour)

    def move_left(self):
        self.x -= self.speed
        self.canvas.move(self.paddle_id, -self.speed, 0)

    def move_right(self):
        self.x += self.speed
        self.canvas.move(self.paddle_id, self.speed, 0)

    def get_position(self):
        return self.x, self.y
