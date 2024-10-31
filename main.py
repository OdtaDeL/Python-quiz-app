import pandas as pd
import tkinter as tk
from tkinter import messagebox
import random

# Đọc dữ liệu từ file Excel với đáp án nhiều lựa chọn

def load_questions(file_path):
    df = pd.read_excel(file_path)
    questions = []
    for _, row in df.iterrows():
        # Xử lý các lựa chọn trong cột "Options"
        options = {}
        for opt in row["Options"].split(";"):
            parts = opt.split(":")
            if len(parts) == 2:  # Kiểm tra mỗi lựa chọn có đúng 2 phần (A: Đáp án)
                options[parts[0].strip()] = parts[1].strip()
        
        # Xử lý đáp án đúng trong cột "Answer"
        answers = [ans.strip() for ans in row["Answer"].split(";")]

        question = {
            "question": row["Question"],  # Nội dung câu hỏi
            "options": options,           # Các lựa chọn
            "answer": answers             # Danh sách đáp án đúng
        }
        questions.append(question)
    
    random.shuffle(questions)  # Ngẫu nhiên thứ tự câu hỏi
    return questions

# Hiển thị câu hỏi
def display_question():
    global current_question, score, timer_countdown

    if current_question < len(questions):
        timer_countdown = 10  # Đặt lại đếm ngược 10 giây cho mỗi câu hỏi
        update_timer()

        question_label.config(text=questions[current_question]["question"])
        
        # Hiển thị các lựa chọn
        for widget in options_frame.winfo_children():
            widget.destroy()  # Xóa các lựa chọn cũ
        for key, value in questions[current_question]["options"].items():
            cb = tk.Checkbutton(options_frame, text=value, variable=selected_options[key], onvalue=True, offvalue=False)
            cb.pack(anchor="w")

        var_option.set(None)  # Đặt lại lựa chọn
    else:
        messagebox.showinfo("Kết quả", f"Bạn đã hoàn thành bài thi!\nĐiểm của bạn: {score}/{len(questions)}")
        root.quit()

# Kiểm tra đáp án và chuyển sang câu hỏi tiếp theo
def check_answer():
    global current_question, score, timer_countdown
    selected = [key for key, var in selected_options.items() if var.get()]
    correct_answer = questions[current_question]["answer"]
    if sorted(selected) == sorted(correct_answer):
        score += 1
    current_question += 1
    display_question()

# Cập nhật bộ đếm thời gian
def update_timer():
    global timer_countdown
    if timer_countdown > 0:
        timer_label.config(text=f"Thời gian: {timer_countdown} giây")
        timer_countdown -= 1
        root.after(1000, update_timer)
    else:
        check_answer()

# Cài đặt giao diện Tkinter
def start_quiz(file_path):
    global root, question_label, options_frame, var_option, current_question, score, questions, timer_label, timer_countdown, selected_options

    # Khởi tạo các biến
    root = tk.Tk()
    root.title("Phần mềm trắc nghiệm")
    questions = load_questions(file_path)
    current_question = 0
    score = 0
    var_option = tk.StringVar()

    # Hiển thị câu hỏi và các lựa chọn
    question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
    question_label.pack(pady=20)

    options_frame = tk.Frame(root)
    options_frame.pack(pady=10)
    
    selected_options = {opt: tk.BooleanVar() for opt in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}

    # Nút xác nhận
    submit_button = tk.Button(root, text="Xác nhận", command=check_answer)
    submit_button.pack(pady=10)

    # Hiển thị bộ đếm thời gian
    timer_label = tk.Label(root, text="", font=("Arial", 12))
    timer_label.pack(pady=5)

    display_question()  # Bắt đầu với câu hỏi đầu tiên
    root.mainloop()

# Chạy ứng dụng với file Excel đầu vào
if __name__ == "__main__":
    # Đặt đường dẫn file Excel vào đây
    file_path = ""
    start_quiz(file_path)
