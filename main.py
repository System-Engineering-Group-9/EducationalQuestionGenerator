import json
import tkinter as tk
from tkinter import ttk, messagebox

from app.ai.enums.subject import Subject
from app.ai.questionGenerator import QuestionGenerator


class TopicFrame(ttk.Frame):
    def __init__(self, parent, remove_callback):
        super().__init__(parent)
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, padx=(0, 5))
        self.remove_btn = ttk.Button(self, text="X", width=2, command=lambda: remove_callback(self))
        self.remove_btn.pack(side=tk.LEFT)

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

    topics = [frame.entry.get().strip() for frame in topic_frames if frame.entry.get().strip()]
    age_group = age_group_entry.get()

    if not age_group:
        messagebox.showerror("Error", "Age Group cannot be empty.")
        return

    result_text.set("Generating questions...\nIt may take a minute to generate quiz questions.")
    root.update_idletasks()

    all_questions = []
    try:
        if topics:
            for topic in topics:
                questions = genAi.generateQuestions(number, subject, age_group, topic)
                all_questions.extend(questions)
        else:
            questions = genAi.generateQuestions(number, subject, age_group)
            all_questions.extend(questions)
        result_text.set("Finished generating questions!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return

    with open("output.json", "w") as file:
        file.write(json.dumps([question.__dict__ for question in all_questions], indent=4))

    messagebox.showinfo("Success", "Questions generated and saved to output.json!")


def add_topic_field():
    frame = TopicFrame(topics_container, remove_topic_field)
    frame.pack(pady=2)
    topic_frames.append(frame)


def remove_topic_field(frame):
    frame.destroy()
    topic_frames.remove(frame)

if __name__ == "__main__":
    genAi = QuestionGenerator()
    topic_frames = []

    root = tk.Tk()
    root.title("Quiz Question Generator")
    root.geometry("450x500")
    root.configure(bg="#f0f0f0")

    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#4CAF50", font=("Arial", 10, "bold"))
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TEntry", padding=5)
    style.configure("TCombobox", padding=5)

    ttk.Label(root, text="Number of questions (1-5):", background="#f0f0f0").pack(pady=5)
    num_questions = ttk.Entry(root)
    num_questions.pack()

    ttk.Label(root, text="Subject:", background="#f0f0f0").pack(pady=5)
    subject_var = tk.StringVar()
    subject_menu = ttk.Combobox(root, textvariable=subject_var, values=[s.name for s in Subject])
    subject_menu.pack()

    # Topics section
    ttk.Label(root, text="Topics (Optional):", background="#f0f0f0").pack(pady=5)
    topics_container = ttk.Frame(root)
    topics_container.pack(pady=5)

    add_topic_btn = ttk.Button(root, text="Add Topic", command=add_topic_field)
    add_topic_btn.pack(pady=5)

    ttk.Label(root, text="Age Group:", background="#f0f0f0").pack(pady=5)
    age_group_entry = ttk.Entry(root)
    age_group_entry.pack()

    generate_button = ttk.Button(root, text="Generate Questions", command=generate_questions)
    generate_button.pack(pady=15)

    result_text = tk.StringVar()
    status_label = ttk.Label(root, textvariable=result_text, background="#f0f0f0", font=("Arial", 10, "italic"))
    status_label.pack()

    root.mainloop()