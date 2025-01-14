import tkinter as tk
import random

# Tetromino shapes
shapes = {
    'O': ['56a9', '6a95', 'a956', '956a'],
    'I': ['4567', '26ae', 'ba98', 'd951'],
    'J': ['0456', '2159', 'a654', '8951'],
    'L': ['2654', 'a951', '8456', '0159'],
    'T': ['1456', '6159', '9654', '4951'],
    'Z': ['0156', '2659', 'a954', '8451'],
    'S': ['1254', 'a651', '8956', '0459'],
}

class TetrisPiece:
    def __init__(self, shape, x=0, y=0, rot=0):
        self.shape = shape
        self.x = x
        self.y = y
        self.rot = rot

    def get_blocks(self):
        """Return the block coordinates for the current piece based on its rotation and position."""
        for char in shapes[self.shape][self.rot % 4]:
            y, x = divmod(int(char, 16), 4)
            yield self.x + x, self.y - y

    def move(self, dx=0, dy=0, drot=0):
        """Move or rotate the Tetromino."""
        self.x += dx
        self.y += dy
        self.rot = (self.rot + drot) % 4

class TetrisGrid:
    def __init__(self, width=10, height=16):
        self.width = width
        self.height = height
        self.grid = [[''] * width for _ in range(height)]

    def clear_full_rows(self):
        cleared_rows = 0
        self.grid = [row for row in self.grid if any(cell == '' for cell in row)]
        cleared_rows = self.height - len(self.grid)
        self.grid = [[''] * self.width for _ in range(cleared_rows)] + self.grid
        return cleared_rows

    def piece_fits(self, piece):
        """Check if the piece fits in the grid."""
        for x, y in piece.get_blocks():
            if not (0 <= x < self.width) or not (0 <= y < self.height) or self.grid[y][x]:
                return False
        return True

    def place_piece(self, piece):
        """Place the piece on the grid."""
        for x, y in piece.get_blocks():
            self.grid[y][x] = piece.shape

class StepTetrisGame:
    def __init__(self, root):
        self.grid = TetrisGrid()
        self.piece = self.get_next_piece()
        self.score = 0  # Initialize score

        # Set up Tkinter window
        self.root = root
        self.root.title("Step-by-Step Tetris")

        self.canvas = tk.Canvas(root, width=300, height=480)
        self.canvas.pack()

        # Label to display the score
        self.score_label = tk.Label(root, text=f"Score: {self.score}")
        self.score_label.pack()

        # Buttons for controls
        btn_frame = tk.Frame(root)
        btn_frame.pack()

        tk.Button(btn_frame, text="Left", command=self.move_left).grid(row=0, column=0)
        tk.Button(btn_frame, text="Right", command=self.move_right).grid(row=0, column=1)
        tk.Button(btn_frame, text="Rotate", command=self.rotate_piece).grid(row=0, column=2)
        tk.Button(btn_frame, text="Step Down", command=self.step_down).grid(row=0, column=3)
        tk.Button(btn_frame, text="Drop", command=self.drop_piece).grid(row=0, column=4)
        tk.Button(btn_frame, text="Reset", command=self.reset_game).grid(row=1, column=2)

        self.update_display()

    def get_next_piece(self):
        shape = random.choice(list(shapes.keys()))
        return TetrisPiece(shape, x=4, y=1)  # Start the piece at y=1 instead of y=0

    def move_left(self):
        self.piece.move(dx=-1)
        if not self.grid.piece_fits(self.piece):
            self.piece.move(dx=1)  # Undo the move
        self.update_display()

    def move_right(self):
        self.piece.move(dx=1)
        if not self.grid.piece_fits(self.piece):
            self.piece.move(dx=-1)  # Undo the move
        self.update_display()

    def rotate_piece(self):
        self.piece.move(drot=1)
        if not self.grid.piece_fits(self.piece):
            self.piece.move(drot=-1)  # Undo the rotation
        self.update_display()

    def step_down(self):
        """Move the piece down step by step."""
        self.piece.move(dy=1)
        if not self.grid.piece_fits(self.piece):
            self.piece.move(dy=-1)  # Undo the move
            self.grid.place_piece(self.piece)  # Lock the piece in place
            cleared_rows = self.grid.clear_full_rows()
            self.update_score(cleared_rows)
            self.piece = self.get_next_piece()  # Get the next piece
        self.update_display()

    def drop_piece(self):
        """Drop the piece to the bottom instantly."""
        while self.grid.piece_fits(self.piece):
            self.piece.move(dy=1)
        self.piece.move(dy=-1)  # Undo last invalid move
        self.grid.place_piece(self.piece)  # Lock the piece in place
        cleared_rows = self.grid.clear_full_rows()
        self.update_score(cleared_rows)
        self.piece = self.get_next_piece()  # Get the next piece
        self.update_display()

    def update_display(self):
        """Update the grid display on the canvas."""
        self.canvas.delete("all")
        block_size = 30

        # Draw the grid
        for y, row in enumerate(self.grid.grid):
            for x, cell in enumerate(row):
                if cell:
                    self.draw_block(x, y, block_size)

        # Draw the current piece
        for x, y in self.piece.get_blocks():
            self.draw_block(x, y, block_size)

    def draw_block(self, x, y, block_size):
        """Draw a single block on the canvas."""
        self.canvas.create_rectangle(
            x * block_size,
            y * block_size,
            (x + 1) * block_size,
            (y + 1) * block_size,
            fill="blue",
            outline="black"
        )

    def update_score(self, cleared_rows):
        """Update the score based on cleared rows."""
        self.score += cleared_rows * 100  # 100 points per cleared row
        self.score_label.config(text=f"Score: {self.score}")

    def reset_game(self):
        """Reset the game to its initial state."""
        self.grid = TetrisGrid()
        self.piece = self.get_next_piece()
        self.score = 0  # Reset score
        self.score_label.config(text=f"Score: {self.score}")
        self.update_display()


root = tk.Tk()
game = StepTetrisGame(root)
root.mainloop()
