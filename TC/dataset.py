import os
import pandas as pd
from pathlib import Path

def create_dataset_df(directory, skip_filename="LICENSE.txt"):
    path = Path(directory)
    title_list = []
    data = []
    for subdir in path.glob('*'):
        if subdir.is_dir():
            title_list.append(subdir.name)
            for file in subdir.glob('*.txt'):
                if file.name == skip_filename:
                    continue
                else:
                    with open(file, "r", encoding='utf-8') as f:
                        sentence = f.readlines()[2].strip()
                        data.append((subdir.name, sentence))
    return title_list, data

script_dir = Path(__file__).parent
sub_dir = "text"
title_list, data = create_dataset_df(script_dir/sub_dir)

def list_to_dict(lst):
    return {key: index for index, key in enumerate(lst)}

title_dict = list_to_dict(title_list)

# dataset
df = pd.DataFrame(data, columns=['label', 'sentence'])
df['label'] = df['label'].map(title_dict)

df = df.sample(frac=1)
print(df)
# make dataset
num = len(df)
df[:int(num*0.8)].to_csv('train.csv', sep=',', index=False)
df[int(num*0.8):].to_csv('dev.csv', sep=',', index=False)