import math

class Ball:

    def __init__(self, canvas, colour, x, y, size, speed):
        self.canvas = canvas
        self.colour = colour
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.ballId = None
        self.dx = self.speed
        self.dy = -self.speed

    def draw(self):
        x0, y0 = self.x - self.size, self.y - self.size
        x1, y1 = self.x + self.size, self.y + self.size
        self.ballId = self.canvas.create_oval(x0, y0, x1, y1, fill=self.colour)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.canvas.move(self.ballId, self.dx, self.dy)
    
    def check_paddle_collision(self, paddle):
        ballX, ballY = self.get_position()
        paddleX, paddleY = paddle.get_position()
        if (
            paddleX - paddle.width / 2 < ballX < paddleX + paddle.width / 2
            and paddleY - paddle.height / 2 < ballY < paddleY + paddle.height / 2
        ):
            relative_position = (ballX - paddleX) / (paddle.width / 2)
            max_reflection_angle = math.radians(60) # Set the maximum angle for reflection (in radians)
            reflection_angle = relative_position * max_reflection_angle # Calculate the new angle based on the relative position
            # Calculate new velocities using trigonometry
            self.dx = self.speed * math.sin(reflection_angle)
            self.dy = -self.speed * math.cos(reflection_angle)
    
    def check_wall_collision(self, windowX):
        ballX, ballY = self.get_position()

        # Check if the ball hits the left or right wall
        if ballX - self.size <= 0 or ballX + self.size >= windowX:
            incidence_angle = math.atan2(self.dy, self.dx)
            reflection_angle = math.pi - incidence_angle
            # Calculate new velocities using trigonometry
            self.dx = self.speed * math.cos(reflection_angle)
            self.dy = self.speed * math.sin(reflection_angle)

        # Check if the ball hits the top wall
        if ballY - self.size <= 0:
            reflection_angle = -math.atan2(self.dy, self.dx)
            # Calculate new velocities using trigonometry
            self.dx = self.speed * math.cos(reflection_angle)
            self.dy = self.speed * math.sin(reflection_angle)
    
    def get_position(self):
        return self.x, self.y
