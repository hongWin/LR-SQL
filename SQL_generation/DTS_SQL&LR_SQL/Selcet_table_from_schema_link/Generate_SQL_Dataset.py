import copy
import json
import pandas as pd
import tqdm

#  train
# df = pd.read_csv("./spider_ori_dataset/full_finetuning_dataset.csv")
# df = pd.read_csv("./generated_schemaLink/full_finetuning_dataset.csv",encoding="GBK")
df = pd.read_csv("./mydataset2_SQL/full_finetuning_dataset.csv",encoding="utf-8")

#  val
# df = pd.read_csv("./spider_ori_dataset/validation_dataset_formatted.csv")
# df = pd.read_csv("./generated_schemaLink/validation_dataset_formatted.csv")
results = []




#  sql
max_length = 0
messages = []
for i in range(len(df['db_id'])):
    question = df['question'][i]
    query = df['query'][i]
    database_schema = df['database_schema'][i]
    db_id = df['db_id'][i]
    message = {
        "instruction": f" I want you to act as a SQL terminal in front of an example database, you need only to return the sql command to me.Below is an instruction that describes a task, Write a response that appropriately completes the request. \n##instruction:{database_schema}",
        "input": f"{question}",
        "output": f"```gerenated SQL\n-- SQL: {query};\n```",
    }
    messages.append(message)



with open("./mydataset2_SQL/T2Q_GLM4_SFT_train_sql.jsonl", "w", encoding="utf-8") as file:
    for message in messages:
        file.write(json.dumps(message, ensure_ascii=False) + "\n")



