import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
import seaborn as sns
import pytz
from pytz import timezone
import math
from textwrap import wrap

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.mode.chained_assignment = None # Mitigates SettingWithCopyWarning: 
                                          #A value is trying to be set on a copy of a slice from a DataFrame.
                                          #Try using .loc[row_indexer,col_indexer] = value instead
#print("Cozie Plot Module start")

class CoziePlot:  
  """
  Class to plot Cozie-Apple data
  """

  def __init__(self, df, participant_list=None, ws_questions=None):   
    """
    Constructor initializes class attributes and prints test string
    
    Arguments
    ----------
      - df, Pandas dataframe, Dataframe with Cozie data
      - participant_list, list of str, List with Participant IDs
    
    Returns
    -------
      -
    """
    self.df = df.copy()
    if participant_list == None:
      self.participant_list = df["id_participant"].unique()
      self.participant_list = np.sort(self.participant_list)
    else:
      self.participant_list = participant_list

    self.ws_questions = ws_questions
      
    return
  
  def test(self):  
    """
    Function that plots some string for debugging
    
    Arguments
    ----------
      - 
      
    Returns
    -------
      - 
    """
    print("CoziePlot Test")
    return
  
  def ts_inspection(self, column_name, id_participant):  
    """
    Function to plot time-series data in detail for one participant
    Arguments
    ----------
      - column_name, str, Name of column with time-series data that should be plotted
      - id_participant, str, Participant ID of which the time-series data should be plotted
    Returns
    -------
      - ax, ?, matplotlib axis object
    """

    df_input = self.df[self.df['id_participant']==id_participant]
    YOUR_TIMEZONE = "Asia/Singapore" # XXX remove/fix this before release
    date_start = df_input.index[0]
    date_end = df_input.index[-1]

    if column_name not in df_input.columns:
      print("Column name does not exist in dataframe.")
      return

    # Prep dataframes
    df2 = df_input[df_input[column_name].notna()]
    #df2 = df2.to_frame()
    num_rows = len(df2.index)
    if (num_rows<2):
      print("Dataframe has less than two rows that are not NaN. No plots could be drawn")
      return

    # Compute difference between index timestamps
    df2['dT'] = df2.index.to_series().diff().dt.total_seconds()/60 # Compute time difference between timestamps in minutes
    #df2['dT'] = df2['dT'].div(1000) # Convert dT from miliseconds to seconds
    #df2['dT'] = df2['dT'].div(60) # Convert dT from seconds to minutes

    # Compute difference between timestamps (index-lambda)
    df2['dTL'] = (df2["timestamp_lambda"]-df2.index).dt.total_seconds()/60 # Compute time difference between timestamps in minutes
    #df2['dTL'] = df2['dTL'].div(1000) # Convert dT from miliseconds to seconds
    #df2['dTL'] = df2['dTL'].div(60) # Convert dT from seconds to minutes

    # Prepare stats:
    id_participant_text = "id_participant:                  " + df2.id_participant[0]
    dt_median =           "Median time between datapoints:  " + str(round(df2["dT"].median(),1)) + " minutes" # Median time between two responses if the difference is more than 0 seconds.
    dt_mean =             "Average time between datapoints: " + str(round(df2["dT"].mean(),1)) + " minutes"   # Median time between two responses if the difference is more than 0 seconds.
    num_entries =         "Number of datapoints:            " + str(df2[column_name].count())
    timestamp_first =     "First timestamp:                 " + str(df2.index[1].strftime('%H:%M:%S%Z, %d.%m.%Y'))
    timestamp_last =      "Last timestamp:                  " + str(df2.index[-1].strftime('%H:%M:%S%Z, %d.%m.%Y'))

    # Create figure
    fig, axs = plt.subplots(3,2, figsize=(15,10))
    fig.tight_layout(pad=5)
    fig.suptitle(column_name, fontsize=16)

    # Plot time-series
    axs[0][0].plot(df2.index, df2[column_name].values, marker='x')
    axs[0][0].set_xlabel('Time') 
    axs[0][0].set_ylabel(column_name)
    axs[0][0].yaxis.set_major_formatter(FormatStrFormatter('%.1f'))
    #date_format = mdates.DateFormatter('%d.%m - %H:%M %Z') # Define format for x-axis (with time zone)
    date_format = mdates.DateFormatter('%d. %b') # Define format for x-axis (without time zone and hour of day)
    date_format.set_tzinfo(timezone(YOUR_TIMEZONE))
    axs[0][0].xaxis.set_major_formatter(date_format) # Set format for x-axis
    axs[0][0].tick_params(axis='x', labelrotation=15) # Rotate xlabel by 45°
    #axs[0][0].set_xticklabels(axs[0][0].get_xticklabels(), ha='right', rotation_mode='anchor') # align xtick labels
    axs[0][0].set_title(column_name)
    axs[0][0].set_xlim([date_start, date_end])

    # Plot stats
    axs[0][1].set_title('Stats')
    axs[0][1].text(0.1, 0.9, id_participant_text, fontsize=12, family='monospace')# x, y, text,
    axs[0][1].text(0.1, 0.8, num_entries, fontsize=12, family='monospace')# x, y, text,
    axs[0][1].text(0.1, 0.7, timestamp_first, fontsize=12, family='monospace')
    axs[0][1].text(0.1, 0.6, timestamp_last, fontsize=12, family='monospace')
    axs[0][1].text(0.1, 0.5, dt_median, fontsize=12, family='monospace')
    axs[0][1].text(0.1, 0.4, dt_mean, fontsize=12, family='monospace')
    axs[0][1].get_yaxis().set_visible(False)
    axs[0][1].set_ylim([0.2, 1.2])
    axs[0][1].set_xlim([0.0, 2.0])
    axs[0][1].tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off
    axs[0][1].tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False) # labels along the bottom edge are off

    # Plot timestamp difference - scatter
    axs[1][0].plot(df2.index, df2['dT'], marker='x') # Plot histogram
    axs[1][0].set_xlabel('Time') 
    axs[1][0].set_ylabel('dT [min]')  
    axs[1][0].set_xlim([date_start, date_end])
    #axs[1][0].set_xticklabels(axs[1][0].get_xticklabels(), ha='right', rotation_mode='anchor') # align xtick labels
    #date_format = mdates.DateFormatter('%d.%m - %H:%M %Z') # Define format for x-axis (with time zone)
    date_format = mdates.DateFormatter('%d. %b') # Define format for x-axis (without time zone and hour of day)
    date_format.set_tzinfo(timezone(YOUR_TIMEZONE))
    axs[1][0].xaxis.set_major_formatter(date_format) # Set format for x-axis
    axs[1][0].tick_params(axis='x', labelrotation=15) # Rotate xlabel by 45°
    axs[1][0].set_title('Duration between Timestamps')

    # Plot timestamp difference - histogram
    if len(df2['dT'].values)>1: # Skip the histogram if there is not at least two values in the dataframe.
      axs[1][1].hist(df2['dT'].values, bins=100, edgecolor='black')
      axs[1][1].set_xlabel('Duration [min]') 
      axs[1][1].set_ylabel('Counts [#]')
      axs[1][1].set_title('Duration between Timestamps (Histogram)')

    # Plot timestamp difference (index-timestamp -lambda-timestamp) - scatter
    axs[2][0].plot(df2.index, df2['dTL'], marker='x') # Plot histogram
    axs[2][0].set_xlabel('Time') 
    axs[2][0].set_ylabel('dTL [min]')
    axs[2][0].set_xlim([date_start, date_end])
    #axs[2][0].set_xticklabels(axs[2][0].get_xticklabels(), ha='right', rotation_mode='anchor') # align xtick labels
    #date_format = mdates.DateFormatter('%d.%m - %H:%M %Z') # Define format for x-axis (with time zone)
    date_format = mdates.DateFormatter('%d. %b') # Define format for x-axis (without time zone and hour of day)
    date_format.set_tzinfo(timezone(YOUR_TIMEZONE))
    axs[2][0].xaxis.set_major_formatter(date_format) # Set format for x-axis
    axs[2][0].tick_params(axis='x', labelrotation=15) # Rotate xlabel by 45°
    axs[2][0].set_title('Duration between timestamp_lambda and index')

    # Plot timestamp difference (index-timestamp -lambda-timestamp)- histogram
    if len(df2['dTL'].values)>1: # Skip the histogram if there is not at least two values in the dataframe.
      axs[2][1].hist(df2['dTL'].values, bins=100, edgecolor='black')
      axs[2][1].set_xlabel('Duration [min]') 
      axs[2][1].set_ylabel('Counts [#]')
      axs[2][1].set_title('Duration between Timestamps (Histogram)')

    plt.show()
    
    return fig, axs
  
  def ts_inspection2(self, column_name, id_participant):  
    """
    Function to plot time-series data in detail for one participant
    Arguments
    ----------
      - column_name, str, Name of column with time-series data that should be plotted
      - id_participant, str, Participant ID of which the time-series data should be plotted
    Returns
    -------
      - fig, ?, Plotly figure object
    """

    # Input processing
    df = self.df.copy()
    modality = column_name

    # Data processing
    # Filter data
    df_participant = df[(df.id_participant == id_participant) & (df[modality].notna())]
    df_all = df[(df[modality].notna())]# create the bins
    modality_min = df_all[modality].min()
    modality_max = df_all[modality].max()

    # Create histograms
    counts_all, bins_all = np.histogram(df_all[modality], bins=range(int(modality_min), int(modality_max), 5), density=True)
    bins_all = 0.5 * (bins_all[:-1] + bins_all[1:])

    counts_participant, bins_participant = np.histogram(df_participant[modality], bins=range(int(modality_min), int(modality_max), 5), density=True)
    bins_all = 0.5 * (bins_participant[:-1] + bins_participant[1:])

    # Create data for heatmap
    df_heatmap = df_participant.copy()
    df_heatmap = df_heatmap[df_heatmap[modality].notna()]
    df_heatmap["hourly"] = df_heatmap[modality].resample('H').mean()
    df_heatmap['hour'] = df_heatmap.index.hour
    df_heatmap['date'] = df_heatmap.index.date

    # Plotting
    fig = make_subplots(rows=2, cols=2,subplot_titles=("Time Series", "Histogram (normalized)", "Heatmap", "Stats"))

    # Plot 1 - Time-Series
    fig.add_trace(go.Scatter(x=df_all.index, y=df_all[modality],
                            mode="markers",
                            marker=dict(color="lightgrey")),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=df_participant.index, y=df_participant[modality],
                            mode="markers"),
                  
                  row=1, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_yaxes(title_text=modality, row=1, col=1)


    # Plot 2 - Histogram
    fig.add_trace(go.Bar(x=bins_all, y=counts_all, marker_color="lightgrey"),
                  row=1, col=2)

    fig.add_trace(go.Bar(x=bins_participant, y=counts_participant),
                  row=1, col=2)

    fig.update_xaxes(title_text=modality, row=1, col=2)
    fig.update_yaxes(title_text="Probability Density [-]", row=1, col=2)


    # Plot 3 - Heat Map
    fig.add_trace(go.Heatmap(x=df_heatmap[df_heatmap.hourly.notna()].date,
                            y=df_heatmap[df_heatmap.hourly.notna()].hour,
                            z=df_heatmap[df_heatmap.hourly.notna()].hourly,
                            colorscale='YlOrRd'),
                  row=2, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text='Time of Day', row=2, col=1)

    # Plot 4 - Stats
    x_bar = ["Min", "Median", "Mean", "Max"]
    y_bar = [df_participant[modality].min(),
            df_participant[modality].median(),
            df_participant[modality].mean(),
            df_participant[modality].max(),
            ]
    fig.add_trace(go.Bar(x = x_bar, y=y_bar),
                  row=2, col=2)
    fig.update_yaxes(title_text=modality, row=2, col=2)

    fig.update_layout(height=1200, width=1200, title_text=modality)
    fig.show()
    return fig

  def cohort_survey_count_bar(self, valid_votes = True):
    """
    Function to plot bar chart of ws_survey_count for all participants
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    fig, ax = plt.subplots(1,1, figsize=(15,10))
    df2 =(df[df["ws_survey_count"].notna()]
    .groupby("id_participant")
    .resample('D')["ws_survey_count"]
    .count()
    .unstack()
    .T)

    df2.plot(kind='bar', 
          title=f'ws_survey_count counts daily, individual {valid_votes_title}', 
          ylabel='Counts', 
          xlabel='Date', 
          figsize=(25, 7),
          ax=ax)

    # Make most of the ticklabels empty so the labels don't get too crowded
    ticklabels = ['']*len(df2.index)
    # Every 7th ticklable shows the month and day
    ticklabels[::7] = [item.strftime('%b %d') for item in df2.index[::7]]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
    plt.gcf().autofmt_xdate()

    ax.legend(loc=(1.05, 0.5))

    plt.show()
    return fig, ax
  

  def cohort_survey_count_bar2(self, participant_list=None, valid_votes=True):
    """
    Function to plot bar chart of ws_survey_count for all participants
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, plotly figure object
    """
    df = self.df.copy()
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    if participant_list == None:
      participant_list = self.participant_list

    # Cumulate data
    df2 =(df[df["ws_survey_count"].notna()]
    .groupby("id_participant")
    .resample('D')["ws_survey_count"]
    .count()
    .unstack()
    .T)
    
    # Add missing participants as empty columns
    for id_participant in participant_list:
      if id_participant not in df2.columns:
        df2[id_participant] = pd.Series(dtype='float64')

    # Plot data
    fig = px.bar(df2, x=df2.index, y=df2.columns, 
                barmode='group',
                title=f'ws_survey_count counts daily, individual {valid_votes_title}',
                width = 800,
                height = 400)
    fig.update_layout(yaxis_title = "ws_survey_count [#]",
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants')
    fig.show()
    return fig

    
  def cohort_all_survey_count_bar(self, valid_votes=True):
    """
    Function to plot bar chart of the sum of ws_survey_count for all participants
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    df2 = (df[df["ws_survey_count"].notna()]
    .resample('D')["ws_survey_count"]
    .count()
    )

    fig, ax = plt.subplots(1,1, figsize=(25,7))
    ax.bar(df2.index, df2.values)
    ax.set_title(f'ws_survey_count counts daily, all {valid_votes_title}')
    ax.set_ylabel('Counts') 
    ax.set_xlabel('Date')

    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.tick_params(axis='x', labelrotation=0) # Rotate xlabel

    plt.show()
    return fig, ax
  
   
  def cohort_all_survey_count_bar2(self, valid_votes=True):
    """
    Function to plot bar chart of the sum of ws_survey_count for all participants using Plotly
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, plotly figure object
    """
    df = self.df.copy()
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data    
    df2 = (df[df["ws_survey_count"].notna()]
    .resample('D')["ws_survey_count"]
    .count()
    )

    # Plot data
    fig = px.bar(df2, x=df2.index, y=df2.values, 
                title=f'ws_survey_count counts daily, all participants {valid_votes_title}',
                width = 800,
                height = 400)
    fig.update_layout(yaxis_title = "ws_survey_count [#]",
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants')
    fig.show()
    return fig

  def cohort_individual_survey_count_bar(self, participant_list=None, valid_votes=True):
    """
    Function to plot bar chart of ws_survey_count for individual participants
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    if participant_list == None:
      participant_list = self.participant_list

    fig, ax = plt.subplots(1,1, figsize =(20, 10))
    ax = (df[df["ws_survey_count"].notna()]
    .groupby("id_participant")["ws_survey_count"]
    .count()
    .plot(kind='bar', 
          title=f'ws_survey_count counts overall, individual {valid_votes_title}', 
          ylabel='Counts', 
          xlabel='Participants', 
          figsize=(25, 7))
    )
    ax.tick_params(axis='x', labelrotation=0)

    return fig, ax

  def cohort_individual_survey_count_bar2(self, participant_list=None, valid_votes=True):
    """
    Function to plot bar chart of ws_survey_count for individual participants
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, matplotlib figure object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    if participant_list == None:
      participant_list = self.participant_list

    # Process data
    df2 = (df[df["ws_survey_count"].notna()]
    .groupby("id_participant")["ws_survey_count"]
    .count()
    )
      
    fig = px.bar(df2, x=df2.index, y=df2.values, 
                title=f'ws_survey_count counts daily, all participants {valid_votes_title}',
                width = 800,
                height = 400)
    fig.update_layout(yaxis_title = "ws_survey_count [#]",
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants')
    fig.show()
    return fig

  def cohort_survey_count_line(self, valid_votes=True):
    """
    Function to plot bar chart of the sum of ws_survey_count for all participants using Matplotlib
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data
    df = df[df.ws_survey_count.notna()]
    df['ws_survey_count_count'] = (df
    .groupby('id_participant')["ws_survey_count"]
    .cumcount()
    )

    # Plot data
    fig, ax = plt.subplots(1,1, figsize=(15,10))
    (df
    .groupby('id_participant')["ws_survey_count_count"]
    .plot(kind='line', 
          title=f'ws_survey_count cumcounts, individual {valid_votes_title}', 
          ylabel='Counts', 
          xlabel='Date', 
          legend=True,
          figsize=(25, 7),
          ax=ax)
    )
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax.get_legend().set_title("Participants")
    return fig, ax

  def cohort_survey_count_line2(self, participant_list=None, valid_votes=True):
    """
    Function to plot bar chart of the sum of ws_survey_count for all participants using Plotly
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    if participant_list == None:
      participant_list = self.participant_list
    
    # Process data
    df = df[df.ws_survey_count.notna()]
    df['ws_survey_count_count'] = (df
    .groupby('id_participant')["ws_survey_count"]
    .cumcount()
    )

    # Plot data
    first = True
    for id_participant in participant_list:
      df2 = df[df["id_participant"]==id_participant]
      if first: 
        fig = px.line(x=df2.index, y=df2["ws_survey_count_count"], width = 800, height = 400)
        first = False
      fig.add_trace(go.Scatter(x=df2.index, y=df2["ws_survey_count_count"], name=id_participant, mode='lines'))

    fig.update_layout(title = f'Cohort cummulative ws_survey_count, individual {valid_votes_title}',
                      yaxis_title = 'Cummulative ws_survey_count [#]',
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants')
    fig.show()
    return fig

  def cohort_all_survey_count_line(self, valid_votes=True):
    """
    Function to plot line chart of the cumsum of ws_survey_count for all participants using Matplotlib
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes
    
    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data
    df["ws_survey_count_count"] = df["ws_survey_count"].notnull().astype('int').cumsum()

    # Plot data
    fig, ax = plt.subplots(1,1, figsize =(20, 10))
    (df["ws_survey_count_count"]
    .plot(kind='line', 
          title=f'ws_survey_count cumcounts, all {valid_votes_title}', 
          ylabel='Counts', 
          xlabel='Date', 
          ax=ax,
          figsize=(25, 7))
    )
    ax.legend(["All participants"])
    ax.set_xlim([df.index[0], df.index[-1]])

    plt.show()
    return fig, ax

  def cohort_all_survey_count_line2(self, valid_votes=True):
    """
    Function to plot line chart of the cumsum of ws_survey_count for all participants using Plotly
    
    Arguments
    ----------
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df = self.df.copy()

    # Process data
    df["ws_survey_count_count"] = df["ws_survey_count"].notnull().astype('int').cumsum()
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Plot data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["ws_survey_count_count"], name="All Participants", mode='lines'))
    fig.update_layout(title = f'Cohort cummulative ws_survey_count, all participants {valid_votes_title}',
                      yaxis_title = 'Cummulative ws_survey_count [#]',
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants',
                      showlegend=True)
    fig.show()
    return fig
  
  def cohort_all_survey_count_line3(self, participant_list=None, valid_votes=True):
    """
    Function to plot line chart of the cumsum of ws_survey_count for entire cohort and individual participants using Plotly
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df_all = self.df.copy()
    df = self.df.copy()
    if participant_list == None:
      participant_list = self.participant_list

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data for individual participants
    df = df[df.ws_survey_count.notna()]
    df['ws_survey_count_count'] = (df.groupby('id_participant')["ws_survey_count"]
                                .cumcount())

    # Process data for all
    df_all["ws_survey_count_count"] = df_all["ws_survey_count"].notnull().astype('int').cumsum()

    # Plot data for all
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_all.index, y=df_all["ws_survey_count_count"], name="All Participants", mode='lines'))
    fig.update_layout(title = f'Cohort cummulative ws_survey_count, all participants {valid_votes_title}',
                      yaxis_title = 'Cummulative ws_survey_count [#]',
                      title_x=0.5,
                      xaxis_title = 'Date',
                      legend_title = 'Participants',
                      showlegend=True)
    
    # Plot data for individual participants
    for id_participant in participant_list:
      df2 = df[df["id_participant"]==id_participant]
      fig.add_trace(go.Scatter(x=df2.index, y=df2["ws_survey_count_count"], name=id_participant, mode='lines'))

    fig.show()
    return fig
  
  def cohort_dt_swarm(self, participant_list=None, threshold=None, valid_votes=True):
    """
    Function to plot swarm chart of the time between two ws_survey_count timestmaps for 
    individual participants with Matplotlib/Seaborn
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """

    df = self.df.copy()
    if participant_list == None:
      participant_list = self.participant_list
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data
    df = df[df.ws_survey_count.notna()]

    # Plot data
    fig, ax = plt.subplots(1,1, figsize =(20, 10))
    #axs[0].set_ylim([0,120]) # y limits need to be applied before plotting
    sns.swarmplot(data=df, x="id_participant", y="dT", ax=ax, order=participant_list)
    
    ax.set_ylabel("Duration between two micro-survey responses [min]")
    ax.set_title(f"Duration between two micro-survey responses {valid_votes_title}")

    # Draw red line
    if threshold != None:
      (xmin, xmax) = ax.get_xlim()
      ax.hlines(threshold, xmin, xmax, colors="red")
      
    plt.show()
    return fig, ax
  

  def cohort_dt_swarm2(self, participant_list=None, threshold=None, valid_votes=True):
    """
    Function to plot swarm chart of the time between two ws_survey_count timestmaps for 
    individual participants with Plotly
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df = self.df.copy()
    if participant_list == None:
      participant_list = self.participant_list
    
    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    df = df[df.ws_survey_count.notna()]

    fig = px.strip(df, x="id_participant", y="dT")
    fig.update_layout(title = f'Cohort cummulative ws_survey_count, all participants {valid_votes_title}',
                      title_x=0.5,
                      yaxis_title = 'Duration between two micro-survey responses [min]',
                      xaxis_title = 'Participants',
                      showlegend=True,
                      yaxis_range=[0,1200])
    fig.add_hline(y=55, line_width=1, line_dash="solid", line_color="red")
    fig.show()

    return fig

  def cohort_dt_hist(self, threshold=None, valid_votes=True):
    """
    Function to plot histogram of the time between two ws_survey_count timestmaps 
    for individual participants with Matplotlib/Seaborn
    
    Arguments
    ----------
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Plot data
    fig, ax = plt.subplots(1,1, figsize =(20, 10))
    df.hist(column="dT", bins=range(1, 600, 5), ax=ax)
    ax.set_ylabel("Counts [-]")
    ax.set_xlabel("Duration [h]")
    ax.set_title(f"Histogram - Duration between two watch survey responses {valid_votes_title}")
    # Convert x-tick labels from minute to hour
    ticks = list(range(-60, 600, 60))
    labels = []
    for tick in ticks:
      label_int = tick/60
      label_str = '%d' % (label_int,)
      labels.append(label_str)
    _=ax.set_xticks(ticks)
    _=ax.set_xticklabels(labels)

    # Draw red line
    if threshold != None:
      (ymin, ymax) = ax.get_ylim()
      ax.vlines(threshold, ymin, ymax, colors="red")
    plt.show()
    return fig, ax
  
  def cohort_dt_hist2(self, threshold=None, valid_votes=True):
    """
    Function to swarm chart chart of the time between two ws_survey_count timestmaps for individual participants with Matplotlib/Seaborn
    
    Arguments
    ----------
      - participant_list, list of str, List of participant IDs
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data
    df["dT"] = df["dT"]/60

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="count", 
                               x=df["dT"].values, 
                               xbins=dict(
                                  start=0,
                                  end=12,
                                  size=1/12)))

    fig.update_layout(title = f'Histogram - Duration between two watch survey responses {valid_votes_title}',
                      title_x=0.5,
                      yaxis_title = 'Counts [#]',
                      xaxis_title = 'Duration [h]',
                      xaxis_range=[0,12],
                      width = 800,
                      height = 400)
    
    if threshold != None:
      threshold = threshold/60
      fig.add_vline(x=threshold, line_width=1, line_dash="solid", line_color="red")

    fig.show()
    return fig
  
  def cohort_threshold_undercut(self, threshold, valid_votes=True):
    """
    Function to plot bar chart of cummulative thresholed exeedances per participant
    
    Arguments
    ----------
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Plot data
    fig, ax = plt.subplots(1,1, figsize =(20, 10))
    ax = (df[df['dT']<threshold].groupby(['id_participant'])["ws_survey_count"]
                    .count()
                    .plot(kind='bar', 
                          title=f'Instances where the duration between two watch survey responses that are less than {threshold} min {valid_votes_title}', 
                          ylabel='Counts [x]', 
                          xlabel='Participants', 
                          figsize=(25, 7))
    )
    ax.tick_params(axis='x', labelrotation=0)

    plt.show()
    return fig, ax
  
  def cohort_threshold_undercut2(self, threshold, valid_votes=True):
    """
    Function to plot bar chart of cummulative thresholed exeedances per participant
    
    Arguments
    ----------
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, Plotly figure object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    # Process data
    df2 = df[df['dT']<threshold].groupby(['id_participant'])["ws_survey_count"].count()

    # Plot data
    fig = px.bar(df2, x=df2.index, y=df2.values, 
                barmode='group',
                title=f'Instances where the duration between two watch survey responses that are less than {threshold} min {valid_votes_title}',
                width = 800,
                height = 400)
    fig.update_layout(yaxis_title = "Counts [#]",
                      title_x=0.5,
                      xaxis_title = 'Participants')
    fig.show()

    return fig
  
  def cohort_treshold_report(self, threshold, valid_votes=True):
    """
    Function to print some stats about the threshold of duration between two cote_counts
    
    Arguments
    ----------
      - threshold, int, Minimal allowed duration between two watch_survey responses in minutes
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - 
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"
    
    print(f"Total votes less than {threshold}min apart:", df[df['dT']<threshold].ws_survey_count.count())
    print(f"Total votes more or equal than {threshold}min apart:", df[df['dT']>=threshold].ws_survey_count.count())

  def cohort_ws_inspection(self, ws_questions, valid_votes=True):
    """
    Function to plot bar chart with the responses to the watch surveys for the entire cohort with Matplotlib
    
    Arguments
    ----------
      - ws_questions, dict, Dictionary with watch survey questions IDs and question texts
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, matplotlib figure object
      - ax, ?, matplotlib axis object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    number_of_questions = len(ws_questions) + 1
    number_of_columns = 2
    number_of_rows = math.ceil(number_of_questions/number_of_columns)+1

    # Add column for questions for which no responses were logged for current question
    for question in ws_questions:
      if question not in df.columns:
        df[question] = None

    fig, axs = plt.subplots(number_of_rows, number_of_columns, figsize =(18, 25))
    fig.tight_layout(pad=7.5)
    gs = fig.add_gridspec(number_of_rows,number_of_columns)
    axs2 = fig.add_subplot(gs[number_of_rows-1, :])

    current_row = 0
    current_column = 0
    my_dict = {}

    # Bar charts of responses to individual questions
    for index, (question_id, question_value) in enumerate(ws_questions.items()):
      current_row = math.ceil((index+1)/number_of_columns)-1
      current_column = index % number_of_columns
      # Skip supplot if no responses were logged for current question
      if df[question_id].count()==0:
        my_dict[question_value] = 0
      else:
        my_dict[question_value] = df[question_id].count()
        df[question_id].value_counts().plot(kind='barh', ax = axs[current_row,current_column])
      title_wrapped = wrap(question_value, 40)
      title_wrapped = "\n".join(title_wrapped)
      axs[current_row,current_column].set_title(title_wrapped, fontsize=20)
      axs[current_row,current_column].set_ylabel("Responses", fontsize=16)
      axs[current_row,current_column].set_xlabel("Counts [#]", fontsize=16)
      axs[current_row,current_column].xaxis.set_major_formatter(FormatStrFormatter('%.0f')) # Remove decimals from x-tick labels
      

    # Bar chart of sum of all responses per question
    labels = []
    for key in my_dict.keys():
      label_wrapped = wrap(key, 20)
      label_wrapped = "\n".join(label_wrapped)
      labels.append(label_wrapped)

    axs2.bar(labels, my_dict.values())
    axs2.set_title("Overview", fontsize=20)
    axs2.set_ylabel("Counts [#]", fontsize=16)
    axs2.set_xlabel("Questions", fontsize=16)
    #axs2.tick_params(axis='x', labelrotation=45) # Rotate xlabel by 45°
    plt.setp(axs2.get_xticklabels(), rotation=55, ha="right", rotation_mode="anchor") 

    # Remove redundant tick labels
    axs[number_of_rows-1,0].set_xticks([])
    axs[number_of_rows-1,0].set_yticks([])
    axs[number_of_rows-1,1].set_xticks([])
    axs[number_of_rows-1,1].set_yticks([])

    plt.show()

    return fig, axs


  def cohort_ws_inspection2(self, ws_questions, valid_votes=True): 
    """
    Function to plot bar chart with the responses to the watch surveys for the entire cohort with Matplotlib
    
    Arguments
    ----------
      - ws_questions, dict, Dictionary with watch survey questions IDs and question texts
      - valid_votes, bool, indicates whether to use only valid votes (default) or all votes

    Returns
    -------
      - fig, ?, plotly figure object
    """
    df = self.df.copy()

    # Filter for valid votes
    valid_votes_title = "(all votes)"
    if "valid_vote" in df.columns:
      if valid_votes == True: 
        df = df[df["valid_vote"]==True]
        valid_votes_title = "(only valid votes)"

    number_of_questions = len(ws_questions) + 1
    number_of_columns = 2
    number_of_rows = math.ceil(number_of_questions/number_of_columns)
   
   # Add column for questions for which no responses were logged for current question
    for question in ws_questions:
      if question not in df.columns:
        df[question] = None

    my_dict = {}
    list_row = []
    list_col = []
    list_traces = []
    list_titles = []

    # Bar charts of responses to individual questions
    for index, (question_id, question_value) in enumerate(ws_questions.items()):
      current_row = math.ceil((index+1)/number_of_columns)
      current_column = index % number_of_columns+1
      if df[question_id].count()==0:
        my_dict[question_value] = 0
        continue
      my_dict[question_value] = df[question_id].count()

      df2 = df[question_id].value_counts()
      title_wrapped = wrap(question_value, 30)
      title_wrapped = "<br>".join(title_wrapped)
      list_titles.append(title_wrapped)
      list_row.append(current_row)
      list_col.append(current_column)
      list_traces.append(go.Bar(x=df2.values, 
                                y=df2.index.values, 
                                orientation='h'))
    
    # Create subplot layout  
    list_specs = []
    for i in range(1, number_of_rows):
      list_specs.append([{}, {}])
    #list_specs.append([{'colspan': 2}, None])
    list_specs.append([{}, {}])

    # Add title of last plot to list
    list_titles.append('Total number of responses per question')

    # Create figure  
    fig = make_subplots(rows=number_of_rows, 
                        cols=number_of_columns,
                        vertical_spacing = 0.1,
                        horizontal_spacing = 0.3,
                        subplot_titles= list_titles,
                        specs=list_specs)  # make specs adapt to the number of questions
    
    # Add traces to figure
    for i, trace in enumerate(list_traces):
      fig.add_trace(trace, list_row[i], list_col[i])
      fig.update_xaxes(title_text='Counts [#]', row=list_row[i], col=list_col[i])
      fig.update_yaxes(title_text='Response Options', row=list_row[i], col=list_col[i])

    # Bar chart of sum of all responses per question
    labels = []
    for key in my_dict.keys():
      label_wrapped = wrap(key, 20)
      label_wrapped = "\n".join(label_wrapped)
      labels.append(label_wrapped)

    values = list(my_dict.values())
    print("labels:\n", labels)
    print(len(labels))
    print("values:\n", values)
    print(len(values))
    # TO DO: finish development of function

    trace2 = go.Bar(x=['A','B','C'], y=[3,8,5])
    fig.add_trace(trace2, number_of_rows, 1)
    fig.update_xaxes(title_text='Questions', row=number_of_rows, col=1)
    fig.update_yaxes(title_text='Counts [#]', row=number_of_rows, col=1)

    fig.update_layout(height=1400, width=1000, showlegend = False)

    fig.show()

    return fig