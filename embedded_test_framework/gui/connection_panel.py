import tkinter as tk
from tkinter import ttk, messagebox
from src.test_framework.t32_connector import T32Connector
from src.test_framework.config_loader import load_config

class ConnectionPanel(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.connector = None
        self.create_widgets()
        self.load_settings()

    def create_widgets(self):
        """Create the connection panel widgets."""
        # Connection settings frame
        settings_frame = ttk.LabelFrame(self, text="Connection Settings")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)

        # Node (IP) input
        ttk.Label(settings_frame, text="Node/IP:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.node_var = tk.StringVar()
        self.node_entry = ttk.Entry(settings_frame, textvariable=self.node_var)
        self.node_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Port input
        ttk.Label(settings_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.port_var = tk.StringVar()
        self.port_entry = ttk.Entry(settings_frame, textvariable=self.port_var)
        self.port_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Retry settings frame
        retry_frame = ttk.LabelFrame(self, text="Retry Settings")
        retry_frame.pack(fill=tk.X, padx=5, pady=5)

        # Max retries
        ttk.Label(retry_frame, text="Max Retries:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_retries_var = tk.StringVar(value="1")
        self.max_retries_entry = ttk.Entry(retry_frame, textvariable=self.max_retries_var)
        self.max_retries_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        # Retry delay
        ttk.Label(retry_frame, text="Retry Delay (s):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.retry_delay_var = tk.StringVar(value="1.0")
        self.retry_delay_entry = ttk.Entry(retry_frame, textvariable=self.retry_delay_var)
        self.retry_delay_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        # Connection status frame
        status_frame = ttk.LabelFrame(self, text="Connection Status")
        status_frame.pack(fill=tk.X, padx=5, pady=5)

        # Status indicator
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(padx=5, pady=5)

        # Connection buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        # Connect button
        self.connect_button = ttk.Button(button_frame, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.LEFT, padx=5)

        # Disconnect button
        self.disconnect_button = ttk.Button(button_frame, text="Disconnect", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.pack(side=tk.LEFT, padx=5)

        # Check connection button
        self.check_button = ttk.Button(button_frame, text="Check Connection", command=self.check_connection)
        self.check_button.pack(side=tk.LEFT, padx=5)

    def load_settings(self):
        """Load connection settings from config file."""
        try:
            cfg = load_config("global_settings.ini")
            self.node_var.set(cfg.get('Trace32', 'node', fallback='localhost'))
            self.port_var.set(cfg.get('Trace32', 'port', fallback='20000'))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load settings: {e}")

    def connect(self):
        """Attempt to connect to Trace32."""
        try:
            # Get connection parameters
            node = self.node_var.get()
            port = self.port_var.get()
            max_retries = int(self.max_retries_var.get())
            retry_delay = float(self.retry_delay_var.get())

            # Create connector if needed
            if not self.connector:
                self.connector = T32Connector()

            # Attempt connection
            if self.connector.connect(node=node, port=port, max_retries=max_retries, retry_delay=retry_delay):
                self.status_var.set("Connected")
                self.connect_button.config(state=tk.DISABLED)
                self.disconnect_button.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Successfully connected to Trace32")
            else:
                messagebox.showerror("Error", "Failed to connect to Trace32")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {e}")

    def disconnect(self):
        """Disconnect from Trace32."""
        if self.connector:
            self.connector.disconnect()
            self.status_var.set("Disconnected")
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "Successfully disconnected from Trace32")

    def check_connection(self):
        """Check connection health."""
        if not self.connector or not self.connector.is_connected:
            messagebox.showwarning("Warning", "Not connected to Trace32")
            return

        if self.connector.check_connection():
            messagebox.showinfo("Success", "Connection health check passed")
        else:
            messagebox.showerror("Error", "Connection health check failed") 