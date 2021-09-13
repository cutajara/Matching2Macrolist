# Fusion Matching File to DC Ascription Macrolist
# Anthony Cutajar
# Take Fusion MatchingFile and turn them into DC macrolists
# Script will always remove any p's from the file
# Edit the 'Option' parameter to allow the reading of late respondent log file (only needed for PP matching2 files)

# Imports required functions
import pandas as pd
import numpy as np

colnames=['m_donor']

##### PARAMETERS #####

# PARAMETER 1: number of recipient columns
# The number of recipient columns you need output in your macrolist 
recipientCols = 21

# PARAMETER 2: Matching File
# Read in Matching file
df = pd.read_csv(r'U:\Productn\I_A\2020 Single Source modules fusion\Matching Files\August 2021\Aug21_Module5_Matching1.txt', names=colnames, header = None)

# PARAMETER 3: Set Script Mode
# Select Option
# Option 1: No edits, turn matching file into macrolist (normal)
# Option 2: Read late respondents from log, remove as recipients and make donors (only needed for Matching2 Product Poll)
Option = 1

# PARAMETER 4: Late Log file. Only needed if using Option = 2
# Put in path and file to late respondent log if needed, else set Option = 1 above
logfile = r"V:\SurveyStore\Customised\Projects\AUS SS Online\2021\08 - Aug\PP Online\Fusion\Extra Respondents\Extra logs\Aug21_newMod3Mod5.txt"

##### PARAMETERS #####


# Option always on: Remove any p characters in the file
# Remove all p's
# Set file to list for p checking
list_df = list(df['m_donor'])
no_p = []
for i in list_df:
    i = i.replace('p','' )
    no_p.append(i)

df = pd.DataFrame({"m_donor" : no_p})

Info = "No Edits"

# Remove respondents from external log    

if Option == 2:
    with open(logfile, "r") as tf:
        lines = tf.read().split('\n')
    
    Info = "Log File Read"
    list_df_2 = list(df['m_donor'])
    
    Correct = []
    for i in list_df_2:
        for j in lines:
            i = i.replace(j,'0' )
        
        Correct.append(i)
    
    Correct.extend(lines)
    df = pd.DataFrame({"m_donor" : Correct})


#Trim empty spaces from the file
df= df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Splits out file by spaces
newdf = df["m_donor"].str.split(" ", expand = True)

# Give column names
# Replace 'Nones' with 0
# Check columns if less than needed
# Add extra columns 
# Output

# Create the column headers
filelen = list(newdf.columns)
OutputHeaders = colnames
for i in range(recipientCols):
    OutputHeaders.append('m_rec' + str(i+1))

# Make sure columns expected aren't less than columns in Matching File
if len(filelen)<=len(OutputHeaders):
    NeededCols = len(OutputHeaders) - len(filelen)
    i = 1
    listofzeros = [0] * newdf.shape[0]
    # Append Extra Blank columns if needed
    while i <= NeededCols:
        newdf['x_'+ str(i+1)]=listofzeros
        i=i+1
    
    
    newdf.columns= OutputHeaders
    # Fill in blank cells with zeros
    df_out = newdf.replace(np.nan, 0)
    # Save as .txt fie, tab delimited, can be read straight into DC
    df_out.to_csv(r'P:\Cutajara\Aug21_Mod5_Testing.txt', sep='\t', index = False, header=True)
    print("File Compete")
    print("Option %s used: %s" % (Option, Info))
else:
    # If there are more recipients in matching file than recipientCols variable update that variable to correct number
    print("Columns Requested are less than columns in Matching File. Script Failed, please update recipientCols variable")
