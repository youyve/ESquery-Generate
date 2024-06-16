from elasticsearch import Elasticsearch
from es_results import process_query
import json
import os

# 定义Elasticsearch连接参数
host = '10.6.51.206'
port = 9200
user = 'elastic'
passwd = 'gdiist2024'
index_name = 'arxiv_papers_2023cs'

# 创建Elasticsearch客户端
es = Elasticsearch(
    [{'host': host, 'port': port, "scheme": "http"}],
    basic_auth=(user, passwd)
)

# ES查询语句所在的文件夹
queries_folder = '../optimize_queries/strict_queries/'
# 存放查询结果的文件夹
results_folder = '../queries_result/'

# 读取和保存的文件名
filename = 'query_qwen14b.json'

# 确保results文件夹存在
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

queries_path = os.path.join(queries_folder, filename)
results_path = os.path.join(results_folder, filename)

# Load your query.json file
with open(queries_path, 'r') as file:
    query_list = json.load(file)

with open('../question.json', 'r') as file:
    questions_list = json.load(file)

successful_queries = []
failed_queries = []

# 打开文件准备写入结果
with open(results_path, 'w', encoding='utf-8') as file:
    query_results = []
    for query_str, question_str in zip(query_list, questions_list):
        try:
            query = json.loads(query_str)
            result = process_query(index=index_name, options=query)
            hits = result['hits']['hits']
            
            # 准备要写入的数据
            result_data = {
                "question": question_str,
                "results": []
            }
            
            # 添加查询结果
            for hit in hits:
                doc = hit['_source']
                result_data['results'].append({
                    "文章ID": hit['_id'],
                    "标题": doc['title'],
                    "作者": ', '.join(doc['author']),
                    "发布日期": doc['date'],
                    "摘要": doc['abstract'],
                    "链接": doc['absurl'],
                })
            
            # 将当前问题及其查询结果添加到列表中
            query_results.append(result_data)
            
            # 记录成功的查询
            successful_queries.append(query_str)
            
        except Exception as e:
            failed_queries.append((query_str, str(e)))

    # 将所有查询结果写入到JSON文件
    json.dump(query_results, file, ensure_ascii=False, indent=4)
    
    print("将所有能够成功查询的结果及其对应的问题保存到指定json文件中")


# Output the results
print(f'Successful queries count: {len(successful_queries)}')
print(f'Failed queries count: {len(failed_queries)}')

# 直接在终端中显示查询失败的语句及其报错
# for failed_query, error in failed_queries:
#     print(f'Failed query: {failed_query}')
#     print(f'Error message: {error}')
#     print('-' * 60)

# 将可以成功查询的es语句按照数组的结构写入文件
# with open('successful_queries.json', 'w', encoding='utf-8') as file:
#     json.dump(successful_queries, file, ensure_ascii=False, indent=4)

# 将可以成功查询的es语句对应的问题按照数组的结构写入文件
# with open('corresponding_questions.json', 'w', encoding='utf-8') as file:
#     json.dump(corresponding_questions, file, ensure_ascii=False, indent=4)

# print("可以成功查询的语句已保存到文件 successful_queries.json")
# print("对应的问题已经保存到文件 corresponding_questions.json")

