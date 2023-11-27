'''
The block class is responsible for provinding a blueprint for moving and non-moving block objects.
The draw function will display the block on the canvas. The collision detection chencks if a ball overlaps the block
and if it is a hit, the direction of the ball changes. The block changes colour or is deleted from the canvas.
For the moving blocks, the move function will move the blocks from one side to the other and then back.
'''

class Block:

    def __init__(self, canvas, topLeftX, topLeftY, bottomRightX, bottomRightY, currentColour, speed=None, blockId=None):
        self.canvas = canvas
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY
        self.blockId = blockId
        self.speed = speed
        self.hits = 0
        self.colours = {1: "green", 2: "orange", 3: "red"}
        self.currentColour = currentColour

    # Draw the block to the canvas with the specified position
    def draw(self):
        self.blockId = self.canvas.create_rectangle(self.topLeftX, self.topLeftY, self.bottomRightX, 
                        self.bottomRightY, outline="black", fill=self.colours.get(self.currentColour), width=2)
    

    def check_collision(self, ball):
        ballX, ballY = ball.get_position()
        # Check if the ball hits the block
        if (
            self.topLeftX <= ballX <= self.bottomRightX 
            and self.topLeftY <= ballY <= self.bottomRightY
        ):
            return True
        return False
    

    def hit(self, ball):
        # Change direction of the ball
        ball.dy = -ball.dy
        if self.speed == None:
            self.canvas.delete(self.blockId)
            if self.currentColour == 3:
                return True
            else:
                self.currentColour += 1 # Advance to next colour
                self.draw()
                return False
    
    
    def move(self):
        if self.speed is not None:
            # Move the block by adding to its coordinates every 5 milliseconds
            self.topLeftX += self.speed
            self.bottomRightX += self.speed
            if self.bottomRightX >= self.canvas.winfo_reqwidth() or self.topLeftX <= 0:
                self.speed *= -1 # Reverse the direction if it reaches one of the ends
            self.canvas.coords(self.blockId, self.topLeftX, self.topLeftY, self.bottomRightX, self.bottomRightY)

    # Store data to json
    def serialize(self):
        return {
            'topLeftX': self.topLeftX,
            'topLeftY': self.topLeftY,
            'bottomRightX': self.bottomRightX,
            'bottomRightY': self.bottomRightY,
            'currentColour': self.currentColour,
            'speed': self.speed,
            'blockId': self.blockId,
        }


    # Load data from json
    @classmethod
    def deserialize(cls, data, canvas):
        return cls(
            canvas=canvas,
            topLeftX=data['topLeftX'],
            topLeftY=data['topLeftY'],
            bottomRightX=data['bottomRightX'],
            bottomRightY=data['bottomRightY'],
            currentColour=data['currentColour'],
            speed=data['speed'],
            blockId=data['blockId'],
        )
