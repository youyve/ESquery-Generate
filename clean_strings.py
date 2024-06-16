import json
import re

def process_json(input_file_path, output_file_path):
    # 读取 JSON 文件
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            # 将文件内容加载到变量中，假设原始文件是一个 JSON 数组
            json_strings = json.load(file)
            
            # 准备一个空列表以存储处理后的字符串
            processed_json_strings = []

            # 遍历原始 JSON 数组中的每个字符串
            for json_str in json_strings:
                # 移除第一个 "{" 之前的所有字符
                json_str = re.sub(r'^[^{]*', '', json_str)
                # 移除最后一个 "}" 之后的所有字符
                json_str = re.sub(r'[^}]*$', '', json_str)

                # 将处理后的字符串添加到列表中
                processed_json_strings.append(json_str)
            
            # 打印成功信息
            print('所有 JSON 对象已经被处理和清理。')
            
            # 将处理后的 JSON 对象列表写入到新的 JSON 文件中
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                json.dump(processed_json_strings, output_file, ensure_ascii=False, indent=4)
                
            print(f"处理后的 JSON 数据已保存到 {output_file_path}")

    except FileNotFoundError:
        print(f"文件 {input_file_path} 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")


input_path = 'optimize_queries/query_qwen14b.json'
output_path = 'optimize_queries/strict_queries/query_qwen14b.json'
process_json(input_path, output_path)