import copy
import json
import pandas as pd
import tqdm
import re
from utils.filter_selected_tables import get_filtered_sql_statements
#  train
# df = pd.read_csv("./spider_ori_dataset/full_finetuning_dataset.csv")
import math
import numpy as np


df = pd.read_csv("./mydataset2_SQL/pre_val.csv",encoding="utf-8")
#  val
# df = pd.read_csv("./spider_ori_dataset/validation_dataset_formatted.csv")
# df = pd.read_csv("./generated_schemaLink/validation_dataset_formatted.csv")
results = []


pre_list = df['predicted_tables'].tolist()
print(pre_list)


for item in pre_list:
    item = str(item)
    if item == "nan":
        print(f"Found nan: {item}")
    # else:
    #     print(f"Not nan: {item}")


# selected_tables = ['employee']
# filtered_sql_statements = get_filtered_sql_statements(sql_statements,selected_tables)


# get select_table_info
df = pd.read_csv("./mydataset_new/table_schema_Reference_cropped.csv",encoding="utf-8")
# df = pd.read_csv("./mydataset_shcema/table_schema_Reference.csv",encoding="utf-8")
database_schema = ""
for i in range(len(df['Reference_group'])):
    database_schema += df['Reference_group'][i]
    database_schema += "\n"

df = pd.read_csv("./mydataset_new/table_schema_noReference_cropped.csv",encoding="utf-8")
# df = pd.read_csv("./mydataset_shcema/table_schema_noReference.csv",encoding="utf-8")
for i in range(len(df['noReference_group'])):
    database_schema += df['noReference_group'][i]
    database_schema += "\n"


print(database_schema)


# df = pd.read_csv("./mydataset_test_upper/validation_dataset_formatted_upper.csv",encoding="utf-8")
df = pd.read_csv("./mydataset_new/validation_dataset_formatted_cropped.csv",encoding="utf-8")
Database_table_dict = {}
max_length = 0
messages = []

list_check = []
list_check_table = []
new_df = []
for i in range(len(df['db_id'])):
    question = df['question'][i]
    query = df['query'][i]
    correct_tables = df['correct_tables'][i]
    db_id = df['db_id'][i].replace(" ", "")
    # print(pre_list[i])
    if str(pre_list[i]) == "nan":
        predicted_tables = ["architect"]
    else:
        predicted_tables = pre_list[i].split(', ')
    if "none" in str(pre_list[i]).lower():
        print("++++++++++++++++++++++++++")
        predicted_tables = ["architect"]
    filtered_sql_statements = get_filtered_sql_statements(database_schema, predicted_tables)
    new_df.append([db_id,query,question,filtered_sql_statements])
    # print(filtered_sql_statements)
    if len(filtered_sql_statements) == 0:
        list_check.append(i)
        list_check_table.append(predicted_tables)
    # print(correct_tables)
    #  验证 database 和 table 是否符合标准
    # if db_id not in Database_table_dict:
    #     Database_table_dict[db_id] = database_schema
    # else:
    #     if database_schema != Database_table_dict[db_id]:
    #         print("+++++++++++++++")
    #         print(Database_table_dict[db_id])
    #         print(database_schema)
    #         print("---------------------")
print()
print(list_check)
print(list_check_table)


new_df = pd.DataFrame(new_df, columns = ['db_id','query','question','database_schema'])
new_df.to_csv('./mydataset2_SQL/val_Myidea_tableOnly.csv',index=False,encoding='utf-8')