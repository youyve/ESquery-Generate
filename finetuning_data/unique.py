import json

# 输入文件路径
input_file_path = './questions_3000.json'
# 输出文件路径
output_file_path = './unique_questions_3000.json'

# 读取JSON文件
with open(input_file_path, 'r', encoding='utf-8') as file:
    # 加载所有问题对象
    questions = json.load(file)

# 使用集合来存储唯一的问题
unique_questions_set = set()
# 创建一个新的列表来存储唯一的问题对象
unique_questions = []

for question_obj in questions:
    # 获取question字段的值
    question_text = question_obj['question']
    # 检查这个问题是否已经在集合中
    if question_text not in unique_questions_set:
        # 如果不在集合中，添加到集合和列表中
        unique_questions_set.add(question_text)
        unique_questions.append(question_obj)

# 将唯一的问题列表写回到一个新的JSON文件
with open(output_file_path, 'w', encoding='utf-8') as file:
    json.dump(unique_questions, file, ensure_ascii=False, indent=4)

print(f'Done. Unique questions have been written to {output_file_path}.')