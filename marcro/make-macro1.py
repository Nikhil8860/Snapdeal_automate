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
    df['Description'].ffill(inplace=True)
    df['Categories'].ffill(inplace=True)
    df['Tags'].ffill(inplace=True)
    df.to_excel(os.path.join(working_directory_output, 'final_'+str(i)+'.xlsx'), index=False)

print("Done!!!")
