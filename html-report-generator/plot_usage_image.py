import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
import pandas as pd
from io import BytesIO

from get_logdf_data import get_usage_data


"""
Returns a base64 data for image of usage data step graph as defined in /logdf
"""
def get_usage_chart(logdf_path, filesystems_to_monitor, defualt_lookback_window):

    # Adds an annotation to the end of line corresponding to data_column
    def addAnnotations(subplot_line, data_column, units):

        # Reverse the series to find index of last data point for a given line
        reverse_series = usage_df[data_column][::-1].notna()
        last_valid_index_from_end = reverse_series.idxmax()

        # Get the date and value associated with the last data point
        last_date = usage_df.loc[last_valid_index_from_end, 'Datetime']
        last_value = usage_df[data_column].loc[last_valid_index_from_end]

        # Add the annotation to the plot, where the position is x=last_date, y=last_value
        subplot_line.annotate(
            f"{last_value}" + units,
            (last_date, last_value),
            textcoords="offset points", xytext=(45,0),
            fontsize=15, fontweight='bold', 
            ha='center', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='black'))


    # Load usage data
    usage_df = get_usage_data(logdf_path, defualt_lookback_window)

    # Create subplots with grids
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(14, 10))

    ax1.grid(True)
    ax2.grid(True)
    
    # Draw both graphs, add annotations
    for filesystem in filesystems_to_monitor:
        ax1.step(usage_df['Datetime'], usage_df['UsageT'+filesystem[0]], color=filesystem[1], label=filesystem[0], linewidth=2.5)
        ax2.step(usage_df['Datetime'], usage_df['Usage'+filesystem[0]], color=filesystem[1], label=filesystem[0], linewidth=2.5)
        addAnnotations(ax1, 'UsageT'+filesystem[0], 'TB')
        addAnnotations(ax2, 'Usage'+filesystem[0], '%')

    ax1.set_ylabel('Terabytes', rotation=90, fontweight='bold', fontsize=15, labelpad=20)
    ax2.set_ylabel('% Usage', rotation=90, fontweight='bold', fontsize=15, labelpad=20)

    # On the bottom graph, make sure 100% and 0% lines are visible
    ax2.set_ylim(top=100)
    ax2.set_ylim(bottom=0)

    # bound the x-axis on the left by the earliest date
    x_left_edge = usage_df['Datetime'].iloc[0]
    
    # bound x on the right by the latest date plus and offset to accomodate labels
    x_right_edge = usage_df['Datetime'].iloc[-1] + pd.DateOffset(months=2)

    ax1.set_xlim(x_left_edge, x_right_edge)
    ax2.set_xlim(x_left_edge, x_right_edge)


    # Add legends
    legend1 = ax1.legend(loc='center left',bbox_to_anchor=(1.02, 0.5), 
                         borderpad=1, handlelength=2, handletextpad=1, labelspacing=1.2)
    legend1.set_title('Filesystem', prop={'size': 10})

    legend2 = ax2.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), 
                         borderpad=1, handlelength=2, handletextpad=1, labelspacing=1.2)
    legend2.set_title('Filesystem', prop={'size': 10})

    # Set major major locator and formatter
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    ax1.set_facecolor('#EBEBEB')
    ax2.set_facecolor('#EBEBEB')

    # Angle the x axis labels
    plt.setp(ax2.get_xticklabels(), rotation=45)

    # Adjust the margins, tighten layout
    plt.subplots_adjust(top=0.92, bottom=0.15, hspace=0.1)
    plt.tight_layout(pad=2.0)

    # Add bottom label
    fig.text(0.5, 0.05, 'Date', ha='center', va='center', fontweight='bold', fontsize=20)
    plt.subplots_adjust(top=0.92, bottom=0.14, hspace=0.1)

    # Save the file as a PNG in memory and export the data string
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64
