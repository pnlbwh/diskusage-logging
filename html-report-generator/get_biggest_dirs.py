import pandas as pd
import matplotlib.pyplot as plt
from get_closest_log import get_closest_log
import base64
from io import BytesIO
from os.path import join as pjoin


"""
Returns a sorted size-sorted DataFrame of all of the subdirectories based on the most recent log.

logfile_directory is the path to the /logdirsizes directory, logfile_prefix is the specific prefix 
the logfiles should have, directory_prefix corresponds to the directory to query 
"""
def get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, isAscending):

    df = pd.read_csv(logfile_directory + get_closest_log(logfile_directory, logfile_prefix))

    # Filter to get rows matching the subdirectory, also remove subdirectories inside of it
    filtered_df = df[
        df[' Directory'].apply(
            lambda x: x.startswith(directory_prefix) and 
                    x.count('/') <= directory_prefix.count('/')
        )
    ].copy()

    # Sort by size
    filtered_df.sort_values(by=' SizeG', ascending=isAscending, inplace=True)
    filtered_df[' SizeG'] = filtered_df[' SizeG'].apply(lambda x: float(format(x, '.2f')))
    
    return filtered_df

"""
Return a DataFrame the n largest directories
"""
def get_top_table(logfile_directory, logfile_prefix, directory_prefix, n):

    filtered_df = get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, False)

    columns = [' Directory', ' SizeG', ' Last Modified']
    filtered_df = filtered_df[columns]

    # Convert to a date object to remove HH:mm
    filtered_df[' Last Modified'] = pd.to_datetime(filtered_df[' Last Modified']).dt.date

    return filtered_df.head(n)


"""
Return base64 image of pie chart corresponding to directory size
"""
def get_top_chart(logfile_directory, logfile_prefix, directory_prefix):

    filtered_df = get_sorted_df(logfile_directory, logfile_prefix, directory_prefix, True)

    # The cutoff percents for when to add labels to pie charts
    percent_threshold = 10
    label_threshold = percent_threshold

    total = filtered_df[' SizeG'].sum()

    # Calculate the percentage for each directory and adjust labels based on the threshold

    filtered_df.loc[:, ' Directory'] = filtered_df[' Directory'].str.replace(
    directory_prefix, '/', regex=False)

    filtered_df['Label'] = [
        row[' Directory'] if (row[' SizeG'] / total * 100) > label_threshold else ''
        for _, row in filtered_df.iterrows()
    ]
    filtered_df['Label'] = filtered_df['Label'].str.lstrip('/')

    # Labels each slice of pie chart with rounded % if the slice is larger than the threshold
    def autopct_format(values):
        def my_format(pct):
            return str(round(pct)) + '%' if (pct > percent_threshold) else ''
        return my_format

    plt.figure(figsize=(5,3),dpi=150,)
    plt.pie(
        filtered_df[' SizeG'], 
        labels=filtered_df['Label'], 
        startangle=90,
        pctdistance=0.80,
        textprops={'fontsize': 8},
        autopct=autopct_format(filtered_df[' SizeG'])
    )
    #plt.title("Top " + prefix + " Directories")
    plt.axis('equal')

    # Save the file as a PNG in memory and export the data string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64




"""
Return HTML for the table/pie chart row
"""
def get_table_and_chart_HTML(logfile_directory, logfile_prefix, directory_prefix):

    # Turn the subdir into an html-compatible id
    safe_subdir = directory_prefix.replace('/', '_').replace('\\', '_').replace(' ', '_').replace(':', '_')

    # List paths to the 5 largest subdirectories inside the directory corresponding to directory_prefix
    top_table = get_top_table(logfile_directory, logfile_prefix, directory_prefix, 5)
    dir_list = top_table[' Directory'].tolist()
    dir_path_list = [pjoin(directory_prefix, dir_name) + '/' for dir_name in dir_list]

    # Generate html for all 5 subtables
    sub_tables_html = []
    for i, subdir_path in enumerate(dir_path_list):
        # Get 10 subdirectories, convert to html table
        subdir_size_list = (get_top_table(logfile_directory, logfile_prefix, subdir_path, 10))
        sub_table_html = subdir_size_list.to_html(index=False)
        # Aadd a directory-specific id and make it hidden
        sub_tables_html.append(f'<div id="subtable{safe_subdir}_{i}" style="display:none; height: 400px;">{sub_table_html}</div>')

    # Add 'clickable' property to make hyperlinks, then convert table to html
    top_table[' Directory'] = top_table[' Directory'].apply(lambda x: f'<span class="clickable">{x}</span>')
    top_table_html = top_table.to_html(classes='tablestyle', index=False, escape=False)

    # Add click functionality with javascript function, specifying correct id
    top_table_html = top_table_html.replace('<tr>', f'<tr onclick="toggleSubTable(event, \'{safe_subdir}\')">')

    script = """
    <script>
        // only react to clickable links
        function toggleSubTable(event, subdirPrefix) {
            var target = event.target;
            if (!target.classList.contains('clickable')) {
                return;
            }

            // if make sure tables are hidden in between clicks
            var allSubtables = document.querySelectorAll('div[id^="subtable' + subdirPrefix + '_"]');
            allSubtables.forEach(div => { div.style.display = 'none'; });

            var row = target.closest('tr');
            var rowIndex = Array.from(row.parentNode.children).indexOf(row);

            // get the specific table by id
            var subtable = document.getElementById('subtable' + subdirPrefix + '_' + rowIndex);
            if (subtable) {
                subtable.style.display = 'block';
                
                // get the heading above the table, and move it to the top of the page (revealing table) when link clicked
                var heading = document.getElementById('heading' + subdirPrefix);
                if (heading) {
                    heading.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            }
        }
    </script>
    """

    return f"""
        <h2 id="heading{safe_subdir}" style="margin-top: 60px; padding-top: 40px;">{directory_prefix} Largest Directories</h2>
        <div style="display: flex; align-items: center; width: 90%;">
            <div style="flex: 3; min-width: 0;">
                {top_table_html}
            </div>
            <div style="flex: 2; min-width: 0;">
                <img src="data:image/png;base64,{
                    get_top_chart(logfile_directory, logfile_prefix, directory_prefix)
                    }" style="max-width: 100%; height: auto;">
            </div>
        </div>
        {''.join(sub_tables_html)}
        <br>
        <br>
        {script}
        """