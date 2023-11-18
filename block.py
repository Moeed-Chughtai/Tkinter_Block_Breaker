import math

class Block:

    def __init__(self, canvas, topLeftX, topLeftY, bottomRightX, bottomRightY):
        self.canvas = canvas
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.blockId = None
        self.hits = 0
        self.colours = {1: "green", 2: "orange", 3: "red"}
        self.currentColour = 1

    def draw(self):
        self.blockId = self.canvas.create_rectangle(self.topLeftX, self.topLeftY, self.bottomRightX, 
                        self.bottomRightY, outline="black", fill=self.colours.get(self.currentColour), width=2)
    
    def check_collision(self, ball):
        # Check if the ball hits the block
        ballX, ballY = ball.get_position()
        if (
            self.topLeftX <= ballX <= self.bottomRightX 
            and self.topLeftY <= ballY <= self.bottomRightY
        ):
            return True
        return False
    
    def hit(self, ball):
        self.canvas.delete(self.blockId)

        if self.currentColour == 3:
            angle_of_incidence = math.atan2(ball.dy, ball.dx)
            # Reflect the ball based on the angle of incidence
            new_angle = math.pi - angle_of_incidence
            ball.dx = ball.speed * math.cos(new_angle)
            ball.dy = ball.speed * math.sin(new_angle)
            return True
        else:
            self.currentColour += 1
            self.draw()
            angle_of_incidence = math.atan2(ball.dy, ball.dx)
            # Reflect the ball based on the angle of incidence
            new_angle = math.pi - angle_of_incidence
            ball.dx = ball.speed * math.cos(new_angle)
            ball.dy = ball.speed * math.sin(new_angle)
            return False
