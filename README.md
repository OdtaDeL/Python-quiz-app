
# Project Title

A brief description of what this project does and who it's for

# Python-quiz-app
Working
# Quiz Application - Python with Text and Excel Parsing

This project is a Python-based quiz application that loads questions from either a text or Excel file and allows users to take a quiz with a graphical interface. The application supports single-choice and multiple-choice questions, and can shuffle questions and options for each run.

## Features

- **Load Questions from Text File**: Supports a specific format to parse questions, options, and correct answers from a text file.
- **Load Questions from Excel File**: Reads questions formatted in Excel with columns for question content, options, and correct answers.
- **Graphical Quiz Interface**: A GUI built with `tkinter` that displays questions, tracks time for each question, and calculates scores.
- **Randomized Question Order**: Questions and options are shuffled to create a unique quiz experience each time.
- **Answer Time Limit**: Set a time limit for each question to increase the challenge.

## Requirements

To run this project, you need:

- Python 3.x
- `pandas` library for handling Excel files
- `openpyxl` library for Excel file I/O with `.xlsx` format

Install the dependencies using:
```bash
pip install pandas openpyxl

# Quiz Application - Python with Text and Excel Parsing

This project is a Python-based quiz application that loads questions from either a text or Excel file and allows users to take a quiz with a graphical interface. The application supports single-choice and multiple-choice questions, and can shuffle questions and options for each run.

## Features

- **Load Questions from Text File**: Supports a specific format to parse questions, options, and correct answers from a text file.
- **Load Questions from Excel File**: Reads questions formatted in Excel with columns for question content, options, and correct answers.
- **Graphical Quiz Interface**: A GUI built with `tkinter` that displays questions, tracks time for each question, and calculates scores.
- **Randomized Question Order**: Questions and options are shuffled to create a unique quiz experience each time.
- **Answer Time Limit**: Set a time limit for each question to increase the challenge.


To run this project, you need:

- Python 3.x
- `pandas` library for handling Excel files
- `openpyxl` library for Excel file I/O with `.xlsx` format

Install the dependencies using:
```bash
pip install pandas openpyxl

File Format
1. Text File Format
Each question in the text file should follow this format:
1.) What AWS services can be used to store files? Choose 2 answers from the options below.

A. Amazon Cloud Watch
B. Amazon Simple Storage Service (Amazon S3)
C. Amazon Elastic Block Store (Amazon EBS)
D. AWS Config
E. Amazon Athena

B, C

Question Line: Starts with a number and .).
Options: Each option begins with a letter (A, B, etc.) followed by a dot and the option text.
Correct Answers: The last line for each question block contains the correct answers, separated by commas.

The Excel file should contain the following columns:
Question: The text of the question.
Options: Each option is prefixed by a letter and separated by ;.
Answer: The correct answer(s), separated by ; for multiple answers.
