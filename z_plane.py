import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons

class ZPlaneEditor:
    def __init__(self):
        # State: lists of zeros and poles (complex numbers)
        self.zeros = []   # list of complex numbers
        self.poles = []
        # History for undo/redo (each state is a dict with 'zeros' and 'poles')
        self.history = []
        self.history_index = -1

        # Set up the figure and axes
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim([-2, 2])
        self.ax.set_ylim([-2, 2])
        self.ax.set_aspect('equal', 'box')
        self.ax.grid(True)
        # Draw the unit circle
        unit_circle = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='--')
        self.ax.add_artist(unit_circle)

        # Artists for zeros (blue circles) and poles (red crosses)
        self.zero_artists = []
        self.pole_artists = []

        # For dragging
        self.selected_artist = None
        self.selected_type = None   # "zero" or "pole"
        self.selected_index = None

        # Create a radio button widget for choosing add mode (Zero or Pole)
        radio_ax = self.fig.add_axes([0.82, 0.7, 0.15, 0.15])
        self.radio = RadioButtons(radio_ax, ('Zero', 'Pole'), active=0)
        self.mode = 'Zero'
        self.radio.on_clicked(self.change_mode)

        # Create a check button for "add conjugate" toggle
        check_ax = self.fig.add_axes([0.82, 0.6, 0.15, 0.1])
        self.check = CheckButtons(check_ax, ['Conjugate'], [False])
        self.add_conjugate = False
        self.check.on_clicked(self.toggle_conjugate)

        # Buttons for clearing zeros, poles, all, swapping, undo, and redo
        btn_clear_zeros_ax = self.fig.add_axes([0.82, 0.5, 0.15, 0.04])
        self.btn_clear_zeros = Button(btn_clear_zeros_ax, 'Clear Zeros')
        self.btn_clear_zeros.on_clicked(self.clear_zeros)

        btn_clear_poles_ax = self.fig.add_axes([0.82, 0.45, 0.15, 0.04])
        self.btn_clear_poles = Button(btn_clear_poles_ax, 'Clear Poles')
        self.btn_clear_poles.on_clicked(self.clear_poles)

        btn_clear_all_ax = self.fig.add_axes([0.82, 0.4, 0.15, 0.04])
        self.btn_clear_all = Button(btn_clear_all_ax, 'Clear All')
        self.btn_clear_all.on_clicked(self.clear_all)

        btn_swap_ax = self.fig.add_axes([0.82, 0.35, 0.15, 0.04])
        self.btn_swap = Button(btn_swap_ax, 'Swap Z/P')
        self.btn_swap.on_clicked(self.swap)

        btn_undo_ax = self.fig.add_axes([0.82, 0.3, 0.07, 0.04])
        self.btn_undo = Button(btn_undo_ax, 'Undo')
        self.btn_undo.on_clicked(self.undo)

        btn_redo_ax = self.fig.add_axes([0.90, 0.3, 0.07, 0.04])
        self.btn_redo = Button(btn_redo_ax, 'Redo')
        self.btn_redo.on_clicked(self.redo)

        # Connect the mouse and key events
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.cid_release = self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.on_key)

        self.push_state()  # save initial empty state

    def change_mode(self, label):
        self.mode = label

    def toggle_conjugate(self, label):
        self.add_conjugate = not self.add_conjugate

    def push_state(self):
        # Save a copy of the current state (for undo/redo)
        state = {'zeros': self.zeros.copy(), 'poles': self.poles.copy()}
        # Trim history if we've undone before
        self.history = self.history[:self.history_index+1]
        self.history.append(state)
        self.history_index += 1

    def restore_state(self, state):
        self.zeros = state['zeros'].copy()
        self.poles = state['poles'].copy()
        self.update_artists()

    def undo(self, event):
        if self.history_index > 0:
            self.history_index -= 1
            self.restore_state(self.history[self.history_index])

    def redo(self, event):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.restore_state(self.history[self.history_index])

    def clear_zeros(self, event):
        self.zeros = []
        self.push_state()
        self.update_artists()

    def clear_poles(self, event):
        self.poles = []
        self.push_state()
        self.update_artists()

    def clear_all(self, event):
        self.zeros = []
        self.poles = []
        self.push_state()
        self.update_artists()

    def swap(self, event):
        self.zeros, self.poles = self.poles, self.zeros
        self.push_state()
        self.update_artists()

    def update_artists(self):
        # Remove old artists
        for artist in self.zero_artists + self.pole_artists:
            artist.remove()
        self.zero_artists = []
        self.pole_artists = []
        # Draw zeros (blue circles)
        for z in self.zeros:
            art, = self.ax.plot(z.real, z.imag, 'bo', markersize=10, picker=5)
            self.zero_artists.append(art)
        # Draw poles (red crosses)
        for p in self.poles:
            art, = self.ax.plot(p.real, p.imag, 'rx', markersize=10, picker=5)
            self.pole_artists.append(art)
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        click_point = complex(x, y)
        tol = 0.1  # tolerance for selecting an existing marker
        found = False

        # Check if clicking near a zero
        for i, z in enumerate(self.zeros):
            if abs(z - click_point) < tol:
                self.selected_artist = self.zero_artists[i]
                self.selected_type = 'zero'
                self.selected_index = i
                found = True
                break
        # Check if clicking near a pole if no zero was selected
        if not found:
            for i, p in enumerate(self.poles):
                if abs(p - click_point) < tol:
                    self.selected_artist = self.pole_artists[i]
                    self.selected_type = 'pole'
                    self.selected_index = i
                    found = True
                    break
        # If nothing is selected, add a new marker based on the current mode.
        if not found:
            new_point = complex(x, y)
            if self.mode == 'Zero':
                self.zeros.append(new_point)
                if self.add_conjugate and abs(new_point.imag) > 1e-6:
                    self.zeros.append(new_point.conjugate())
            elif self.mode == 'Pole':
                self.poles.append(new_point)
                if self.add_conjugate and abs(new_point.imag) > 1e-6:
                    self.poles.append(new_point.conjugate())
            self.push_state()
            self.update_artists()

    def on_motion(self, event):
        if self.selected_artist is None or event.inaxes != self.ax:
            return
        # Update the position of the selected marker during dragging
        x, y = event.xdata, event.ydata
        new_point = complex(x, y)
        if self.selected_type == 'zero':
            self.zeros[self.selected_index] = new_point
        elif self.selected_type == 'pole':
            self.poles[self.selected_index] = new_point
        self.selected_artist.set_data([x], [y])
        self.fig.canvas.draw_idle()

    def on_release(self, event):
        if self.selected_artist is not None:
            self.push_state()  # commit state change after drag
        self.selected_artist = None
        self.selected_type = None
        self.selected_index = None

    def on_key(self, event):
        # Allow deletion of a selected marker with delete/backspace
        if event.key in ['delete', 'backspace']:
            if self.selected_artist is not None:
                if self.selected_type == 'zero':
                    del self.zeros[self.selected_index]
                elif self.selected_type == 'pole':
                    del self.poles[self.selected_index]
                self.push_state()
                self.update_artists()
                self.selected_artist = None
                self.selected_type = None
                self.selected_index = None

if __name__ == "__main__":
    editor = ZPlaneEditor()
    plt.show()
