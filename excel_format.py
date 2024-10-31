import re
import pandas as pd

def parse_text_file(file_path):
    questions = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    question = {}
    options = {}
    for line in lines:
        line = line.strip()
        
        # Tìm câu hỏi và số lượng đáp án đúng
        if match := re.match(r"^\d+\.\)\s*(.*?)(Chose\s*(\d+)\s*answers)?$", line):
            if question:
                # Lưu câu hỏi trước đó vào danh sách
                question["options"] = options
                questions.append(question)
                options = {}

            question = {
                "question": match.group(1).strip(),
                "num_answers": int(match.group(3)) if match.group(3) else 1,
                "answers": []  # Danh sách đáp án đúng
            }
        
        # Tìm đáp án lựa chọn (A, B, C,...)
        elif opt_match := re.match(r"^([A-Z])\.\s*(.*)", line):
            opt_letter = opt_match.group(1).strip()
            options[opt_letter] = opt_match.group(2).strip()
        
        # Tìm đáp án đúng (dòng cuối mỗi câu hỏi)
        elif re.match(r"^[A-Z](,\s*[A-Z])*", line):
            question["answers"] = [ans.strip() for ans in line.split(",")]

    # Thêm câu hỏi cuối cùng vào danh sách (nếu có)
    if question:
        question["options"] = options
        questions.append(question)

    return questions

def save_to_excel(questions, output_path="output_questions.xlsx"):
    data = {
        "Question": [],
        "Options": [],
        "Answer": []
    }
    for question in questions:
        data["Question"].append(question["question"])
        
        # Định dạng các lựa chọn theo "A: Option A; B: Option B; ..."
        options_str = "; ".join([f"{key}: {value}" for key, value in question["options"].items()])
        data["Options"].append(options_str)
        
        # Thêm danh sách đáp án đúng
        correct_answers = "; ".join(question["answers"])
        data["Answer"].append(correct_answers)

    # Tạo DataFrame và lưu vào file Excel
    df = pd.DataFrame(data)
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Đã lưu file Excel tại: {output_path}")

# Sử dụng hàm trên
if __name__ == "__main__":
    text_file_path = ""  # Đặt đường dẫn tới file text của bạn
    questions = parse_text_file(text_file_path)
    save_to_excel(questions, "Questions.xlsx") #Đặt tên file Excel
