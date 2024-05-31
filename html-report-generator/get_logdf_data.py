import pandas as pd
import os


"""
Returns a DataFrame representing all data collected from the daily logs in /logdf
"""
def get_usage_data(logdf_path, defualt_lookback_window):
    
    #print(defualt_lookback_window)

    all_dataframes = []

    # Iterate through all files in the directory
    for filename in os.listdir(logdf_path):
        file_path = os.path.join(logdf_path, filename)

        df = pd.read_csv(file_path)

        # Pivot each logdf csv into a single-rowed csv
        pivoted_df = df.pivot(index='Datetime', columns='Filesystem', values=['Usage', 'UsageT'])

        # Joins the names together as such: Usage/data/pnl/, UsageT/rfanfs/pnl-zorro/, etc.
        pivoted_df.columns = [''.join(col) for col in pivoted_df.columns.values]
        pivoted_df.reset_index(inplace=True)

        # Convert string to pd Datetime
        pivoted_df['Datetime'] = pd.to_datetime(pivoted_df['Datetime'])

        # Add data frame to list
        all_dataframes.append(pivoted_df)

    # Combine all data frames and sort by increasing date
    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df = final_df.sort_values('Datetime')

    # Filter everything after the default lookback window
    # Cuttoff has an extra day added to it to ensure that the first month remains visible
    cutoff = pd.to_datetime("today") - pd.DateOffset(months=defualt_lookback_window) - pd.DateOffset(days=1)
    final_df = final_df[final_df['Datetime'] >= cutoff]

    return final_df
