import json
import tkinter as tk
from tkinter import ttk, messagebox

from app.ai.enums.subject import Subject
from app.ai.questionGenerator import QuestionGenerator


def generate_questions():
    try:
        number = int(num_questions.get())
        if number < 1 or number > 5:
            raise ValueError("Number out of range")
    except ValueError:
        messagebox.showerror("Error", "Please enter a number between 1 and 5.")
        return

    try:
        subject = Subject(subject_var.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid subject.")
        return

    item = item_entry.get().strip()
    age_group = age_group_entry.get()

    if not age_group:
        messagebox.showerror("Error", "Age Group cannot be empty.")
        return

    # Initialize the question generator
    result_text.set("Generating questions...\nIt may take a minute to generate quiz questions.")
    root.update_idletasks()

    try:
        questions = genAi.generateQuestions(number, subject, age_group, item if item else None)
        result_text.set("Finished generating questions!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    # Save to JSON
    with open("output.json", "w") as file:
        file.write(json.dumps([question.__dict__ for question in questions], indent=4))

    messagebox.showinfo("Success", "Questions generated and saved to output.json!")


if __name__ == "__main__":
    # Initialize the Question Generator
    genAi = QuestionGenerator()

    # Create main window
    root = tk.Tk()
    root.title("Quiz Question Generator")
    root.geometry("450x350")
    root.configure(bg="#f0f0f0")

    # Styling
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 10, "bold"))
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TEntry", padding=5)
    style.configure("TCombobox", padding=5)

    # Number of Questions
    ttk.Label(root, text="Number of questions (1-5):", background="#f0f0f0").pack(pady=5)
    num_questions = ttk.Entry(root)
    num_questions.pack()

    # Subject
    ttk.Label(root, text="Subject:", background="#f0f0f0").pack(pady=5)
    subject_var = tk.StringVar()
    subject_menu = ttk.Combobox(root, textvariable=subject_var, values=[s.name for s in Subject])
    subject_menu.pack()

    # Item (Optional)
    ttk.Label(root, text="Item (Optional):", background="#f0f0f0").pack(pady=5)
    item_entry = ttk.Entry(root)
    item_entry.pack()

    # Age Group
    ttk.Label(root, text="Age Group:", background="#f0f0f0").pack(pady=5)
    age_group_entry = ttk.Entry(root)
    age_group_entry.pack()

    # Generate Button
    generate_button = ttk.Button(root, text="Generate Questions", command=generate_questions)
    generate_button.pack(pady=15)

    # Status Label
    result_text = tk.StringVar()
    status_label = ttk.Label(root, textvariable=result_text, background="#f0f0f0", font=("Arial", 10, "italic"))
    status_label.pack()

    # Run the application
    root.mainloop()
