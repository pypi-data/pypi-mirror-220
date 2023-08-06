#import os, sys
#sys.path.insert(0, '..')

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from coziepy import Cozie


#from cozie import Cozie
#from cozie import CoziePlot
# Test test

def test_answer():

    print("test_answer")
    cozie = Cozie()
    assert "asdf7" == cozie.test()

cozie = Cozie()
cozie.test()

#df = cozie.load(log_file = 'examples/cozie_angatest01_anga_logs.txt',
#                timezone = "Asia/Singapore",
#                output_file = 'anga.parquet.gizp')

# Filter data for valid votes
#cozie = Cozie()
#df = cozie.load(input_file="orenth.parquet.gizp")


# Load data from web API
df = cozie.load(id_experiment = "leth",
                participant_list = ["leth01", "leth03"],
                timezone = "Asia/Singapore",
                api_url="https://m7cy76lxmi.execute-api.ap-southeast-1.amazonaws.com/default/cozie-apple-researcher-read-influx", 
                api_key="3gEAa10VPY6xnJHw8Rsyn6vVjwKwVdyr15Oae6hS")
df.head()


df2 = cozie.keep_valid_votes(threshold=55)
print(df.ws_survey_count.count())
print(df2.ws_survey_count.count())