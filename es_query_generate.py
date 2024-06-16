import json
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',
)

def generate_es_query_for_user_query(user_query):
    # Generate the ES search query using the translated English query
    prompt = f"Translate the following user query into an ES search query,using technique such as using less restrictive query, expanding the search scope etc to increase the recall rate of the search: '{user_query}'.the ES index field contain 'author','date', title','abstract'.If the user query is not English, translate it into english first. Only return the final json result, no explanation or other texts."
    
    response = client.chat.completions.create(
        model="codegemma:2b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    es_search_query = response.choices[0].message.content.strip()
    return es_search_query

# Load the questions from the JSON file
with open('question.json', 'r', encoding='utf-8') as file:
    questions = json.load(file)

# Generate ES search queries for each question
es_queries = []
for question in questions:
    es_query = generate_es_query_for_user_query(question['question'])
    es_queries.append(es_query)

# Write the generated ES queries to a JSON file
with open('query_codegemma2b.json', 'w', encoding='utf-8') as file:
    json.dump(es_queries, file, ensure_ascii=False, indent=4)

print('ES queries have been generated and saved to query.json.')