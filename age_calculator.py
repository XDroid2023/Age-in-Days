import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkcalendar import DateEntry
import tkinter.messagebox as messagebox
from gtts import gTTS
import os
import tempfile
import subprocess
import platform

class AgeCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Age Calculator")
        self.root.geometry("500x600")
        self.root.configure(bg='white')  # Pure white background

        # Configure styles
        self.configure_styles()

        # Create main frame
        main_frame = ttk.Frame(root, padding="30", style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # App title with custom font and color
        title_frame = ttk.Frame(main_frame, style='Title.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30), sticky='ew')
        
        title_label = ttk.Label(
            title_frame,
            text="AGE CALCULATOR",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=10)
        
        subtitle_label = ttk.Label(
            title_frame,
            text="DISCOVER YOUR LIFE IN NUMBERS",
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 10))

        # Birth date section
        date_frame = ttk.Frame(main_frame, style='Date.TFrame')
        date_frame.grid(row=1, column=0, columnspan=2, pady=20, sticky='ew')
        
        date_label = ttk.Label(
            date_frame,
            text="SELECT YOUR BIRTH DATE:",
            style='DateLabel.TLabel'
        )
        date_label.grid(row=0, column=0, pady=(0, 10))

        self.birth_date = DateEntry(
            date_frame,
            width=15,
            background='black',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            font=('Helvetica', 12, 'bold')
        )
        self.birth_date.grid(row=1, column=0, pady=10)

        # Calculate button with hover effect
        self.calculate_button = ttk.Button(
            main_frame,
            text="CALCULATE DAYS",
            command=self.calculate_days,
            style='Calculate.TButton'
        )
        self.calculate_button.grid(row=2, column=0, columnspan=2, pady=30)

        # Result section
        result_frame = ttk.Frame(main_frame, style='Result.TFrame')
        result_frame.grid(row=3, column=0, columnspan=2, pady=20, sticky='ew')
        
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(
            result_frame,
            textvariable=self.result_var,
            style='Result.TLabel',
            wraplength=400
        )
        self.result_label.grid(row=0, column=0, pady=20)

        # Center the window
        self.center_window()

    def configure_styles(self):
        style = ttk.Style()
        style.configure('Main.TFrame', background='white')
        
        # Title styles
        style.configure('Title.TFrame', background='white')
        style.configure('Title.TLabel',
                       font=('Helvetica', 32, 'bold'),
                       foreground='black',
                       background='white')
        style.configure('Subtitle.TLabel',
                       font=('Helvetica', 16, 'bold'),
                       foreground='black',
                       background='white')
        
        # Date section styles
        style.configure('Date.TFrame', background='white')
        style.configure('DateLabel.TLabel',
                       font=('Helvetica', 16, 'bold'),
                       foreground='black',
                       background='white')
        
        # Calculate button styles
        style.configure('Calculate.TButton',
                       font=('Helvetica', 14, 'bold'),
                       padding=15)
        
        # Result section styles
        style.configure('Result.TFrame', background='white')
        style.configure('Result.TLabel',
                       font=('Helvetica', 18, 'bold'),
                       foreground='black',
                       background='white',
                       justify='center')

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def speak_text(self, text):
        try:
            temp_dir = tempfile.gettempdir()
            temp_file = os.path.join(temp_dir, 'age_calc_speech.mp3')
            
            tts = gTTS(text=text, lang='en')
            tts.save(temp_file)
            
            if platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', temp_file])
            elif platform.system() == 'Windows':
                os.startfile(temp_file)
            else:  # Linux
                subprocess.run(['xdg-open', temp_file])
                
        except Exception as e:
            print(f"Speech error: {e}")

    def calculate_days(self):
        try:
            birth_date = self.birth_date.get_date()
            today = datetime.now().date()
            days_difference = (today - birth_date).days
            
            years = days_difference // 365
            remaining_days = days_difference % 365
            
            result_text = f"YOU HAVE LIVED FOR {days_difference:,} DAYS!\n\n"
            result_text += f"THAT'S APPROXIMATELY\n{years} YEARS\nAND {remaining_days} DAYS"
            
            self.result_var.set(result_text)
            
            speech_text = f"You have lived for {days_difference:,} days! That's approximately {years} years and {remaining_days} days"
            self.speak_text(speech_text)
            
        except Exception as e:
            messagebox.showerror("Error", "Please enter a valid date")

def main():
    root = tk.Tk()
    app = AgeCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
