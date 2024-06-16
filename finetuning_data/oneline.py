import json

# 读取输入的JSON文件
input_file_path = './unique_questions_3000.json'
# 输出文件的路径
output_file_path = './unique_questions_3000_1.json'

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    questions = json.load(input_file)  # 加载JSON数据

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    # 先写入一个开头中括号
    output_file.write('[\n')
    # 对于questions列表中的每个问题对象，除了最后一个外
    for question in questions[:-1]:
        # 将每个问题对象转换为一个JSON字符串，不添加额外的空格或缩进
        question_str = json.dumps(question, ensure_ascii=False)
        # 将每个JSON字符串写入文件的一行中，并在末尾添加逗号和换行符
        output_file.write(f'{question_str},\n')
    # 最后一个问题对象后面不需要逗号
    last_question_str = json.dumps(questions[-1], ensure_ascii=False)
    output_file.write(last_question_str + '\n')
    # 写入结束的中括号
    output_file.write(']\n')

print(f'Done. The questions have been written to {output_file_path}.')