"""Tkinter GUI wrapper for an unchanged main.py email extractor.

Place this file beside your existing main.py. The GUI copies the chosen input
file to a temporary input.txt, runs main.py there, and reads its emails.txt.
"""

import shutil
import subprocess
import sys
import tempfile
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_FOLDER = Path(__file__).resolve().parent
MAIN_SCRIPT = APP_FOLDER / "main.py"


class EmailExtractorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Extractor")
        self.geometry("700x500")
        self.minsize(550, 380)

        self.selected_file = None
        self.emails_text = ""
        self.file_label = tk.StringVar(value="No input file selected")
        self.status = tk.StringVar(value="Choose a text file, then extract emails.")
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        ttk.Label(frame, text="Email Extractor", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, sticky="w"
        )

        controls = ttk.Frame(frame)
        controls.grid(row=1, column=0, sticky="ew", pady=(16, 10))
        controls.columnconfigure(0, weight=1)
        ttk.Label(controls, textvariable=self.file_label).grid(row=0, column=0, sticky="w")
        ttk.Button(controls, text="Choose file…", command=self.choose_file).grid(
            row=0, column=1, padx=(12, 0)
        )

        buttons = ttk.Frame(frame)
        buttons.grid(row=2, column=0, sticky="w", pady=(0, 10))
        ttk.Button(buttons, text="Extract emails", command=self.extract_emails).pack(side="left")
        self.save_button = ttk.Button(buttons, text="Save results…", command=self.save_results, state="disabled")
        self.save_button.pack(side="left", padx=(8, 0))

        output = ttk.LabelFrame(frame, text="Results", padding=8)
        output.grid(row=3, column=0, sticky="nsew")
        output.columnconfigure(0, weight=1)
        output.rowconfigure(0, weight=1)
        self.results = tk.Text(output, state="disabled", font=("Consolas", 10))
        scrollbar = ttk.Scrollbar(output, command=self.results.yview)
        self.results.configure(yscrollcommand=scrollbar.set)
        self.results.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        ttk.Label(frame, textvariable=self.status).grid(row=4, column=0, sticky="w", pady=(10, 0))

    def choose_file(self):
        filename = filedialog.askopenfilename(
            title="Choose input text file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file = Path(filename)
            self.file_label.set(str(self.selected_file))
            self.status.set("Ready to extract emails.")

    def extract_emails(self):
        if not self.selected_file:
            messagebox.showwarning("Choose a file", "Please choose an input text file first.")
            return
        if not MAIN_SCRIPT.is_file():
            messagebox.showerror("main.py not found", f"Put your unchanged main.py beside this GUI file:\n{MAIN_SCRIPT}")
            return

        try:
            with tempfile.TemporaryDirectory() as temporary_folder:
                temporary_path = Path(temporary_folder)
                shutil.copyfile(self.selected_file, temporary_path / "input.txt")
                result = subprocess.run(
                    [sys.executable, str(MAIN_SCRIPT)],
                    cwd=temporary_path,
                    text=True,
                    capture_output=True,
                    check=True,
                )
                self.emails_text = (temporary_path / "emails.txt").read_text(encoding="utf-8")
        except (OSError, subprocess.CalledProcessError) as error:
            details = getattr(error, "stderr", "") or str(error)
            messagebox.showerror("Extraction failed", details)
            return

        self._display_results()
        count = len([line for line in self.emails_text.splitlines() if line])
        self.status.set(f"{count} email address{'es' if count != 1 else ''} extracted successfully.")
        self.save_button.configure(state="normal")

    def _display_results(self):
        self.results.configure(state="normal")
        self.results.delete("1.0", "end")
        self.results.insert("1.0", self.emails_text or "No email addresses found.")
        self.results.configure(state="disabled")

    def save_results(self):
        filename = filedialog.asksaveasfilename(
            title="Save email addresses", defaultextension=".txt", initialfile="emails.txt",
            filetypes=[("Text files", "*.txt")],
        )
        if filename:
            Path(filename).write_text(self.emails_text, encoding="utf-8")
            self.status.set(f"Results saved to {filename}")


if __name__ == "__main__":
    EmailExtractorGUI().mainloop()