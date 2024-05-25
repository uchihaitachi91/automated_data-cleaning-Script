import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from autoclean import AutoClean
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import sys


class AutoCleanGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoClean GUI")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to AutoClean GUI")
        self.label.pack()

        self.load_button = tk.Button(self, text="Load CSV", command=self.load_csv)
        self.load_button.pack()

        self.dataset_label = tk.Label(self, text="Dataset: None")
        self.dataset_label.pack()

        self.clean_button = tk.Button(self, text="Clean Data", command=self.clean_data, state=tk.DISABLED)
        self.clean_button.pack()

        self.save_button = tk.Button(self, text="Save Cleaned Data", command=self.save_data, state=tk.DISABLED)
        self.save_button.pack()

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.close_button = tk.Button(self, text="Close", command=self.close_app)
        self.close_button.pack()

        self.explanation_label = tk.Label(self, text="")
        self.explanation_label.pack()

        self.before_after_frame = tk.Frame(self)
        self.before_after_frame.pack(fill=tk.BOTH, expand=True)

        self.before_text = tk.Text(self.before_after_frame, wrap=tk.NONE, width=50)
        self.before_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.after_text = tk.Text(self.before_after_frame, wrap=tk.NONE, width=50)
        self.after_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.view_more_button = tk.Button(self, text="View More...", command=self.toggle_view_more)
        self.view_more_button.pack()

        self.fullscreen_button = tk.Button(self, text="Full Screen Visualizations", command=self.open_fullscreen)
        self.fullscreen_button.pack()

        self.canvas = None
        self.toolbar = None
        self.fullscreen = False

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.dataset_label.config(text=f"Dataset: {file_path}")
            self.clean_button.config(state=tk.NORMAL)

    def clean_data(self):
        try:
            self.cleaner = AutoClean(self.df)
            self.cleaned_df = self.cleaner.output

            # Align columns of cleaned DataFrame with original DataFrame
            self.cleaned_df = self.cleaned_df.reindex(columns=self.df.columns)

            self.save_button.config(state=tk.NORMAL)
            self.show_explanation()
            self.show_before_after()
            messagebox.showinfo("Success", "Data cleaned successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def show_explanation(self):
        explanation = "Data cleaning completed!\n\n"
        explanation += "Changes made to the dataset:\n"

        if self.cleaner.duplicates:
            explanation += "- Removed duplicate rows.\n"

        if self.cleaner.missing_num or self.cleaner.missing_categ:
            explanation += "- Imputed missing values.\n"

        if self.cleaner.outliers:
            explanation += "- Handled outliers.\n"

        if self.cleaner.extract_datetime:
            explanation += "- Extracted datetime features.\n"

        if self.cleaner.encode_categ:
            explanation += "- Encoded categorical features.\n"

        self.explanation_label.config(text=explanation)

    def show_before_after(self):
        before_text = "Before Cleaning:\n\n" + self.df.head(15).to_string(index=False)
        after_text = "After Cleaning:\n\n" + self.cleaned_df.head(15).to_string(index=False)

        self.before_text.delete(1.0, tk.END)
        self.before_text.insert(tk.END, before_text)

        self.after_text.delete(1.0, tk.END)
        self.after_text.insert(tk.END, after_text)

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.cleaned_df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Cleaned data saved successfully!")

    def reset(self):
        self.load_button.config(state=tk.NORMAL)
        self.clean_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.dataset_label.config(text="Dataset: None")
        self.explanation_label.config(text="")
        self.before_text.delete(1.0, tk.END)
        self.after_text.delete(1.0, tk.END)

    def close_app(self):
        self.destroy()
        sys.exit()

    def toggle_view_more(self):
        if self.view_more_button.cget("text") == "View More...":
            self.show_full_data()
            self.view_more_button.config(text="View Less")
        else:
            self.show_before_after()
            self.view_more_button.config(text="View More...")

    def show_full_data(self):
        before_text = "Before Cleaning:\n\n" + self.df.to_string(index=False)
        after_text = "After Cleaning:\n\n" + self.cleaned_df.to_string(index=False)

        self.before_text.delete(1.0, tk.END)
        self.before_text.insert(tk.END, before_text)

        self.after_text.delete(1.0, tk.END)
        self.after_text.insert(tk.END, after_text)

    def open_fullscreen(self):
        if self.fullscreen:
            self.fullscreen_button.config(text="Full Screen Visualizations")
            self.fullscreen_window.destroy()
            self.fullscreen = False
        else:
            self.fullscreen_button.config(text="Exit Full Screen")
            self.fullscreen_window = tk.Toplevel(self)
            self.fullscreen_window.attributes('-fullscreen', True)
            self.fullscreen_window.protocol("WM_DELETE_WINDOW", self.close_fullscreen)
            self.fullscreen_window.title("Full Screen Visualizations")
            self.fullscreen_window.configure(bg="white")

            fig, ax = plt.subplots(1, 2, figsize=(15, 6))

            # Plot outliers distribution for before cleaning
            self.df.boxplot(ax=ax[0])
            ax[0].set_title("Before Cleaning")
            ax[0].set_ylabel("Values")

            # Plot outliers distribution for after cleaning
            self.cleaned_df.boxplot(ax=ax[1])
            ax[1].set_title("After Cleaning")
            ax[1].set_ylabel("Values")

            canvas = FigureCanvasTkAgg(fig, master=self.fullscreen_window)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            toolbar = NavigationToolbar2Tk(canvas, self.fullscreen_window)
            toolbar.update()
            toolbar.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

            back_button = tk.Button(self.fullscreen_window, text="Back to GUI", command=self.close_fullscreen)
            back_button.pack(side=tk.BOTTOM)

            self.fullscreen = True

    def close_fullscreen(self):
        self.fullscreen_button.config(text="Full Screen Visualizations")
        self.fullscreen_window.destroy()
        self.fullscreen = False


if __name__ == "__main__":
    app = AutoCleanGUI()
    app.mainloop()
