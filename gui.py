import re
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class EmailExtractorApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Email Extractor Pro")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)

        self.input_file_path = ""
        self.output_file_path = ""

        self.setup_ui()

    def setup_ui(self):
        # Main frame with padding
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="📧 Email Extractor Pro",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(20, 30))

        # Input File Section
        input_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        input_frame.pack(padx=20, pady=10, fill="x")

        input_label = ctk.CTkLabel(
            input_frame,
            text="Input File:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        input_label.pack(padx=15, pady=(15, 5), anchor="w")

        self.input_path_label = ctk.CTkLabel(
            input_frame,
            text="No file selected",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.input_path_label.pack(padx=15, pady=(0, 10), anchor="w")

        input_button = ctk.CTkButton(
            input_frame,
            text="📁 Select Input File",
            command=self.select_input_file,
            height=40,
            corner_radius=8
        )
        input_button.pack(padx=15, pady=(0, 15), fill="x")

        # Output File Section
        output_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        output_frame.pack(padx=20, pady=10, fill="x")

        output_label = ctk.CTkLabel(
            output_frame,
            text="Output File:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        output_label.pack(padx=15, pady=(15, 5), anchor="w")

        self.output_path_label = ctk.CTkLabel(
            output_frame,
            text="Default: emails.txt",
            text_color="gray",
            font=ctk.CTkFont(size=12)
        )
        self.output_path_label.pack(padx=15, pady=(0, 10), anchor="w")

        output_button = ctk.CTkButton(
            output_frame,
            text="💾 Select Output Location",
            command=self.select_output_file,
            height=40,
            corner_radius=8
        )
        output_button.pack(padx=15, pady=(0, 15), fill="x")

        # Extract Button
        extract_button = ctk.CTkButton(
            main_frame,
            text="🚀 Extract Emails",
            command=self.extract_emails,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        extract_button.pack(padx=20, pady=20, fill="x")

        # Results Section
        results_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        results_frame.pack(padx=20, pady=10, fill="both", expand=True)

        results_label = ctk.CTkLabel(
            results_frame,
            text="Results:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        results_label.pack(padx=15, pady=(15, 10), anchor="w")

        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=ctk.CTkFont(family="Consolas", size=11),
            corner_radius=8
        )
        self.results_text.pack(padx=15, pady=(0, 15), fill="both", expand=True)

        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready",
            text_color="gray",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.pack(pady=(5, 15))

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.input_file_path = file_path
            self.input_path_label.configure(
                text=os.path.basename(file_path),
                text_color="black"
            )
            self.status_label.configure(text=f"Input selected: {os.path.basename(file_path)}")

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Save Extracted Emails",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("All Files", "*.*")
            ],
            initialfile="emails.txt"
        )
        if file_path:
            self.output_file_path = file_path
            self.output_path_label.configure(
                text=os.path.basename(file_path),
                text_color="black"
            )
            self.status_label.configure(text=f"Output: {os.path.basename(file_path)}")

    def extract_emails(self):
        if not self.input_file_path:
            messagebox.showwarning("Warning", "Please select an input file first!")
            return

        try:
            self.status_label.configure(text="Extracting emails...")
            self.results_text.delete("1.0", "end")

            # Original extraction code
            with open(self.input_file_path, "r", encoding="utf-8") as file:
                text = file.read()

            emails = re.findall(r"[\w.-]+@[\w.-]+\.\w+", text)
            unique_emails = list(dict.fromkeys(emails))

            # Display results
            self.results_text.insert("1.0", f"Found {len(unique_emails)} unique emails:\n\n")
            for email in unique_emails:
                self.results_text.insert("end", f"• {email}\n")

            # Save to file
            output_path = self.output_file_path if self.output_file_path else "emails.txt"
            with open(output_path, "w", encoding="utf-8") as file:
                for email in unique_emails:
                    file.write(email + "\n")

            self.status_label.configure(
                text=f"✓ {len(unique_emails)} emails extracted and saved!",
                text_color="#2E8B57"
            )
            messagebox.showinfo(
                "Success",
                f"{len(unique_emails)} email addresses extracted successfully!\nSaved to: {output_path}"
            )

        except FileNotFoundError:
            messagebox.showerror("Error", "Input file not found!")
            self.status_label.configure(text="Error: File not found", text_color="red")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = EmailExtractorApp()
    app.run()
