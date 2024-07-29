#!/usr/bin/env python

from jinja2 import Environment, FileSystemLoader
import datetime
import os
from os.path import dirname, abspath, join as pjoin
from plot_usage_image import get_usage_chart
from get_biggest_changes import get_biggest_changes
from get_biggest_dirs import get_top_chart, get_top_table
import sys

# Use Agg non-interactive backend to prevent X forwarding error
import matplotlib
matplotlib.use('Agg')

os.environ["OMP_NUM_THREADS"] = "1"


if len(sys.argv) > 1:
    print(f'''Usage:
{__file__}

Simply execute this script after modifying _config/dirs.txt''')
    exit()


# -------------------------- SETUP --------------------------
# Step chart setup -- line colors and number of months to look back
line_colors = ['red', 'blue', 'green', 'yellow', 'violet']
default_lookback_window = 12

# Largest changes setup -- Look at 1 week and 4 week changes, only display > 10 GB
week_intervals = [1, 4]
change_threshold_gb = 10

# Largest directory setup -- minimum percent to label a slice
pie_label_threshold = 10
# -----------------------------------------------------------


# Returns the prefix of the logfile for a corresponding directory
def directory_to_logfile_prefix(prefix):
    return prefix.strip('/').replace('/', '_') + '-dirsizes-'


current_date = datetime.datetime.now()

# Defaults: working dir is 1 directory above where this file is located
working_dir = abspath(pjoin(dirname(__file__), '..'))

# Default relative paths for input data and output location
data_path = pjoin(working_dir, '_data')
logdf_path = pjoin(data_path, 'logdf')
logdirsizes_path = pjoin(data_path, 'logdirsizes/')
template_path = pjoin(working_dir, 'html-report-generator', 'templates')
config_file_path = pjoin(working_dir, '_config', 'dirs.txt')

# Read _config/dirs.txt, omitting blanks
with open(config_file_path, 'r') as file:
    dir_list = file.read().strip().split('\n')

# Get the name of the filesystem from config.txt
filesystem_name = dir_list[0].split('/')[1]

# Title report file as report-data-{datestamp}.html or report-rfanfs-{datestamp}.html
file_path = f"{pjoin(working_dir, '_data/', 'htmlreport/')}report-{filesystem_name}-{current_date:%Y%m%d}.html"

# Create an environment and load the template file
env = Environment(loader=FileSystemLoader(template_path))
template = env.get_template('disk_report_template.html')

# Define context variables
context = {
    'report_date': current_date.strftime("%Y-%m-%d"),
    'step_img': get_usage_chart(logdf_path, dir_list, default_lookback_window, line_colors),
    'biggest_changes': [],
    'biggest_dirs': []
}

# Add the biggest changes section
for dir_name in dir_list:
    for weeks in week_intervals:
        increases, decreases, week1, week2, dirname, weeks \
            = get_biggest_changes(logdirsizes_path, directory_to_logfile_prefix(dir_name), weeks, change_threshold_gb)

        increases_list = increases.to_dict(orient='records')
        decreases_list = decreases.to_dict(orient='records')

        new_card = {
            'num_weeks': weeks,
            'dirname': dirname,
            'week1': week1,
            'week2': week2,
            'increases': increases_list,
            'decreases': decreases_list
        }
        context['biggest_changes'].append(new_card)


# Add the biggest dirs section
for top_dir in dir_list:

    logfile_prefix = directory_to_logfile_prefix(top_dir)

    pie_chart = get_top_chart(logdirsizes_path, logfile_prefix, top_dir, pie_label_threshold)
    top_table = get_top_table(logdirsizes_path, logfile_prefix, top_dir, 5)

    sub_dirs = []
    for _, row in top_table.iterrows():
        hidden_dirs = get_top_table(
            logdirsizes_path, logfile_prefix, row[' Directory']+'/', 10).to_dict(orient='records')
        subdir = row.to_dict()
        subdir['hidden_dirs'] = hidden_dirs
        sub_dirs.append(subdir)

    new_card = {
        'dirname': top_dir,
        'img_data': pie_chart,
        'subdirs': sub_dirs
    }
    context['biggest_dirs'].append(new_card)


# Render the template with the context variables
html_content = template.render(context)

# Save the rendered HTML to a file
with open(file_path, 'w') as f:
    f.write(html_content)

print('Report generated successfully')
