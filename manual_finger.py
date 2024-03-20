#!/usr/bin/env python

# finger command is hard to work with via subprocess
# so we generate the list of users as:
# ./manual_finger.sh

import pandas as pd

df= pd.DataFrame(columns=['user','fname','uid'])

with open('people.txt') as f:
    lines= f.read().strip().split('\n')

for i,line in enumerate(lines):
    parts= line.split(":")
    df.loc[i]= [parts[0],parts[4].split(',')[0],parts[2]]

df.sort_values(by='user', inplace=True)    
df.drop_duplicates(subset='user', inplace=True)

df.to_csv('user_name.csv', index=False)

