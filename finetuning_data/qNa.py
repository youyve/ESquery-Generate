import json

# 读取questions.json文件
with open('questions.json', 'r', encoding='utf-8') as file:
    questions_data = json.load(file)

# 读取answers.json文件
with open('answers.json', 'r', encoding='utf-8') as file:
    answers_data = json.loads(file.read())  # 由于answers.json内容格式略有不同，使用json.loads()

# 确保问题和答案的数量相同
assert len(questions_data) == len(answers_data), "Questions and answers count do not match."

# 创建结构化的数据列表
structured_data = []
for question, answer in zip(questions_data, answers_data):
    structured_entry = {
        'question': question['question'],
        'answer': answer  # 假设answers.json中的数据是已经是所需的格式
    }
    structured_data.append(structured_entry)

# 写入结构化数据到新的json文件
with open('es_finetuning_data.json', 'w', encoding='utf-8') as file:
    json.dump(structured_data, file, ensure_ascii=False, indent=4)

print('Structured QA data has been saved to es_finetuning_data.json.')