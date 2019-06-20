#!/usr/bin/env python

import pandas as pd
import sys
from os.path import isdir

def usage():
    print('Usage: ./dir_sort.py infoFile.csv outSummary.csv /abs/path/of/parent/dir/*')
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
        print('provide a list of directories, not the parent directory only, may be you forgot an * at the end?')
        usage()

    dirs= [dir for dir in dirs if isdir(dir)]
    df= pd.read_csv(infoFile)

    df_parent= pd.DataFrame(columns= ['Directory', 'SizeG'])
    for j,dir in enumerate(dirs):
        space= 0.
        for i,name in enumerate(df.values[:,3]):
            if dir in name:
                space+=df.values[:,2][i]

        df_parent.loc[j]= [dir,space/2.]

    df_parent.sort_values(by=['SizeG'], ascending=False, inplace= True)
    df_parent.set_index('Directory', inplace=True)
    df_parent.to_csv(outSummary)
    print(df_parent)

if __name__=='__main__':
    main()

'''
./dir_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv Collaborators.csv `ls -d /rfanfs/pnl-zorro/Collaborators/*`
./dir_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv projects.csv `ls -d /rfanfs/pnl-zorro/projects/*`
./dir_sort.py _data/logdirsizes/rfanfs_pnl-zorro-dirsizes-3-20190506.csv home.csv `ls -d /rfanfs/pnl-zorro/home/*`
'''