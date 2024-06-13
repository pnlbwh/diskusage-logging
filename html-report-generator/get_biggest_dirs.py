import pandas as pd
import matplotlib.pyplot as plt
from get_closest_log import get_closest_log
import base64
from io import BytesIO


# Returns a sorted size-sorted DataFrame of all the subdirectories based on the most recent log
def get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, is_ascending):
    df = pd.read_csv(logfile_directory + get_closest_log(logfile_directory, logfile_prefix))

    # Filter to get rows matching the subdirectory, also remove subdirectories inside of it
    filtered_df = df[
        df[' Directory'].apply(
            lambda x: x.startswith(directory_prefix) and x.count('/') <= directory_prefix.count('/')
        )].copy()

    # Sort by size
    filtered_df.sort_values(by=' SizeG', ascending=is_ascending, inplace=True)
    return filtered_df


# Return a DataFrame the n largest directories
def get_top_table(logfile_directory, logfile_prefix, directory_prefix, n):
    filtered_df = get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, False)

    columns = [' Directory', ' SizeG', ' Last Modified']
    filtered_df = filtered_df[columns]

    # Convert to a date object to remove HH:mm, also add 2 decimal points
    filtered_df[' Last Modified'] = pd.to_datetime(filtered_df[' Last Modified']).dt.date
    filtered_df[' SizeG'] = filtered_df[' SizeG'].apply(lambda x: f"{x:.2f}")

    return filtered_df.head(n)


# Return base64 image of pie chart corresponding to directory size
def get_top_chart(logfile_directory, logfile_prefix, directory_prefix, pie_label_threshold):
    filtered_df = get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, True)

    total = filtered_df[' SizeG'].sum()

    # Calculate the percentage for each directory and adjust labels based on the threshold
    filtered_df.loc[:, ' Directory'] = filtered_df[' Directory'].str.replace(
        directory_prefix, '/', regex=False)

    filtered_df['Label'] = [
        row[' Directory'] if (row[' SizeG'] / total * 100) > pie_label_threshold else ''
        for _, row in filtered_df.iterrows()
    ]
    filtered_df['Label'] = filtered_df['Label'].str.lstrip('/')

    # Labels each slice of pie chart with rounded % if the slice is larger than the threshold
    def autopct_format(values):
        def my_format(pct):
            return str(round(pct)) + '%' if (pct > pie_label_threshold) else ''

        return my_format

    plt.figure(figsize=(5, 3), dpi=150, )
    plt.pie(
        filtered_df[' SizeG'],
        labels=filtered_df['Label'],
        startangle=90,
        pctdistance=0.80,
        textprops={'fontsize': 8},
        autopct=autopct_format(filtered_df[' SizeG'])
    )
    plt.axis('equal')

    # Save the file as a PNG in memory and export the data string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64
