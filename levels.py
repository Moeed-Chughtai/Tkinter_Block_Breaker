'''
Levels class necessary for updating the difficulty for the next level.
'''

class Levels:
    
    def __init__(self, ball, paddle):
        self.ball = ball
        self.paddle = paddle


    def increase_level(self):
        self.paddle.width //= 1.2 # Reduce paddle width
        self.paddle.speed += 2 # Increase paddle speed
        self.ball.speed += 1.2 # Increase ball speed
