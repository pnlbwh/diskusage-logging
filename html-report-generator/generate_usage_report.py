#!/usr/bin/env python

import datetime
import itertools
from os.path import dirname, abspath, basename, join as pjoin

# Use Agg non-interactive backend to prevent X forwarding error
import matplotlib
matplotlib.use('Agg')

from plot_usage_image import get_usage_chart
from get_biggest_changes import get_biggest_change_HTML
from get_biggest_dirs import get_table_and_chart_HTML


def usage():
    print ('''Create an HTML diskusage report for directories listed in _config/dirs.txt''')

def main():
    current_date = datetime.datetime.now()

    # Defaults: working dir is 1 directory above where this file is located
    working_dir = abspath(pjoin(dirname(__file__),'..'))

    # Default relative paths for input data and output location
    data_path = pjoin(working_dir, '_data/')
    
    logdf_path = data_path + 'logdf/'
    logdirsizes_path = data_path + 'logdirsizes/'

    # Get directories to query from _config/dirs.txt
    config_file_path = pjoin(working_dir, '_config/') + 'dirs.txt'
    with open(config_file_path, 'r') as file:
	# only add lines to dir_list that are non-empty
        dir_list = file.read().strip().split('\n')

    # Get the name of the filesystem from config.txt
    filesystem_name = dir_list[0].split('/')[1]

    # Title report file as report-data-{datestamp}.html or report-rfanfs-{datestamp}.html
    file_path = f"{pjoin(working_dir, '_data/', 'htmlreport/')}report-{filesystem_name}-{current_date:%Y%m%d}.html"    

    # ------------------------------------
    # Configure Usage v. Time Step Chart:
    # ------------------------------------
    # Make colors correspond with filesystems listed in dirs.txt
    colors = itertools.cycle(['red', 'blue', 'green', 'yellow', 'violet'])
    filesystems_to_monitor = [ (directory_prefix, next(colors)) for directory_prefix in dir_list]

    # number of months to look back on step chart
    defualt_lookback_window = 12

    # ------------------------------------
    # Configure Increase/Decrease Tables:
    # ------------------------------------
    # Converts a directory name to a logfile prefix, as used in /logdirsizes
    def directory_to_logfile_prefix(directory_prefix):
        return directory_prefix.strip('/').replace('/', '_') + '-dirsizes-'

    # Look at the biggest increase/decreases over 1 and 4 week periods
    logfiles_to_monitor_change = []
    for directory_prefix in dir_list:
        logfiles_to_monitor_change.append( (directory_to_logfile_prefix(directory_prefix), 1) )
        logfiles_to_monitor_change.append( (directory_to_logfile_prefix(directory_prefix), 4) )

    # ------------------------------------
    # Configure Biggest Directory Tables:
    # ------------------------------------
    # Tuple has the logfile prefix and the directory 
    directories_to_query = [ (directory_to_logfile_prefix(directory_prefix), directory_prefix) for directory_prefix in dir_list]

    """
    Returns all of the HTML for the increase/decrease tables
    """
    def get_all_changes_tables_html():
        output = ""
        for logfile in logfiles_to_monitor_change: 
            output += get_biggest_change_HTML(logdirsizes_path, logfile[0], logfile[1]) 
        return output


    """
    Generates all the HTML for the largest directory tables/pie charts
    """
    def get_all_chart_html():
        output_html = ""
        for query_tuple in directories_to_query:
            output_html += get_table_and_chart_HTML(logdirsizes_path, query_tuple[0], query_tuple[1])
        return output_html


    # Define the HTML for the report
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Disk Usage Report</title>
        <style>
            body {{
                padding-bottom: 50px;
                font-family: sans-serif;
                display: flex;
                align-items: center;
                min-height: 100vh;
                flex-direction: column;
            }}
            h1{{
                margin-top: 90px;
            }}
            h2{{   
                margin-top: 50px;
                margin-bottom: 5px;
            }}
        .tablestyle {{
            border: none;
            width: 60%;
            margin-left: auto;
            margin-right: auto;
            border-collapse: collapse;
            margin-bottom: 25px;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border: none;
        }}
        .col-1, .col-2 {{
            width: 150px; /* Adjust the width as needed */
        }}
        
        .clickable{{
            cursor: pointer;
            color: blue;
            text-decoration: underline;
        }}
            
        </style>
    </head>
    <body>

        <h1>Disk Usage Report for {current_date.strftime("%Y-%m-%d %H:%M")}</h1>
        <img src="data:image/png;base64,{get_usage_chart(logdf_path, filesystems_to_monitor, defualt_lookback_window)}" style="max-width: 75%; height: auto;">
        {get_all_changes_tables_html()}
        {get_all_chart_html()}
    </body>
    </html>
    """

    # Write the HTML content to the file
    with open(file_path, 'w') as file:
        file.write(html_content)

if __name__ == '__main__':
    main()
