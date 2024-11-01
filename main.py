import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Đọc dữ liệu từ file Excel với đáp án nhiều lựa chọn
def load_questions(file_path):
    df = pd.read_excel(file_path)
    questions = []
    for _, row in df.iterrows():
        options = {}
        for opt in row["Options"].split(";"):
            parts = opt.split(":")
            if len(parts) == 2:  # Kiểm tra mỗi lựa chọn có đúng 2 phần (A: Đáp án)
                options[parts[0].strip()] = parts[1].strip()
        
        answers = [ans.strip() for ans in row["Answer"].split(";")]
        question = {
            "question": row["Question"],
            "options": options,
            "answer": answers,
            "num_answers": len(answers)  # Số đáp án đúng
        }
        questions.append(question)
    
    random.shuffle(questions)  # Ngẫu nhiên thứ tự câu hỏi
    return questions

# Hiển thị câu hỏi
def display_question():
    global current_question, score, timer_countdown, user_answers, timer_job

    if current_question < num_questions:
        # Hủy job đếm ngược cũ nếu tồn tại
        if timer_job:
            root.after_cancel(timer_job)

        timer_countdown = 60  # Đặt lại đếm ngược 60 giây cho mỗi câu hỏi
        update_timer()

        question_label.config(text=questions[current_question]["question"])
        for widget in options_frame.winfo_children():
            widget.destroy()  # Xóa các lựa chọn cũ

        selected_options.clear()
        
        # Hiển thị các lựa chọn với loại câu hỏi đơn hoặc nhiều đáp án
        if questions[current_question]["num_answers"] > 1:
            for key, value in questions[current_question]["options"].items():
                var = tk.BooleanVar()
                cb = tk.Checkbutton(options_frame, text=value, variable=var)
                cb.pack(anchor="w")
                selected_options[key] = var
        else:
            for key, value in questions[current_question]["options"].items():
                var_option.set(None)  # Đặt lại lựa chọn
                rb = tk.Radiobutton(options_frame, text=value, variable=var_option, value=key)
                rb.pack(anchor="w")

    else:
        # Hiển thị kết quả sau khi hoàn thành
        show_results()

# Kiểm tra đáp án và chuyển sang câu hỏi tiếp theo
def check_answer():
    global current_question, score, user_answers

    if questions[current_question]["num_answers"] > 1:
        selected = [key for key, var in selected_options.items() if var.get()]
    else:
        selected = [var_option.get()]

    correct_answer = questions[current_question]["answer"]
    selected_content = [questions[current_question]["options"].get(ans, "") for ans in selected]
    correct_content = [questions[current_question]["options"].get(ans, "") for ans in correct_answer]

    # Lưu thông tin câu trả lời cho thống kê
    user_answers.append({
        "question": questions[current_question]["question"],
        "user_answer": selected,
        "user_answer_content": selected_content,
        "correct_answer": correct_answer,
        "correct_answer_content": correct_content
    })

    # Kiểm tra đúng sai và tăng điểm số
    if sorted(selected) == sorted(correct_answer):
        score += 1

    current_question += 1
    display_question()

# Cập nhật bộ đếm thời gian
def update_timer():
    global timer_countdown, timer_job
    if timer_countdown > 0:
        timer_label.config(text=f"Thời gian: {timer_countdown} giây")
        timer_countdown -= 1
        timer_job = root.after(1000, update_timer)  # Gọi hàm lại sau 1 giây
    else:
        check_answer()

# Hiển thị kết quả sau bài kiểm tra
def show_results():
    result_message = f"Bạn đã hoàn thành bài thi!\nĐiểm của bạn: {score}/{num_questions}\n\n"
    result_message += "Chi tiết câu hỏi và đáp án:\n"
    for i, answer in enumerate(user_answers, 1):
        result_message += f"Câu {i}: {answer['question']}\n"
        result_message += f"  Đáp án của bạn: {', '.join(answer['user_answer'])} ({', '.join(answer['user_answer_content'])})\n"
        result_message += f"  Đáp án đúng: {', '.join(answer['correct_answer'])} ({', '.join(answer['correct_answer_content'])})\n\n"

    messagebox.showinfo("Kết quả", result_message)
    root.quit()

# Cài đặt giao diện Tkinter
def start_quiz(file_path):
    global root, question_label, options_frame, var_option, current_question, score, questions, timer_label, timer_countdown, selected_options, user_answers, num_questions, timer_job

    # Khởi tạo các biến
    root = tk.Tk()
    root.title("Phần mềm trắc nghiệm")
    questions = load_questions(file_path)

    # Chọn số lượng câu hỏi
    max_questions = len(questions)
    num_questions = simpledialog.askinteger("Số lượng câu hỏi", f"Chọn số câu hỏi (tối đa {max_questions}):", minvalue=1, maxvalue=max_questions)
    if not num_questions:
        root.destroy()
        return

    questions = questions[:num_questions]  # Chọn số lượng câu hỏi theo yêu cầu
    current_question = 0
    score = 0
    var_option = tk.StringVar()
    user_answers = []
    selected_options = {}
    timer_job = None  # Khởi tạo biến để lưu job đếm thời gian

    # Hiển thị câu hỏi và các lựa chọn
    question_label = tk.Label(root, text="", font=("Arial", 14), wraplength=400)
    question_label.pack(pady=20)

    options_frame = tk.Frame(root)
    options_frame.pack(pady=10)

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
    file_path = "AWS_Questions.xlsx"  # Đặt đường dẫn tới file Excel của bạn
    start_quiz(file_path)
