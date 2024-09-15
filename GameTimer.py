import tkinter as tk
from typing import Tuple
from datetime import datetime, timedelta

class GameTimer:
    """GameTimer - Represents a timer for usage inside Game.
        Allows for initialization with duration, and controlling the timer from outside."""
    def __init__(self, minutes: int, seconds: int, bg: str) -> None:
        self.timer_label: tk.Label
        self.start_time = (minutes, seconds)
        self.time: datetime
        self.reset()
        self.running = False
        self.bg = bg

    def start(self):
        """Start the timer"""
        if (not self.running):
            self.running = True

    def stop(self):
        """Stop and reset the timer"""
        self.running = False
        self.reset()

    def get_timer_state(self):
        """Returns current timer state - running or not."""
        return self.running

    def update_time(self):
        """Call to force update the timer and it's GUI representation."""
        if (self.time.minute == 0 and self.time.second == 0):
            self.timer_label.config(text="Time's Up!")
            self.stop()
        else:
            self.time -= timedelta(seconds=1)
            self.timer_label.config(text=self.time.strftime("%M:%S"))

    def reset(self):
        """Reset the timer to initialized time"""
        minutes, seconds = self.start_time
        self.time = datetime(year=1, month=1, day=1, minute=minutes, second=seconds)

    def gui(self, frame: tk.Frame, location: Tuple[int, int, int]):
        """Create the GUI representation of the timer."""
        self.timer_label = tk.Label(frame, text=self.time.strftime("%M:%S"), font=("Arial", 24), bg=self.bg)
        row, col, colspan = location
        self.timer_label.grid(row=row, column=col, columnspan=colspan, pady=10)
