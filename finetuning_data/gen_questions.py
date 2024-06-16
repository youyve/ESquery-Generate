import json
import os
from openai import OpenAI
from tqdm import tqdm

# 初始化OpenAI客户端
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# 生成问题的函数
def generate_user_query(prompt):
    try:
        # 发送请求到OpenAI API
        response = client.chat.completions.create(
            model="anthropic/claude-3-sonnet",
            messages=[
                {"role": "system", "content": "你是一个数据生成专家。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        # 解析响应并提取生成的问题
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error while generating question: {e}")
        return None

# 构建prompt
base_prompt = (
    "请根据以下示例问题，生成一个关注于检索人工智能领域特定研究主题的问题。"
    "确保问题简洁且问题尽量以文献、论文、文章和研究等词汇结尾。\n\n"
    "示例问题：\n"
    "- 与大模型工具学习相关论文\n"
    "- 查找OCR文本检测最新进展\n"
    "- 近一个月与多模态大模型相关论文\n"
    "只用给出一个问题不要生成其他任何内容"
)

# 储存生成的问题
generated_questions = set()

# 生成问题并添加到集合中，直到达到3000个
while len(generated_questions) < 3000:
    new_question = generate_user_query(base_prompt)
    if new_question and new_question not in generated_questions:
        generated_questions.add(new_question)
        print(f"Generated question {len(generated_questions)}: {new_question}")

# 保存生成的问题到JSON文件
output_json_path = './generated_ai_questions.json'
with open(output_json_path, 'w', encoding='utf-8') as file:
    json.dump(list(generated_questions), file, ensure_ascii=False, indent=2)

print(f"3000 unique AI-related questions have been generated and saved to {output_json_path}")