from datetime import datetime
import pandas as pd
import os
from get_closest_log import get_week_interval, extract_date


"""
Returns DataFrame with directories ranked by decreasing size gain and the two dates corresponding to when
the logs were created, where num_weeks is the week interval to look over 
"""
def get_sorted_df(directory_prefix, logfile_prefix, num_weeks):

    # Load two reports with the closest date to today and the week before, respectively
    week1_file, week2_file = get_week_interval(directory_prefix, logfile_prefix, num_weeks)

    df1 = pd.read_csv(directory_prefix + week1_file)
    df2 = pd.read_csv(directory_prefix + week2_file)

    # Merge the two data frames with respect to Directory
    merged_df = pd.merge(df2, df1, on=' Directory', suffixes=('_old', '_new'), how='outer')

    # Filling NaN values with 0 for calculations
    merged_df.fillna(0, inplace=True)

    # Calculating the size difference
    merged_df['Size Change (GB)'] = (merged_df[' SizeG_new'] - merged_df[' SizeG_old'])

    # Filtered out 
    merged_df = merged_df[(merged_df['Size Change (GB)'] >= 0.01) | (merged_df['Size Change (GB)'] <= -0.01)]

    # def get_percentage_change(new_size, old_size):
    #     if new_size == old_size:
    #         return 0
    #     if new_size == 0:
    #         return -100
    #     if old_size == 0:
    #         return None;
    #     return ((new_size-old_size)/old_size)*100

    # merged_df['Size Change (%)'] = merged_df.apply(
    #     lambda row: get_percentage_change(row[' SizeG_new'], row[' SizeG_old']), axis=1
    # )

    # Filter to only look 5 directories in
    merged_df = merged_df[
        merged_df[' Directory'].apply(
            lambda dirname: dirname.count('/') == 5
        )
    ]

    # Sorting by 'size_increase' in descending order
    merged_df.sort_values('Size Change (GB)', ascending=False, inplace=True)

    # Rename the columns to make export prettier
    result_df = merged_df[[' Directory', 'Size Change (GB)', ' SizeG_new', ]].copy().rename(
        columns={' Directory': 'Directory', 
                 ' SizeG_new': 'New Size (GB)'
                 })
    
    # Function returns number rounded to two decimal places
    def round_two_decimals(value):
        return float(format(value, '.2f'))

    result_df['New Size (GB)'] = result_df['New Size (GB)'].apply(round_two_decimals)
    result_df['Size Change (GB)'] = result_df['Size Change (GB)'].apply(round_two_decimals)
    #result_df['Size Change (%)'] = result_df['Size Change (%)'].apply(round_two_decimals)

    return result_df, extract_date(week1_file), extract_date(week2_file)

# Function returns top 5 largest movers, omitting rows with 0 size change
def get_top_bottom_changes(sorted_df, is_increases=True):
    if is_increases:
        top_entries = sorted_df.head(5)
        if (top_entries['Size Change (GB)'] > 0).all():
            return top_entries
        else:
            return top_entries[top_entries['Size Change (GB)'] > 0]
    else:
        # Reverse bottom entries to preserve magnitude
        bottom_entries = sorted_df.tail(5).iloc[::-1]
        if (bottom_entries['Size Change (GB)'] < 0).all():
            return bottom_entries
        else:
            return bottom_entries[bottom_entries['Size Change (GB)'] < 0]
        


"""
Returns HTML of the largest increases and decreases
"""
def get_biggest_change_HTML(directory_prefix, logfile_prefix, num_weeks):

    sorted_df, week1, week2 = get_sorted_df(directory_prefix, logfile_prefix,num_weeks)

    # Gets the directory name from the top of the file
    dir_name = '/'.join(sorted_df.iloc[0]['Directory'].split('/')[:3]) + '/'

    return f"""<h2>{num_weeks} Week Changes for {dir_name} ({
            week2.strftime("%m-%d")} to {week1.strftime("%m-%d")}):</h2>
        <h3> biggest increases</h3>
        {get_top_bottom_changes(sorted_df,True).to_html(classes='tablestyle', index=False)}
        <h3> biggest decreases</h3>
        {get_top_bottom_changes(sorted_df,False).to_html(classes='tablestyle', index=False)}
        """
