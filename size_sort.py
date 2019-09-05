#!/usr/bin/env python

import pandas as pd
import sys
from os.path import isdir

def usage():
    print('''Organize directories according to last access date.
Usage:  
# for all subdirectories in dir
./size_sort.py infoFile.csv outSummary.csv `ls -d /abs/path/of/parent/dir/*/`
# for all files in dir
./size_sort.py infoFile.csv outSummary.csv `ls -d /abs/path/of/parent/dir/*`''')

    exit()

def main():

    if len(sys.argv)==1 or sys.argv[1]=='-h' or sys.argv[1]=='--help':
        usage()

    infoFile= sys.argv[1]
    outSummary = sys.argv[2]
    dirs = sys.argv[3:]

    # sanity check
    if not (infoFile.endswith('.csv') and outSummary.endswith('.csv')):
        print('infoFile and outSummary must be .csv files')
        usage()

    if len(dirs)<2:
        print('provide a list of directories, not the parent directory only, may be you forgot an */ at the end?')
        usage()
    
    # checking for directories will fail for remote servers
    # dirs= [dir for dir in dirs if isdir(dir)]
    df= pd.read_csv(infoFile)

    df_parent= pd.DataFrame(columns= ['Directory', 'SizeG', 'Last Modified'])
    for j,dir in enumerate(dirs):
        for i,name in enumerate(df[' Directory']):
            if dir==name+'/':
                df_parent.loc[j]= [dir,df[' SizeG'][i],df[' Last Modified'][i]]


    df_parent.sort_values(by=['SizeG'], ascending=False, inplace= True)
    df_parent.set_index('Directory', inplace=True)
    df_parent.to_csv(outSummary)
    print(df_parent)

if __name__=='__main__':
    main()

'''
./size_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv Collaborators.csv `ls -d /rfanfs/pnl-zorro/Collaborators/*/`
./size_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv projects.csv `ls -d /rfanfs/pnl-zorro/projects/*/`
./size_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv home.csv `ls -d /rfanfs/pnl-zorro/home/*/`
./size_sort.py _data/logdirsizes/data_pnl-dirsizes-3-20190615.csv data_pnl.csv `ssh eris1n2.research.partners.org "ls -d /data/pnl/*/"`
'''

