from datetime import datetime
import os

date = datetime.now()


"""
Returns a datetime object from a file name
"""
def extract_date(filename):
    return datetime.strptime(filename.split("-")[-1].split(".")[0], "%Y%m%d")


"""
Returns list of file names that begin with the prefix, sorted by closest date first
"""
def get_sorted_files(directory, logfile_prefix):

    # Filter CSV files to ones that start with prefix
    filenames = [file for file in os.listdir(directory) if file.startswith(logfile_prefix)]

    # Extract the dates from the files
    file_dates = {filename: extract_date(filename) for filename in filenames}

    # Filter to only have files that are on or before specified date
    before_dates = {filename: file_date for filename, file_date in file_dates.items() if file_date <= date}

    # Sort the filenames based on the date, closest first
    sorted_before_filenames = sorted(before_dates.keys(), key=lambda x: abs(before_dates[x] - date))

    return sorted_before_filenames


"""
Returns the filename with the closest date to today
"""
def get_closest_log(directory, logfile_prefix):
    return get_sorted_files(directory, logfile_prefix)[0]


"""
Returns two filenames with the closest week interval to today
"""
def get_week_interval(directory, logfile_prefix, num_weeks):
    sorted_files = get_sorted_files(directory, logfile_prefix)
    return sorted_files[0], sorted_files[num_weeks]
