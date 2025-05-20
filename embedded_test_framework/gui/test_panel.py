import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import subprocess
import threading

class TestPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.test_process = None

    def create_widgets(self):
        """Create the test panel widgets."""
        # Test selection frame
        selection_frame = ttk.LabelFrame(self, text="Test Selection")
        selection_frame.pack(fill=tk.X, padx=5, pady=5)

        # Test path input
        ttk.Label(selection_frame, text="Test Path:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.test_path_var = tk.StringVar(value="tests/")
        self.test_path_entry = ttk.Entry(selection_frame, textvariable=self.test_path_var)
        self.test_path_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Browse button
        self.browse_button = ttk.Button(selection_frame, text="Browse", command=self.browse_test)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        # Test options frame
        options_frame = ttk.LabelFrame(self, text="Test Options")
        options_frame.pack(fill=tk.X, padx=5, pady=5)

        # Verbose output checkbox
        self.verbose_var = tk.BooleanVar(value=True)
        self.verbose_check = ttk.Checkbutton(options_frame, text="Verbose Output", variable=self.verbose_var)
        self.verbose_check.pack(padx=5, pady=5, anchor=tk.W)

        # Test output frame
        output_frame = ttk.LabelFrame(self, text="Test Output")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Output text widget with scrollbar
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=10)
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)

        # Test control buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Run tests button
        self.run_button = ttk.Button(button_frame, text="Run Tests", command=self.run_tests)
        self.run_button.pack(side=tk.LEFT, padx=5)

        # Stop tests button
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_tests, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Clear output button
        self.clear_button = ttk.Button(button_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def browse_test(self):
        """Open file dialog to select test file or directory."""
        initial_dir = os.path.abspath(self.test_path_var.get())
        if not os.path.exists(initial_dir):
            initial_dir = os.getcwd()

        path = filedialog.askopenfilename(
            initialdir=initial_dir,
            title="Select Test File",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        
        if path:
            self.test_path_var.set(path)

    def run_tests(self):
        """Run the selected tests."""
        test_path = self.test_path_var.get()
        if not test_path:
            messagebox.showerror("Error", "Please select a test file or directory")
            return

        # Clear previous output
        self.clear_output()

        # Prepare command
        cmd = ["python", "run_tests.py"]
        if self.verbose_var.get():
            cmd.append("-v")
        cmd.append(test_path)

        # Disable run button and enable stop button
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Run tests in a separate thread
        self.test_thread = threading.Thread(target=self._run_tests_thread, args=(cmd,))
        self.test_thread.daemon = True
        self.test_thread.start()

    def _run_tests_thread(self, cmd):
        """Run tests in a separate thread and capture output."""
        try:
            self.test_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            # Read output in real-time
            for line in self.test_process.stdout:
                self.output_text.insert(tk.END, line)
                self.output_text.see(tk.END)
                self.output_text.update()

            # Wait for process to complete
            self.test_process.wait()

        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            # Re-enable run button and disable stop button
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.test_process = None

    def stop_tests(self):
        """Stop the running tests."""
        if self.test_process:
            self.test_process.terminate()
            self.output_text.insert(tk.END, "\nTests stopped by user.\n")
            self.run_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.test_process = None

    def clear_output(self):
        """Clear the output text widget."""
        self.output_text.delete(1.0, tk.END) 