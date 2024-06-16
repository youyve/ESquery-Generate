import json
from openai import OpenAI
import os
from os import getenv
from tqdm import tqdm

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=getenv("OPENROUTER_API_KEY"),
)

# 评分文章与给定问题相关性的函数
def score_relevance(question, abstract):
    try:
        prompt=(
            f"针对研究问题 '{question}'，以下论文摘要的相关性如何？请从0到100打分。\n\n摘要：{abstract}"
            f"只给出分数，不要输出任何解释"
        )

        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.5,
        )
        score = float(response.choices[0].message.content.strip())
        return score
    except Exception as e:
        print(f"无法评分，错误信息：{e}")
        return 0.0
# 存放查询结果的文件夹
results_folder = '../queries_result/'
record_folder = '../record/'
# 只用改这里即可
name = 'query_mistral7b'

# 读取的文件名
filename = f'{name}.json'
# 保存中间结果的文件名
filename_process = f'{name}.txt'

# 确保results文件夹存在
if not os.path.exists(record_folder):
    os.makedirs(record_folder)

results_path = os.path.join(results_folder, filename)
record_path = os.path.join(record_folder, filename_process)

# 加载JSON数据
with open(results_path, 'r') as file:
    data = json.load(file)

# 处理每个问题和结果
total_average_scores = []  # 用于存储所有问题的平均得分

# 将中间输出记录保存到文件中
with open(record_path, 'w', encoding='utf-8') as f:
    for item in tqdm(data, desc="处理中"):
        question = item["question"]["question"]
        results = item["results"]
        
        if results:
            scores = [score_relevance(question, result["摘要"]) for result in results]
            average_score = sum(scores) / len(scores)
            f.write(f"问题: '{question}' 的平均相关性得分为: {average_score:.2f}\n")
        else:
            average_score = 0.0
            f.write(f"问题: '{question}' 没有结果，得分为 0\n")

        # 存储每个问题的平均得分用于计算总平均分
        total_average_scores.append(average_score)
    
    # 计算所有问题的平均分的总平均分
    if total_average_scores:
        overall_average_score = sum(total_average_scores) / len(total_average_scores)
        f.write(f"所有问题的平均相关性得分的总平均分为: {overall_average_score:.2f}\n")
        print(f"所有问题的平均相关性得分的总平均分为: {overall_average_score:.2f}")
    else:
        f.write("没有问题的得分可用于计算总平均分。\n")
        print("没有问题的得分可用于计算总平均分。")