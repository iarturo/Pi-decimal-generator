import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import sys
from decimal import Decimal, getcontext

class PiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Generator")
        self.root.geometry("500x450")
        self.root.resizable(True, True)  # Enable window resizing
        self.root.minsize(450, 400)  # Set minimum size
        
        # Fullscreen state
        self.is_fullscreen = False
        
        # Dark mode state
        self.is_dark_mode = False
        
        # Threading control
        self.calculation_thread = None
        self.stop_calculation = False
        self.result_queue = queue.Queue()
        
        # Configure styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))
        
        # Create header frame for dark mode toggle
        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        # Dark mode toggle button (positioned on the right)
        self.dark_mode_button = ttk.Button(self.header_frame, text="🌙 Dark Mode", command=self.toggle_dark_mode)
        self.dark_mode_button.pack(side=tk.RIGHT)
        
        # Fullscreen toggle button (positioned on the right, before dark mode)
        self.fullscreen_button = ttk.Button(self.header_frame, text="⛶ Fullscreen", command=self.toggle_fullscreen)
        self.fullscreen_button.pack(side=tk.RIGHT, padx=(0, 5))
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create input elements
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.quantity_label = ttk.Label(self.input_frame, text="Quantity of Digits:")
        self.quantity_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.quantity_var = tk.StringVar()
        
        # Register validation function
        vcmd = (self.root.register(self.validate_number_input), '%P')
        
        self.quantity_entry = ttk.Entry(self.input_frame, width=10, textvariable=self.quantity_var, 
                                      validate='key', validatecommand=vcmd)
        self.quantity_entry.pack(side=tk.LEFT)
        
        self.run_button = ttk.Button(self.input_frame, text="🚀 Generate Pi", command=self.generate_pi)
        self.run_button.pack(side=tk.LEFT, padx=(10, 0))
        
        self.stop_button = ttk.Button(self.input_frame, text="⏹️ Stop", command=self.stop_generation, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Progress bar and info
        self.progress_frame = ttk.Frame(self.main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(10, 10))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = ttk.Label(self.progress_frame, text="Ready to generate Pi digits")
        self.status_label.pack()
        
        # Create output area
        self.output_frame = ttk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_label = ttk.Label(self.output_frame, text="Pi digits will appear here")
        self.output_label.pack(pady=10)
        
        # Create frame for text widget and scrollbar
        self.text_frame = ttk.Frame(self.output_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget
        self.result_text = tk.Text(self.text_frame, height=12, width=50, wrap=tk.WORD, state="disabled")
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create and configure scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text widget to work with scrollbar
        self.result_text.configure(yscrollcommand=self.scrollbar.set)
        
        # Apply initial light theme after all widgets are created
        self.configure_light_theme()
        
        # Bind keyboard shortcuts
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Escape>', lambda e: self.exit_fullscreen() if self.is_fullscreen else None)
        
        # Start queue processing
        self.process_queue()
        
    def validate_number_input(self, value):
        """Validate that input contains only numbers"""
        if value == "":  # Allow empty string
            return True
        try:
            int(value)  # Try to convert to integer
            return True
        except ValueError:
            return False  # Reject if not a valid number
        
    def calculate_pi_chudnovsky(self, precision):
        """Calculate Pi using Chudnovsky algorithm (very fast convergence)"""
        getcontext().prec = precision + 100  # Extra precision for calculation
        
        # Chudnovsky algorithm constants
        C = 426880 * Decimal(10005).sqrt()
        K, M, L, X, S = 6, 1, 13591409, 1, 13591409
        
        for k in range(1, precision // 14 + 100):  # Each iteration gives ~14 digits
            if self.stop_calculation:
                return None
                
            M = (K**3 - 16*K) * M // (k**3)
            L += 545140134
            X *= -262537412640768000
            S += Decimal(M * L) / X
            K += 12
            
            # Update progress periodically
            if k % 10 == 0:
                progress = min(100, (k * 14 * 100) // precision)
                self.result_queue.put(("progress", progress))
        
        pi = C / S
        return pi
    
    def calculate_pi_machin(self, precision):
        """Calculate Pi using Machin's formula (good for moderate precision)"""
        getcontext().prec = precision + 50
        
        def arctan(x, precision_needed):
            power = x
            result = x
            i = 1
            while True:
                if self.stop_calculation:
                    return None
                power *= -x * x
                term = power / (2 * i + 1)
                if abs(term) < Decimal(10) ** (-precision_needed - 10):
                    break
                result += term
                i += 1
                
                # Update progress
                if i % 100 == 0:
                    progress = min(90, (i * 100) // (precision_needed // 4))
                    self.result_queue.put(("progress", progress))
            
            return result
        
        # Machin's formula: π = 16*arctan(1/5) - 4*arctan(1/239)
        pi = 4 * (4 * arctan(Decimal(1)/Decimal(5), precision) - arctan(Decimal(1)/Decimal(239), precision))
        return pi
    
    def generate_pi(self):
        try:
            digits = int(self.quantity_var.get())
            if digits <= 0:
                messagebox.showerror("Invalid Input", "Please enter a positive number")
                return
            
            # Hard limit for hardware protection
            if digits > 100000:
                messagebox.showerror("Number Too Large", 
                    "The number of digits must be 100,000 or less.\n"
                    "Larger numbers would consume too much memory and time.")
                return
            
            # Warning for large numbers (5000+ digits)
            if digits > 5000:
                result = messagebox.askyesno("Large Number Warning", 
                    f"Generating {digits:,} digits will take some time.\n"
                    f"Estimated time: {self.estimate_time(digits)}\n"
                    "Are you sure you want to continue?")
                if not result:
                    return
                    
            # Reset stop flag and clear previous results
            self.stop_calculation = False
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state="disabled")
            
            # Update UI state
            self.run_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.progress_bar.config(maximum=100, value=0)
            self.status_label.config(text="Calculating Pi...")
            
            # Start calculation in separate thread
            self.calculation_thread = threading.Thread(target=self.pi_worker, args=(digits,))
            self.calculation_thread.daemon = True
            self.calculation_thread.start()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
    
    def pi_worker(self, digits):
        """Calculate Pi in a separate thread"""
        try:
            # Send initial message
            self.result_queue.put(("start", f"Calculating Pi to {digits} decimal places...\n\n"))
            
            # Choose algorithm based on precision needed
            if digits <= 5000:
                pi = self.calculate_pi_machin(digits)
            else:
                pi = self.calculate_pi_chudnovsky(digits)
            
            if pi is None:  # Calculation was stopped
                return
            
            # Format the result
            pi_str = str(pi)
            
            # Ensure we have the right number of digits after decimal point
            if '.' in pi_str:
                integer_part, decimal_part = pi_str.split('.')
                if len(decimal_part) > digits:
                    decimal_part = decimal_part[:digits]
                elif len(decimal_part) < digits:
                    decimal_part = decimal_part.ljust(digits, '0')
                pi_formatted = f"{integer_part}.{decimal_part}"
            else:
                pi_formatted = pi_str + '.' + '0' * digits
            
            # Format output with line breaks every 50 characters for readability
            output_text = "Pi = "
            chars_per_line = 50
            for i, char in enumerate(pi_formatted):
                output_text += char
                if char != '.' and (i + 1) % chars_per_line == 0:
                    output_text += "\n     "  # Indent continuation lines
            
            # Send the result
            self.result_queue.put(("result", output_text))
            self.result_queue.put(("complete", f"\n\nCalculation complete! Generated Pi to {digits} decimal places."))
            
        except Exception as e:
            self.result_queue.put(("error", f"Error during calculation: {str(e)}"))
    
    def stop_generation(self):
        """Stop the current Pi calculation"""
        self.stop_calculation = True
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Stopping calculation...")
    
    def process_queue(self):
        """Process messages from the worker thread"""
        try:
            while True:
                message_type, data = self.result_queue.get_nowait()
                
                if message_type == "start":
                    self.result_text.config(state="normal")
                    self.result_text.insert(tk.END, data)
                    self.result_text.config(state="disabled")
                    
                elif message_type == "result":
                    self.result_text.config(state="normal")
                    self.result_text.insert(tk.END, data)
                    self.result_text.see(tk.END)  # Auto-scroll to bottom
                    self.result_text.config(state="disabled")
                    
                elif message_type == "progress":
                    self.progress_bar.config(value=data)
                    self.status_label.config(text=f"Calculating Pi... {data}%")
                    
                elif message_type in ["complete", "stopped", "error"]:
                    self.result_text.config(state="normal")
                    self.result_text.insert(tk.END, data)
                    self.result_text.config(state="disabled")
                    
                    # Reset UI state
                    self.run_button.config(state="normal")
                    self.stop_button.config(state="disabled")
                    self.status_label.config(text="Ready to generate Pi digits")
                    self.progress_bar.config(value=100)
                    
        except queue.Empty:
            pass
        
        # Schedule next queue check
        self.root.after(50, self.process_queue)
    
    def estimate_time(self, digits):
        """Estimate calculation time based on digits"""
        if digits <= 1000:
            return "less than 1 second"
        elif digits <= 5000:
            return "1-5 seconds"
        elif digits <= 10000:
            return "5-15 seconds"
        elif digits <= 25000:
            return "15-30 seconds"
        elif digits <= 50000:
            return "30-60 seconds"
        elif digits <= 75000:
            return "1-2 minutes"
        elif digits <= 100000:
            return "2-3 minutes"
        else:
            return "3+ minutes"
    
    def configure_light_theme(self):
        """Configure light theme colors"""
        # Configure ttk styles for light theme
        self.style.configure("TButton", font=("Arial", 10), foreground="black", background="white")
        self.style.configure("TLabel", font=("Arial", 12), foreground="black", background="white")
        self.style.configure("TEntry", font=("Arial", 12), foreground="black", fieldbackground="white")
        self.style.configure("TFrame", background="white")
        
        # Configure root and text widget
        self.root.configure(bg="white")
        self.result_text.configure(bg="white", fg="black", insertbackground="black")
    
    def configure_dark_theme(self):
        """Configure dark theme colors"""
        # Configure ttk styles for dark theme - TEXTO SIEMPRE NEGRO
        self.style.configure("TButton", font=("Arial", 10), foreground="black", background="#c0c0c0")
        self.style.configure("TLabel", font=("Arial", 12), foreground="white", background="#2d2d2d")
        self.style.configure("TEntry", font=("Arial", 12), foreground="black", fieldbackground="white")
        self.style.configure("TFrame", background="#2d2d2d")
        
        # Configure root and text widget
        self.root.configure(bg="#2d2d2d")
        self.result_text.configure(bg="#2d2d2d", fg="white", insertbackground="white")
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.is_dark_mode = not self.is_dark_mode
        
        if self.is_dark_mode:
            self.configure_dark_theme()
            self.dark_mode_button.configure(text="☀️ Light Mode")
        else:
            self.configure_light_theme()
            self.dark_mode_button.configure(text="🌙 Dark Mode")
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        
        if self.is_fullscreen:
            self.root.attributes('-fullscreen', True)
            self.fullscreen_button.configure(text="⛶ Exit Fullscreen")
        else:
            self.root.attributes('-fullscreen', False)
            self.fullscreen_button.configure(text="⛶ Fullscreen")
    
    def exit_fullscreen(self):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.root.attributes('-fullscreen', False)
            self.fullscreen_button.configure(text="⛶ Fullscreen")

if __name__ == "__main__":
    root = tk.Tk()
    app = PiApp(root)
    root.mainloop()