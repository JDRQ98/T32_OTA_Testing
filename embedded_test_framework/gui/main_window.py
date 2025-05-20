import tkinter as tk
from tkinter import ttk, messagebox
import os
from .connection_panel import ConnectionPanel
from .test_panel import TestPanel

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Trace32 Test Framework")
        self.root.geometry("800x600")
        
        # Create menu bar
        self.create_menu()
        
        # Create main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create panels
        self.connection_panel = ConnectionPanel(self.notebook)
        self.test_panel = TestPanel(self.notebook)
        
        # Add panels to notebook
        self.notebook.add(self.connection_panel, text="Connection")
        self.notebook.add(self.test_panel, text="Tests")
        
        # Create status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set up close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_menu(self):
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Preferences", command=self.show_preferences)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

    def show_preferences(self):
        """Show preferences dialog."""
        messagebox.showinfo("Preferences", "Preferences dialog will be implemented in a future version.")

    def show_about(self):
        """Show about dialog."""
        about_text = """Trace32 Test Framework GUI
Version 0.1.0

A graphical interface for the Trace32 Test Framework.
Provides easy access to connection management and test execution."""
        messagebox.showinfo("About", about_text)

    def on_closing(self):
        """Handle window closing."""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()

def main():
    """Launch the GUI application."""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 