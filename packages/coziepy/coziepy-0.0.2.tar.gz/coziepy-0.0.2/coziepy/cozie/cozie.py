#import requests
#import numpy as np
#import time
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates  
#from matplotlib.ticker import FormatStrFormatter
#import seaborn as sns
#from pytz import timezone
import pandas as pd
from influxdb import DataFrameClient
import json
import requests
import shutil
import os
import datetime
import pytz


#print("Cozie Module start")
class Cozie:
  """
  Class to retrieve and process Cozie-Apple data
  """

  def __init__(self):   
    """
    Constructor initializes class attributes and prints test string
    
    Arguments
    ----------
      -
    
    Returns
    -------
      -
    """
    self.participant_list = []
    self.df = []
    self.test_string = 'CoziePy Test String'

  def test(self):    
    """
    Function for testing, prints test string
    
    Arguments
    ----------
      -   
    
    Returns
    -------
      - test_string, str, String for testing
    """
    print("test")
    print(self.test_string)
    return self.test_string

  def load(self,
           host = None,
           port = None,
           user = None,
           password = None,
           database = None,
           timezone = None,
           id_experiment = None,
           participant_list = [],
           settings_file = None,
           input_file = None,
           log_file = None,
           output_file = None,
           api_url = None,
           api_key = None,
           clean_up = True):    
    """
    Function for querying Cozie data from InfluxDB
    
    Arguments
    ----------
      host :  str, InfluxDB Server URL
      port : int, InfluxDB Server Port
      user : str, InfluxDB username
      password : str, InfluxDB password
      database : str, IndluxDB database name
      timezone : str, Timezone of participants
      id_experiment : str, name of experiment, i.e., 'measurement' in InfluxDB
      participant_list : list of str, participant IDs
      settings_file : str, Path to text file with credentials and settings, instead of arguments listed above
      output_file : str, Path to text file with Cozie data or where Cozie data should be saved
      input_file : str, Path to text file with Cozie data or where Cozie data should be loaded from
      log_file : str, Path to text file with Cozie data from Cozie app
      api_url : str, URL to Cozie data retrieval web API
      api_key : str, key for Cozie data retrieval web API
      
    Returns
    -------
      df : Pandas dataframe, Dataframe with micro surveys
    """  
    
    #  Check participant_list
    if participant_list is not None:
      self.participant_list = participant_list

    # Check timzone
    if timezone is not None:
      self.timezone = timezone
    else:
      # Get system timzone
      self.timezone = 'UTC'

    # Check input data file
    if input_file is not None:
      df = pd.read_parquet(input_file)
      self.participant_list = df["id_participant"].unique()
      self.df = df
      return df
    
    # Check api parameter
    elif api_url is not None:
      # Retrieve data from web API
      df_raw = self.load_from_api(id_experiment, participant_list, api_url, api_key)

    # Check settings file
    elif settings_file is not None: 
      file = open(settings_file)
      settings = json.load(file) 
      host = settings["host"]
      port = settings["port"]
      user = settings["user"]
      password = settings["password"]
      database = settings["database"]
      timezone = settings["timezone"]
      id_experiment = settings["id_experiment"]
      participant_list = settings["participant_list"]
      output_file = settings["output_file"]

      df_raw = self.load_from_influx(host, port, user, password, database, id_experiment, participant_list)
    
    elif host is not None:
       df_raw = self.load_from_influx(host, port, user, password, database, id_experiment, participant_list)
      
    elif log_file is not None:
      df_raw = self.load_from_log_file(log_file)

    # Clean up raw dataframe
    if clean_up == True:
      df = self.clean_up_raw_dataframe(df_raw)
    else:
      df = df_raw

    # Save dataframe to class attribute
    self.df = df

    # Save dataframe to parquet file
    if output_file is not None:
      print("output_file:", output_file)
      df.to_parquet(output_file, compression='gzip', engine="fastparquet")
    
    return df

  def clean_up_raw_dataframe(self, df):
    """
    Function for cleaning up raw dataframe with Cozie data:
     - parses dates that are stored as strings
     - Localizes timestamps witht the timezone
     - computes differences between timestamps
     - sorts index
    
    Arguments
    ----------
      df : Pandas dataframe, Dataframe with raw Cozie data from the database
    
    Returns
    -------
      df : Pandas dataframe, Dataframe with processed Cozie data
    """
    df = df.sort_index(ascending=False)

    # Convert index to local timezone
    df.index = df.index.tz_convert(self.timezone)

    # Order timestmaps
    df.sort_index(inplace=True, ascending=True)

    # Rename columns for compatibility between Cozie v2 and v3
    df = df.rename(columns={"vote_count": "ws_survey_count", 
                            "timestamp_location": "ws_timestamp_location", 
                            "timestamp_start": "ws_timestamp_start"})

    # Parse timestamp_lambda
    df["timestamp_lambda"] = pd.to_datetime(df["timestamp_lambda"], format="%Y-%m-%dT%H:%M:%S.%f%z", errors='coerce')

    # Parse ws_timestamp_location
    df["ws_timestamp_location"] = pd.to_datetime(df["ws_timestamp_location"], format="%Y-%m-%dT%H:%M:%S.%f%z", errors='coerce')
    #df["ws_timestamp_location"] = df["ws_timestamp_location"].tz_convert(self.timezone)

    # Parse timestamp_start
    df["ws_timestamp_start"] = pd.to_datetime(df["ws_timestamp_start"], format="%Y-%m-%dT%H:%M:%S.%f%z", errors='coerce')
    #df["ws_timestamp_start"] = df["ws_timestamp_start"].tz_convert(self.timezone)

    # Compute timestamp differences
    #print('index', df.index[0])
    df['timestamp'] = pd.to_datetime(df.index)
    df['timestamp'] = df.index

    #print('timestamp', df.timestamp[0])

    #df["timestamp"] = df["timestamp"].tz_convert('Asia/Singapore')
    #print('timestamp', df.timestamp[0])
    
    # Reset index to avoid reindexing issues with duplicate timestamps
    df = df.reset_index()
    df = df.rename(columns={'index': 'time'})

    grouped = df[df["ws_survey_count"].notna()].groupby('id_participant')

    for id_participant, group in grouped:
      df.loc[df.id_participant==id_participant, 'dT'] = group['timestamp'].diff().dt.total_seconds().div(60)

    # Undo index reset
    df.index = df['time']
    df = df = df.drop(columns=['time'])
    df = df.rename_axis(None, axis=1) # Remove name of index

    return df
  
  def load_from_api(self, id_experiment, participant_list, api_url, api_key):
    """
    Function for retrieving Cozie data using the web api
    
    Arguments
    ----------
      id_experiment : str, name of experiment, i.e., 'measurement' in InfluxDB
      participant_list : list of str, participant IDs
      api_url : str, URL to Cozie data retrieval web API
      api_key : str, key for Cozie data retrieval web API
    
    Returns
    -------
      df : Pandas dataframe, Dataframe with raw Cozie data
    """
  # Initialize temprorary dataframe
    df_all = pd.DataFrame()
    
    # Query data for each participant
    for participant in participant_list:
        
      print('Download data for', participant)
      
      # Query data
      payload = {'id_participant': participant,'id_experiment': id_experiment, 'weeks': 2000}
      headers = {"Accept": "application/json", 'x-api-key': api_key}
      response = requests.get(api_url, params=payload, headers=headers)
      url = response.content

      # Download zipped CSV file with Cozie data
      with requests.get(url, stream=True) as r:
          with open('cozie.zip', 'wb') as f:
              shutil.copyfileobj(r.raw, f)

      # Convert zipped CSV file with Cozie to dataframe
      with open('cozie.zip', 'rb') as f:
            df = pd.read_csv(f, compression={'method': 'zip', 'archive_name': 'sample.csv'})
      
      if df.empty:
          print("No data found.")

      df = df.drop(columns=['Unnamed: 0'])
      df['index'] = pd.to_datetime(df['index'])
      df = df.set_index('index')
      
      # Store data of current participant in dataframe for all participants
      df_all = pd.concat([df_all, df])
      
      # Delete zip file
      os.remove('cozie.zip')
        
    # Sort data by date
    df_raw = df_all.sort_index()

    return df_raw
  
  def load_from_influx(self, host, port, user, password, database, id_experiment, participant_list):
    """
    Function for retrieving Cozie data with direct access to InfluxDB
    
    Arguments
    ----------
      host :  str, InfluxDB Server URL
      port : int, InfluxDB Server Port
      user : str, InfluxDB username
      password : str, InfluxDB password
      database : str, IndluxDB database name
      id_experiment : str, name of experiment, i.e., 'measurement' in InfluxDB
      participant_list : list of str, participant IDs
      settings_file : str, Path to text file with credentials and settings, instead of arguments listed above
      output_file : str, Path to text file with Cozie data or where Cozie data should be saved
      input_file : str, Path to text file with Cozie data or where Cozie data should be loaded from
      api_url : str, URL to Cozie data retrieval web API
      api_key : str, key for Cozie data retrieval web API    

    Returns
    -------
      df : Pandas dataframe, Dataframe with raw Cozie data
    """
     # Initialize InfluxDB client
    client = DataFrameClient(host, port, user, password, database, ssl=True, verify_ssl=True)

    # Get list of participants
    if (participant_list is None) or (participant_list == []):
      print("participant list is None or []")
      query = f'SHOW TAG VALUES ON "{database}" FROM "{id_experiment}" WITH KEY = "id_participant"'
      result = client.query(query)
      for item in result[id_experiment]:
        participant_list.append(item.get("value"))

    df_raw = pd.DataFrame()

    # Query influx
    for participant in participant_list:
      query = f'SELECT * FROM "cozie-apple"."autogen"."{id_experiment}" WHERE "id_participant"=\'{participant}\''
      print("Query:", query)

      # Get result
      result = client.query(query=query, epoch='ns')
      #print("\nResult:\n", result)
      df_participant = pd.DataFrame.from_dict(result[id_experiment])
      df_raw = pd.concat([df_raw, df_participant])

    return df_raw
  
  def load_from_log_file(self, log_file):
    """
    Function for retrieving Cozie data from Cozie app log file
    
    Arguments
    ----------
      log_file  : str, Path to text file with Cozie data from Cozie app
      output_file : str, Path to text file with Cozie data or where Cozie data should be saved

    Returns
    -------
      df : Pandas dataframe, Dataframe with raw Cozie data
    """
    # Read log file
    file = file1 = open(log_file, "r")
    file_content = file.read()
    data = json.loads(file_content)

    # Parse content of log file
    list_rows = []
    for log_item in data:
      # Combine log items into one dict i.e., row
      if type(log_item) is not list:
        log_item = [log_item]
      for log_sub_item in log_item:
        fields = log_sub_item["fields"]
        tags = log_sub_item["tags"]
        fields.update(tags)
        fields["time"] = log_sub_item["time"]
        fields["id_experiment"] = log_sub_item["measurement"]
        list_rows.append(fields)

    # Convert list of dicts to dataframe
    df_raw = pd.DataFrame.from_dict(list_rows)

    # For 'time' column: convert string to timestamp
    df_raw["time"] =  pd.to_datetime(df_raw["time"])

    # Convert 'time' column to index
    df_raw = df_raw.set_index(["time"])

    # Reorder some columns
    primary_col_names = ["id_experiment", "id_participant", "id_password"]
    for name in reversed(primary_col_names):
      temp_col = df_raw.pop(name)
      df_raw.insert(0, name, temp_col)
    
    # Add column for timestamp_lambda
    df_raw['timestamp_lambda'] =  datetime.datetime.now().astimezone(pytz.timezone(self.timezone)).strftime("%Y-%m-%dT%H:%M:%S.%f%z")

    return df_raw
    
  def keep_valid_votes_participant(self, df_participant, threshold):
    """
    Function for removing invalid watch survey responses for one participant
    
    Arguments
    ----------
      df :  Pandas dataframe, Dataframe with Cozie data for one participant

    Returns
    -------
      df_output : Pandas dataframe, Dataframe with processed Cozie data
    """  
    #df_participant = df_participant[df_participant.ws_survey_count.notna()]
    #df_output = df_participant.copy()
    timestamp_previous_valid = -1

    for timestamp, row in df_participant[df_participant.ws_survey_count.notna()].iterrows():

      # Skip first entry
      if timestamp_previous_valid==-1:
        timestamp_previous_valid = timestamp
        df_participant.at[timestamp, "valid_vote"] = True
        continue

      # Compute time difference between ws_survey_counts
      timestamp_diff = (timestamp-timestamp_previous_valid).total_seconds()/60
      if timestamp_diff>threshold:
        timestamp_previous_valid = timestamp
        df_participant.at[timestamp, "valid_vote"] = True
        df_participant.at[timestamp, "dT_valid"] = timestamp_diff
      else: 
        df_participant.at[timestamp, "valid_vote"] = False
      
    return df_participant

  def keep_valid_votes(self, threshold):
    """
    Function for removing invalid watch survey responses
    
    Arguments
    ----------
      threshold :  int, Minimal required time between two watch survey responses 

    Returns
    -------
      df_output : Pandas dataframe, Dataframe with processed Cozie data
    """
    df_input = self.df

    # Initialize valid_vote column
    df_input["valid_vote"] = None

    # Apply keep_valid_votes for each participant
    df_output = df_input.groupby("id_participant", group_keys=False).apply(lambda x: self.keep_valid_votes_participant(df_participant=x, threshold=threshold))
 
    return df_output.copy()
  
  def save(self, output_file):
    """
    Function for saving Cozie dataframe to file
    
    Arguments
    ----------
      output_file : str, Path to text file with Cozie data or where Cozie data should be saved 

    Returns
    -------
      -
    """
    print("output_file:", output_file)
    self.df.to_parquet(output_file, compression='gzip')
    return