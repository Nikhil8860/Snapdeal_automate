import os
import pandas as pd
import re

base_dir = os.getcwd()

working_directory_input = os.path.join(base_dir, 'Inputs')
working_directory_output = os.path.join(base_dir, 'Outputs')

if not os.path.exists(working_directory_input):
    os.mkdir(working_directory_input)

if not os.path.exists(working_directory_output):
    os.mkdir(working_directory_output)

file_name = [i for i in os.listdir(working_directory_input) if '.xlsx' in i]


def get_size(size):
    return re.findall(r'(\s+\d+)|(\s+\D+)', size)


def get_color(color):
    return re.findall(r':\s+\w+', color)


def apply_filter(data):
    return re.findall(r"[a-z].*", data)


def apply_filter_child(data):
    return re.findall(r"[^a-z].*", data)


for i, v in enumerate(file_name):
    print("Processing file " + str(i))
    file_path = os.path.join(working_directory_input, v)
    df = pd.read_excel(file_path, sheet_name='data')
    df['Content'].ffill(inplace=True)
    df['Product categories'].ffill(inplace=True)
    df['Size'] = df['Excerpt'].str.split(',').str[0].apply(lambda x: get_size(str(x))).str[0]
    df['Color'] = df['Excerpt'].str.split(',').str[1].apply(lambda x: get_color(str(x))).str[0]
    df['Parent Sku'] = df['_sku'].apply(lambda x: apply_filter(x)).str[0].ffill()
    df['Child Sku'] = df['_sku'].apply(lambda x: apply_filter_child(x)).str[0]
    df.to_excel(os.path.join(working_directory_output, 'final_'+str(i)+'.xlsx'), index=False)

print("Done!!!")


