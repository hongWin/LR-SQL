import copy
import json
import pandas as pd
import tqdm
import re
from utils.filter_selected_tables import get_filtered_sql_statements




#  train_SET_Pretable
# df = pd.read_csv("./SQL_table/dataset2/pre_table_DTS_SQL.csv",encoding="utf-8")
df = pd.read_csv("./mydataset2_SQL/pre_train.csv",encoding="utf-8")
#  val
# df = pd.read_csv("./spider_ori_dataset/validation_dataset_formatted.csv")
# df = pd.read_csv("./generated_schemaLink/validation_dataset_formatted.csv")
results = []


pre_list = df['predicted_tables'].tolist()
print(pre_list)



#  train
# df = pd.read_csv("./spider_ori_dataset/full_finetuning_dataset.csv")
# df = pd.read_csv("./mydataset_new/full_finetuning_dataset_cropped.csv",encoding="utf-8")
df = pd.read_csv("./mydataset_new/full_finetuning_dataset_cropped.csv",encoding="utf-8")

#  val
# df = pd.read_csv("./spider_ori_dataset/validation_dataset_formatted.csv")
# df = pd.read_csv("./generated_schemaLink/validation_dataset_formatted.csv")
results = []






Database_table_dict = {}
max_length = 0
messages = []
database_schema = ""
if "database_schema" not in df.columns:
    # df2 = pd.read_csv("./mydataset_new/table_schema_Reference_cropped.csv", encoding="utf-8")
    df2 = pd.read_csv("./mydataset_new/table_schema_Reference_cropped.csv", encoding="utf-8")
    for i in range(len(df2['Reference_group'])):
        database_schema += df2['Reference_group'][i]
        database_schema += "\n"

    # df2 = pd.read_csv("./mydataset_new/table_schema_noReference_cropped.csv",encoding="utf-8")
    df2 = pd.read_csv("./mydataset_new/table_schema_noReference_cropped.csv",encoding="utf-8")
    for i in range(len(df2['noReference_group'])):
        database_schema += df2['noReference_group'][i]
        database_schema += "\n"

print(database_schema)



list_check = []
new_df = []
for i in range(len(df['db_id'])):
    question = df['question'][i]
    query = df['query'][i]
    # database_schema = df['database_schema'][i]
    db_id = df['db_id'][i].replace(" ", "")
    correct_tables = df['correct_tables'][i].split(', ')
    if str(pre_list[i]) == "nan":
        predicted_tables = set()
    else:
        predicted_tables = set(pre_list[i].split(', '))
    train_tables = list(set(correct_tables) | predicted_tables)
    filtered_sql_statements = get_filtered_sql_statements(database_schema, train_tables)
    new_df.append([db_id,query,question,filtered_sql_statements])
    # print(filtered_sql_statements)
    if len(filtered_sql_statements) == 0:
        list_check.append(i)
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


# new_df = pd.DataFrame(new_df, columns = ['db_id','query','question','database_schema'])
new_df = pd.DataFrame(new_df, columns = ['db_id','query','question','database_schema'])
new_df.to_csv('./mydataset2_SQL/full_finetuning_dataset.csv',index=False,encoding='utf-8')