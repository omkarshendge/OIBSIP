import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

# ---------------- DATABASE ----------------
conn = sqlite3.connect("bmi_data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    weight REAL,
    height REAL,
    bmi REAL,
    timestamp TEXT
)
""")
conn.commit()

# ---------------- BMI LOGIC ----------------
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_bmi_color(bmi):
    if bmi < 18.5:
        return "#4A90E2"  # Blue for underweight
    elif bmi < 25:
        return "#2ECC71"  # Green for normal
    elif bmi < 30:
        return "#F39C12"  # Orange for overweight
    else:
        return "#E74C3C"  # Red for obese

# ---------------- GUI APP ----------------
class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator - Health Tracker (Made by Not_Omkar)")
        self.root.geometry("700x650")
        self.root.minsize(600, 500)  # Minimum window size
        self.root.configure(bg="#F5F5F5")
        
        # Make window resizable
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), background="#F5F5F5", foreground="#2C3E50")
        self.style.configure('Heading.TLabel', font=('Segoe UI', 11, 'bold'), background="#F5F5F5", foreground="#34495E")
        self.style.configure('Custom.TButton', font=('Segoe UI', 10, 'bold'), padding=10)
        self.style.configure('Action.TButton', font=('Segoe UI', 11, 'bold'), padding=(15, 10))

        self.create_widgets()
        
        # Bind window resize event to update fonts if needed
        self.root.bind('<Configure>', self.on_window_resize)

    def create_widgets(self):
        # Main container with padding - using grid for better control
        main_frame = tk.Frame(self.root, bg="#F5F5F5")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=15)
        main_frame.rowconfigure(1, weight=1)  # Input section can expand
        main_frame.columnconfigure(0, weight=1)

        # Title section
        title_frame = tk.Frame(main_frame, bg="#F5F5F5")
        title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = tk.Label(
            title_frame, 
            text="BMI Calculator", 
            font=('Segoe UI', 26, 'bold'),
            bg="#F5F5F5",
            fg="#2C3E50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Track your Body Mass Index and maintain a healthy lifestyle",
            font=('Segoe UI', 10),
            bg="#F5F5F5",
            fg="#7F8C8D"
        )
        subtitle_label.pack(pady=(5, 0))

        # Input section with card-like appearance
        input_frame = tk.Frame(main_frame, bg="#FFFFFF", relief=tk.FLAT, bd=0)
        input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # Add padding inside the frame
        input_inner = tk.Frame(input_frame, bg="#FFFFFF")
        input_inner.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        input_inner.columnconfigure(0, weight=1)

        # User input fields
        self.username = tk.StringVar()
        self.weight = tk.StringVar()
        self.height = tk.StringVar()

        # Username field
        username_label = tk.Label(
            input_inner,
            text="👤 Your Name",
            font=('Segoe UI', 10, 'bold'),
            bg="#FFFFFF",
            fg="#34495E",
            anchor="w"
        )
        username_label.pack(fill="x", pady=(0, 5))
        
        username_entry = tk.Entry(
            input_inner,
            textvariable=self.username,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bd=2,
            bg="#F8F9FA",
            fg="#2C3E50",
            insertbackground="#2C3E50",
            highlightthickness=2,
            highlightbackground="#BDC3C7",
            highlightcolor="#3498DB"
        )
        username_entry.pack(fill="x", pady=(0, 15), ipady=8)
        username_entry.bind('<FocusIn>', lambda e: username_entry.config(highlightbackground="#3498DB"))
        username_entry.bind('<FocusOut>', lambda e: username_entry.config(highlightbackground="#BDC3C7"))

        # Weight field
        weight_label = tk.Label(
            input_inner,
            text="⚖️ Weight (kg)",
            font=('Segoe UI', 10, 'bold'),
            bg="#FFFFFF",
            fg="#34495E",
            anchor="w"
        )
        weight_label.pack(fill="x", pady=(0, 5))
        
        weight_entry = tk.Entry(
            input_inner,
            textvariable=self.weight,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bd=2,
            bg="#F8F9FA",
            fg="#2C3E50",
            insertbackground="#2C3E50",
            highlightthickness=2,
            highlightbackground="#BDC3C7",
            highlightcolor="#3498DB"
        )
        weight_entry.pack(fill="x", pady=(0, 15), ipady=8)
        weight_entry.bind('<FocusIn>', lambda e: weight_entry.config(highlightbackground="#3498DB"))
        weight_entry.bind('<FocusOut>', lambda e: weight_entry.config(highlightbackground="#BDC3C7"))

        # Height field with helpful hint
        height_label = tk.Label(
            input_inner,
            text="Height (meters)",
            font=('Segoe UI', 10, 'bold'),
            bg="#FFFFFF",
            fg="#34495E",
            anchor="w"
        )
        height_label.pack(fill="x", pady=(0, 5))
        
        height_hint = tk.Label(
            input_inner,
            text="💡 Tip: Enter height in meters (e.g., 1.75 for 175 cm)",
            font=('Segoe UI', 8),
            bg="#FFFFFF",
            fg="#95A5A6",
            anchor="w"
        )
        height_hint.pack(fill="x", pady=(0, 5))
        
        height_entry = tk.Entry(
            input_inner,
            textvariable=self.height,
            font=('Segoe UI', 11),
            relief=tk.FLAT,
            bd=2,
            bg="#F8F9FA",
            fg="#2C3E50",
            insertbackground="#2C3E50",
            highlightthickness=2,
            highlightbackground="#BDC3C7",
            highlightcolor="#3498DB"
        )
        height_entry.pack(fill="x", pady=(0, 15), ipady=8)
        height_entry.bind('<FocusIn>', lambda e: height_entry.config(highlightbackground="#3498DB"))
        height_entry.bind('<FocusOut>', lambda e: height_entry.config(highlightbackground="#BDC3C7"))
        
        # Bind Enter key to calculate
        username_entry.bind('<Return>', lambda e: weight_entry.focus())
        weight_entry.bind('<Return>', lambda e: height_entry.focus())
        height_entry.bind('<Return>', lambda e: self.process_bmi())

        # Calculate button
        calc_btn = tk.Button(
            input_inner,
            text="Calculate BMI",
            command=self.process_bmi,
            font=('Segoe UI', 12, 'bold'),
            bg="#3498DB",
            fg="white",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=30,
            pady=12,
            activebackground="#2980B9",
            activeforeground="white"
        )
        calc_btn.pack(pady=(5, 0), fill="x")
        calc_btn.bind('<Enter>', lambda e: calc_btn.config(bg="#2980B9"))
        calc_btn.bind('<Leave>', lambda e: calc_btn.config(bg="#3498DB"))

        # Result section
        result_frame = tk.Frame(main_frame, bg="#F5F5F5")
        result_frame.grid(row=2, column=0, sticky="ew", pady=(10, 15))
        result_frame.columnconfigure(0, weight=1)

        self.result_label = tk.Label(
            result_frame,
            text="",
            font=('Segoe UI', 14, 'bold'),
            bg="#F5F5F5",
            fg="#2C3E50"
        )
        self.result_label.pack()
        
        self.category_label = tk.Label(
            result_frame,
            text="",
            font=('Segoe UI', 11),
            bg="#F5F5F5",
            fg="#7F8C8D"
        )
        self.category_label.pack(pady=(5, 0))

        # Action buttons section
        btn_frame = tk.Frame(main_frame, bg="#F5F5F5")
        btn_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)

        # Create styled buttons
        buttons = [
            ("View History", self.show_history, "#16A085"),
            (" Show Graph", self.show_graph, "#9B59B6"),
            (" Statistics", self.show_stats, "#E67E22")
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=('Segoe UI', 10, 'bold'),
                bg=color,
                fg="white",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                padx=20,
                pady=12,
                activebackground=self.darken_color(color),
                activeforeground="white"
            )
            btn.grid(row=0, column=i, padx=8, sticky="nsew", ipady=10)
            btn.bind('<Enter>', lambda e, c=color, b=btn: b.config(bg=self.darken_color(c)))
            btn.bind('<Leave>', lambda e, c=color, b=btn: b.config(bg=c))

    def on_window_resize(self, event):
        """Handle window resize events"""
        if event.widget == self.root:
            # Update any dynamic sizing if needed
            pass

    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        color_map = {
            "#16A085": "#138D75",
            "#9B59B6": "#8E44AD",
            "#E67E22": "#D35400"
        }
        return color_map.get(color, color)

    def process_bmi(self):
        try:
            name = self.username.get().strip()
            weight_str = self.weight.get().strip()
            height_str = self.height.get().strip()

            if not name:
                messagebox.showerror("Input Error", "Please enter your name.")
                return

            if not weight_str or not height_str:
                messagebox.showerror("Input Error", "Please enter both weight and height.")
                return

            weight = float(weight_str)
            height = float(height_str)

            if weight <= 0 or height <= 0:
                raise ValueError("Values must be positive")

            if height > 3:  # Likely entered in cm instead of meters
                messagebox.showwarning(
                    "Height Warning",
                    "Height seems too large. Did you mean to enter in meters?\n"
                    "Example: 1.75 for 175 cm"
                )
                return

            bmi = calculate_bmi(weight, height)
            category = bmi_category(bmi)
            color = get_bmi_color(bmi)

            # Update result display with better formatting
            self.result_label.config(
                text=f"Your BMI: {bmi}",
                fg=color,
                font=('Segoe UI', 18, 'bold')
            )
            
            category_emoji = {
                "Underweight": "📉",
                "Normal": "✅",
                "Overweight": "⚠️",
                "Obese": "🚨"
            }
            
            self.category_label.config(
                text=f"{category_emoji.get(category, '')} Category: {category}",
                fg=color,
                font=('Segoe UI', 12)
            )

            # Save to database
            cur.execute(
                "INSERT INTO bmi_records VALUES (NULL, ?, ?, ?, ?, ?)",
                (name, weight, height, bmi, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

            # Show success message
            messagebox.showinfo("Success", f"BMI calculated and saved!\n\nBMI: {bmi}\nCategory: {category}")

        except ValueError as e:
            if "could not convert" in str(e).lower():
                messagebox.showerror("Input Error", "Please enter valid numbers for weight and height.")
            else:
                messagebox.showerror("Input Error", "Please enter valid positive values for weight and height.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def show_history(self):
        name = self.username.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter your name first to view history.")
            return

        win = tk.Toplevel(self.root)
        win.title(f"BMI History - {name}")
        win.geometry("750x500")
        win.minsize(600, 400)
        win.configure(bg="#F5F5F5")
        
        # Make window resizable
        win.rowconfigure(1, weight=1)
        win.columnconfigure(0, weight=1)

        # Header
        header = tk.Frame(win, bg="#34495E", pady=15)
        header.grid(row=0, column=0, sticky="ew")
        win.columnconfigure(0, weight=1)
        
        tk.Label(
            header,
            text=f"📋 BMI History for {name}",
            font=('Segoe UI', 16, 'bold'),
            bg="#34495E",
            fg="white"
        ).pack()

        # Treeview with scrollbar
        container = tk.Frame(win, bg="#F5F5F5")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(container)
        scrollbar.grid(row=0, column=1, sticky="ns")

        cols = ("Date & Time", "Weight (kg)", "Height (m)", "BMI", "Category")
        tree = ttk.Treeview(container, columns=cols, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        # Configure columns with proportional widths
        tree.heading("Date & Time", text="Date & Time")
        tree.heading("Weight (kg)", text="Weight (kg)")
        tree.heading("Height (m)", text="Height (m)")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")

        # Use stretch option for responsive columns
        # Configure columns with proportional widths
        tree.column("Date & Time", width=200, anchor="center", stretch=True, minwidth=150)
        tree.column("Weight (kg)", width=120, anchor="center", stretch=True, minwidth=80)
        tree.column("Height (m)", width=120, anchor="center", stretch=True, minwidth=80)
        tree.column("BMI", width=100, anchor="center", stretch=True, minwidth=70)
        tree.column("Category", width=150, anchor="center", stretch=True, minwidth=100)

        tree.grid(row=0, column=0, sticky="nsew")
        
        # Function to resize columns on window resize
        def resize_columns(event):
            if event.widget == win:
                total_width = win.winfo_width() - 60  # Account for padding and scrollbar
                if total_width > 0:
                    # Proportional column widths
                    tree.column("Date & Time", width=int(total_width * 0.30))
                    tree.column("Weight (kg)", width=int(total_width * 0.18))
                    tree.column("Height (m)", width=int(total_width * 0.18))
                    tree.column("BMI", width=int(total_width * 0.15))
                    tree.column("Category", width=int(total_width * 0.19))
        
        win.bind('<Configure>', resize_columns)

        # Fetch and display data
        cur.execute(
            "SELECT timestamp, weight, height, bmi FROM bmi_records WHERE username=? ORDER BY timestamp DESC",
            (name,)
        )
        rows = cur.fetchall()

        if not rows:
            messagebox.showinfo("No Data", f"No BMI records found for {name}.")
            win.destroy()
            return

        for row in rows:
            timestamp, weight, height, bmi = row
            category = bmi_category(bmi)
            tree.insert("", "end", values=(timestamp, f"{weight:.2f}", f"{height:.2f}", f"{bmi:.2f}", category))

    def show_graph(self):
        name = self.username.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter your name first to view graph.")
            return

        cur.execute(
            "SELECT timestamp, bmi FROM bmi_records WHERE username=? ORDER BY timestamp",
            (name,)
        )
        data = cur.fetchall()

        if not data:
            messagebox.showinfo("No Data", f"No BMI records found for {name}.")
            return

        dates = [d[0] for d in data]
        bmis = [d[1] for d in data]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, bmis, marker="o", linewidth=2, markersize=8, color="#3498DB")
        plt.xticks(rotation=45, ha='right')
        plt.title(f"BMI Trend Over Time - {name}", fontsize=14, fontweight='bold', pad=20)
        plt.xlabel("Date", fontsize=11)
        plt.ylabel("BMI", fontsize=11)
        plt.grid(True, alpha=0.3, linestyle='--')
        
        # Add category reference lines
        plt.axhline(y=18.5, color='#4A90E2', linestyle='--', alpha=0.5, label='Underweight threshold')
        plt.axhline(y=25, color='#2ECC71', linestyle='--', alpha=0.5, label='Normal threshold')
        plt.axhline(y=30, color='#F39C12', linestyle='--', alpha=0.5, label='Overweight threshold')
        
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    def show_stats(self):
        name = self.username.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Please enter your name first to view statistics.")
            return

        cur.execute(
            "SELECT bmi FROM bmi_records WHERE username=?",
            (name,)
        )
        bmis = [row[0] for row in cur.fetchall()]

        if not bmis:
            messagebox.showinfo("No Data", f"No BMI records found for {name}.")
            return

        avg_bmi = round(sum(bmis) / len(bmis), 2)
        min_bmi = min(bmis)
        max_bmi = max(bmis)
        latest_bmi = bmis[-1]
        latest_category = bmi_category(latest_bmi)
        
        # Create a nice stats window
        stats_win = tk.Toplevel(self.root)
        stats_win.title(f"BMI Statistics - {name}")
        stats_win.geometry("500x400")
        stats_win.minsize(450, 350)
        stats_win.configure(bg="#F5F5F5")
        
        # Make window resizable
        stats_win.rowconfigure(1, weight=1)
        stats_win.columnconfigure(0, weight=1)

        # Header
        header = tk.Frame(stats_win, bg="#34495E", pady=20)
        header.grid(row=0, column=0, sticky="ew")
        stats_win.columnconfigure(0, weight=1)
        
        tk.Label(
            header,
            text=f"📊 BMI Statistics",
            font=('Segoe UI', 18, 'bold'),
            bg="#34495E",
            fg="white"
        ).pack()

        # Stats content with scrollable frame
        content_frame = tk.Frame(stats_win, bg="#F5F5F5")
        content_frame.grid(row=1, column=0, sticky="nsew", padx=30, pady=30)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Canvas for scrolling
        canvas = tk.Canvas(content_frame, bg="#F5F5F5", highlightthickness=0)
        scrollbar_stats = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        content = tk.Frame(canvas, bg="#F5F5F5")
        
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_stats.set)
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar_stats.grid(row=0, column=1, sticky="ns")

        stats_data = [
            ("Total Records", f"{len(bmis)}", "#3498DB"),
            ("Latest BMI", f"{latest_bmi:.2f} ({latest_category})", get_bmi_color(latest_bmi)),
            ("Average BMI", f"{avg_bmi:.2f}", "#9B59B6"),
            ("Minimum BMI", f"{min_bmi:.2f}", "#16A085"),
            ("Maximum BMI", f"{max_bmi:.2f}", "#E67E22")
        ]

        for i, (label, value, color) in enumerate(stats_data):
            stat_frame = tk.Frame(content, bg="#FFFFFF", relief=tk.FLAT, bd=1)
            stat_frame.pack(fill="x", pady=8, padx=10)
            stat_frame.columnconfigure(0, weight=1)
            
            inner = tk.Frame(stat_frame, bg="#FFFFFF", padx=20, pady=15)
            inner.pack(fill="both", expand=True)
            inner.columnconfigure(0, weight=1)
            
            tk.Label(
                inner,
                text=label,
                font=('Segoe UI', 10),
                bg="#FFFFFF",
                fg="#7F8C8D",
                anchor="w"
            ).pack(fill="x")
            
            tk.Label(
                inner,
                text=value,
                font=('Segoe UI', 16, 'bold'),
                bg="#FFFFFF",
                fg=color,
                anchor="w"
            ).pack(fill="x", pady=(5, 0))
        
        # Update canvas scroll region when content changes
        content.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

# ---------------- RUN APP ----------------
root = tk.Tk()
app = BMICalculator(root)
root.mainloop()
conn.close()
