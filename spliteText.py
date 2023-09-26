import os
import re

# Revised code based on testing results and suggestions

def create_folder(filename):
    base_dir = os.path.dirname(os.path.realpath(filename))
    base_name = os.path.splitext(os.path.basename(filename))[0]
    new_folder = os.path.join(base_dir, base_name + "split")
    os.makedirs(new_folder, exist_ok=True)
    return new_folder

def detect_language(text):
    if re.search("[\u4e00-\u9FFF]", text):
        return "chinese"
    else:
        return "english"

def split_by_length(text, length):  # Added function for splitting long Chinese paragraphs
    return [text[i:i+length] for i in range(0, len(text), length)]

def split_text(filename, new_folder):
    base_name = os.path.basename(os.path.splitext(filename)[0])

    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    paragraphs = text.split('\n')

    language = detect_language(text)  # Moved language detection here to check only once

    split_texts = []
    current_text = ""
    for paragraph in paragraphs:
        if language == "chinese":
            if len(paragraph) < 750:
                if len(current_text) + len(paragraph) < 750:
                    current_text += paragraph + "\n"
                else:
                    split_texts.append(current_text.strip())
                    current_text = paragraph + "\n"
            else:
                for sub_para in split_by_length(paragraph, 750):
                    split_texts.append(sub_para)

        elif language == "english":
            word_count = len(paragraph.split())
            if word_count < 350:
                if len(current_text.split()) + word_count < 350:
                    current_text += paragraph + "\n"
                else:
                    split_texts.append(current_text.strip())
                    current_text = paragraph + "\n"
            else:
                words = paragraph.split()
                while words:
                    chunk = words[:350]
                    split_texts.append(" ".join(chunk))
                    words = words[350:]

    if current_text:
        split_texts.append(current_text.strip())

    file_count = 0
    for index, split_text in enumerate(split_texts):
        new_filename = os.path.join(new_folder, base_name + "split" + str(index + 1).zfill(2) + ".txt")
        with open(new_filename, 'w', encoding='utf-8') as file:
            file.write(split_text)
        file_count += 1

    return file_count

def main_split_text(filename):
    new_folder = create_folder(filename)
    file_count = split_text(filename, new_folder)
    return new_folder, file_count


def main(filename):
    new_folder = create_folder(filename)
    split_text(filename, new_folder)
    file_count = split_text(filename, new_folder)
    return new_folder , file_count

def run_script():
    try:
        filename = input("请输入文件名（包括扩展名）：")
        new_folder, file_count = main_split_text(filename)
        print(f"切分完成！新文件夹为：{new_folder}，包含 {file_count} 个文件。")
    except Exception as e:
        print(f"发生错误：{e}")

# This block ensures the code runs only when the script is executed directly, not when imported
if __name__ == "__main__":
    run_script()