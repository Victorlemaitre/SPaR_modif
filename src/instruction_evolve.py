import requests
import multiprocessing
from multiprocessing import Manager
import json
from tqdm import tqdm
import os
import time
# import pandas as pd
import random

API_KEY = 'your_api_key_here'  # Replace with your actual API key

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

API_URL = "https://api.openai.com/v1/chat/completions"  # OpenAI API endpoint for chat completions


def chat_gpt(messages, counter, error_count):
    responses = []
    for i, m in enumerate(messages):
        try:
            message = m['message']
            # print(message)
            # assert False
            # data = json.dumps({"model": "gpt-4o-2024-05-13", "messages": message, "temperature": 0.3})
            data = json.dumps({"model": "gpt-4o-mini-2024-07-18", "messages": message, "temperature": 0.7})
            response = requests.post(API_URL, headers=HEADERS, data=data)
            response_json = response.json()
            print(response_json)
            res = response_json['choices'][0]['message']['content']
            m['response'] = res
            # 保存响应到文件
            with open(output_file, 'a', encoding='utf-8') as f:
                print(json.dumps(m, ensure_ascii=False), file=f)

            responses.append(response_json)

            # Increment and print the counter
            counter.value += 1
        except Exception as e:
            error_count.value += 1
            print(e)
        print('running time:{} finished number:{} skipped number:{}'.format(time.time()-s_time, counter.value, error_count.value), end='\r')
        # print(f'Messages stored: {counter.value}', time.time()-s_time, end='\r')

    return responses


def multi_process_chat_gpt(messages_list, num_processes):
    # 将messages_list分为num_processes个子列表
    sublists = [messages_list[i::num_processes] for i in range(num_processes)]

    # Create a shared counter
    manager = Manager()
    counter = manager.Value('i', 0)
    error_count = manager.Value('j', 0)

    with multiprocessing.Pool() as pool:
        all_responses = pool.starmap(chat_gpt, [(sublist, counter, error_count) for sublist in sublists])
    # 将所有响应合并为一个列表
    return [item for sublist in all_responses for item in sublist]



def get_messages_list():
    evaluated = []
    with open(output_file, encoding='utf-8') as f:
        lines = f.readlines()[:]
    for i in lines:
        evaluated.append(json.loads(i)['origin'])

    with open(input_file, encoding='utf-8') as f:
        d = json.load(f)[:]

    messages_list = []

    cons = [
"""  - Length: 
    * Number of characters
    * Words
    * Sentences
    * Paragraphs
    * Sections""",
"""  - Text format: 
    * JSON
    * Markdown
    * List
    * Table
    * Bullets
    * Postscript""",
"""  - Character format: 
    * Uppercase
    * Lowercase
    * Mixed
    * Frequency""",
"""  - Template: 
    * Example
    * Multiple-choice
    * Special template""",
"""  - Punctuation: 
    * Without
    * Frequency
    * Start with
    * End with""",
"""  - Numeric format: 
    * Integer
    * Float
    * Scientific notation
    * Ordinal number""",
    
"""  - Keyword: 
    * Include
    * Exclude
    * Frequency""",
"""  - Symbol: 
    * Title mark
    * Emoji
    * Placeholder
    * Custom symbol""",
"""  - Sentence: 
    * Start with
    * End with
    * Include
    * Syntax""",
"""  - Genre: 
    * Poetry
    * Novel
    * Script
    * Letter
    * Speech
    * Diary
    * Tweet""",

"""  - Language: 
    * English
    * Chinese
    * Thai
    * German
    * Marathi
    * Spanish""",
"""  - Situation: 
    * Role-play
    * Reasoning
    * Topic""",
"""  - Language style: 
    * Formality
    * Writing style
    * Literary style
    * Humor
    * Era
    * Job""",
"""  - Sentiment: 
    * Positive
    * Negative
    * Hopeful
    * Fascinating"""
    ]

    for i in d[:]:
        if i in evaluated:
            continue
        main_cos = random.choice(cons)
        messages_list.append({'message': [
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Follow the user\'s instructions carefully to provide accurate and helpful content."},
                {"role": "user", "content": """In this task, you need to refine the prompt to make it more specific and complex. Transfer the prompt to an instruction-following task.


To enhance specificity, refer to constraints from the following taxonomy:

1. Format
  - Length: 
    * Number of characters
    * Words
    * Sentences
    * Paragraphs
    * Sections
  - Text format: 
    * JSON
    * Markdown
    * List
    * Table
    * Bullets
    * Postscript
  - Character format: 
    * Uppercase
    * Lowercase
    * Mixed
    * Frequency
  - Template: 
    * Example
    * Multiple-choice
    * Special template
  - Punctuation: 
    * Without
    * Frequency
    * Start with
    * End with
  - Numeric format: 
    * Integer
    * Float
    * Scientific notation
    * Ordinal number

2. Content
  - Keyword: 
    * Include
    * Exclude
    * Frequency
  - Symbol: 
    * Title mark
    * Emoji
    * Placeholder
    * Custom symbol
  - Sentence: 
    * Start with
    * End with
    * Include
    * Syntax
  - Genre: 
    * Poetry
    * Novel
    * Script
    * Letter
    * Speech
    * Diary
    * Tweet

3. General
  - Language: 
    * English
    * Chinese
    * Thai
    * German
    * Marathi
    * Spanish
  - Situation: 
    * Role-play
    * Reasoning
    * Topic
  - Language style: 
    * Formality
    * Writing style
    * Literary style
    * Humor
    * Era
    * Job
  - Sentiment: 
    * Positive
    * Negative
    * Hopeful
    * Fascinating


prompt: [[start]]{}[[end]]

Main constraint:
{}


Note:
1. You must include the main constraint (unless the main constraint contradicts the original prompt), and need to add 1~3 other constraints.
2. You need to ensure that these constraints are reasonable and do not conflict with each other. 
3. The added constraints need to make sense with the original prompt and not conflict with it. 
4. Please ensure the constraints as much diverse as possible, you can add new types not mentioned in the taxonomy above.
5. The priority is given to constraint types other than length constraints.
6. Do not list the added constraints in points.
7. Don't give the response to your refined prompt.
8. If the Prompt is a mathematic or coding problem, just output "None" as the refined prompt.
9. Never involve visual elements.

output in the following format:
""".format(i['prompt'], main_cos) + "[[start]]{your refined prompt}[[end]]"}

            ],
                              'origin': i,
                              'main_constraint': main_cos
                              })
        # from IPython import embed
        # embed()
        # exit()
    return messages_list



if __name__ == '__main__':

    input_file = 'your_input_file_path.json' # a list of prompts 
    output_file = 'your_output_file_path.jsonl'

    if not os.path.exists(output_file):
        x = open(output_file, 'w')
        x.close()
    messages_list = get_messages_list()
    print("total num: ", len(messages_list))
    s_time = time.time()
    responses = multi_process_chat_gpt(messages_list, num_processes=20)