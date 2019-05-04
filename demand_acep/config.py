# This file has the global configuration 
# so we do not have to repeat those in every function 

# This is for production environment
# The tests will define these paths separately
print("Config imported")
DATA_ROOT = "/gscratch/stf/demand_acep/Data"
METADATA_PATH = "/gscratch/stf/demand_acep/demand_acep/demand_acep/data/properties/"
METER_CHANNEL_FILE = METADATA_PATH + "Copy of Measured Channels PFRR.xlsx"
DATA_YEARS_FILE = METADATA_PATH + "data_years.txt"