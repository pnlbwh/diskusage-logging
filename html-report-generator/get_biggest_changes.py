import pandas as pd
from get_closest_log import get_week_interval, extract_date


# Returns sorted dataframe by size
def get_sorted_df(directory_prefix, logfile_prefix, num_weeks, change_threshold):
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
    merged_df = merged_df[(merged_df['Size Change (GB)'] >= change_threshold)
                          | (merged_df['Size Change (GB)'] <= -1 * change_threshold)]

    # Filter to only look 5 directories in
    merged_df = merged_df[
        merged_df[' Directory'].apply(
            lambda dirname: dirname.count('/') == 5)
    ]

    # Sorting by 'size_increase' in descending order
    merged_df.sort_values('Size Change (GB)', ascending=False, inplace=True)

    return merged_df, extract_date(week1_file), extract_date(week2_file)


# Function returns top 5 largest movers, omitting rows with 0 size change and formatting
def get_top_bottom_changes(sorted_df, change_threshold, is_increases=True):
    if is_increases:
        output_df = sorted_df.head(5)[sorted_df.head(5)['Size Change (GB)'] > change_threshold]
    else:
        # Reverse bottom entries to preserve magnitude
        output_df = sorted_df.tail(5).iloc[::-1][sorted_df.tail(5).iloc[::-1]['Size Change (GB)'] < change_threshold]

    # Format output_df
    output_df['Size Change (GB)'] = output_df['Size Change (GB)'].apply(lambda x: f"{x:.2f}")
    output_df[' SizeG_new'] = output_df[' SizeG_new'].apply(lambda x: f"{x:.2f}")

    return output_df


# Returns 5 largest increases and decreases, the two dates for which they were measured,
# the directory name, and the number of weeks it was able to query
def get_biggest_changes(directory_prefix, logfile_prefix, num_weeks, change_threshold):
    sorted_df, week1, week2 = get_sorted_df(directory_prefix, logfile_prefix, num_weeks, change_threshold)

    dir_name = '/'.join(sorted_df.iloc[0][' Directory'].split('/')[:3]) + '/'

    return (get_top_bottom_changes(sorted_df, change_threshold, True),
            get_top_bottom_changes(sorted_df, change_threshold, False),
            week1.strftime("%m-%d"), week2.strftime("%m-%d"), dir_name, num_weeks)
