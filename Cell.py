import tkinter as tk

class Cell:
    """Cell - Represents a single cell of letters.
        The cell has a GUI representation of type {tk.Button}."""
    def __init__(self, letters: str, frame: tk.Frame, command, bg: str):
        self.letters = letters
        self.frame = frame
        self.command = command
        self.bg = bg

    def get_content(self):
        """Return the Cell's letters."""
        return self.letters
        
    def gui(self) -> tk.Button:
        """Create the GUI representation of the cell."""
        return tk.Button(
            self.frame,
            text=self.letters,
            font=("Arial", 24),
            width=5, height=2,
            command=self.command,
            bg=self.bg
            )
