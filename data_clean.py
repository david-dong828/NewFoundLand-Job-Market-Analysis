# Name: Dong Han
# Student ID: 202111878
# Mail: dongh@mun.ca

import re
import pandas as pd

############################################# CLEAN DATA #############################################
## Clean Data: Combine 2 seperated scraped data files; Correct some data from in wrong places; Remove uncompleted rows
# Function to convert the 'Date Posted' text to numeric
def convert_date_posted(text):
    text = str(text)
    if '30+' in text:
        return 30
    # Use regex to find the number of days; if "day" is found without a number, assume 1
    day_match = re.search(r'(\d+)\s+day', text)
    if day_match:
        return int(day_match.group(1))
    if 'day' in text:
        return 1
    return pd.NaT  # Not a Time for non-matching text

# Function to move job type data from 'Salary' to 'Job Type'
def move_job_type(row):
    job_types = ['Full-time', 'Part-time', 'Permanent','Temporary']
    for job_type in job_types:
        text = str(row['Salary'])
        if job_type in text:
            # Update JobType column
            row['Job Type'] = job_type
            # Clean up 'Salary' column by removing job type data
            row['Salary'] = row['Salary'].replace(job_type, '').strip(', ')
    return row

### Save a file named "cleaned_xxx_jobs.csv"
def data_clean(dataPath1,dataPath2):
    df1 = pd.read_csv(dataPath1)
    df2 = pd.read_csv(dataPath2)

    # Merge dataframes since they have the same columns
    combined_df = pd.concat([df1, df2], ignore_index=True)

    # Drop rows where the 'Title' is empty or contains only whitespace
    combined_df['Title'] = combined_df['Title'].astype(str)
    combined_df = combined_df[combined_df['Title'].str.strip().astype(bool)]
    # Drop rows where the 'Title' column is 'N/A' or 'nan' (if these values are present)
    combined_df = combined_df[~combined_df['Title'].isin(['N/A', 'nan'])]

    # Move Job Type data from Salary to Job Type column
    combined_df = combined_df.apply(move_job_type, axis=1)

    # Convert Salary to numeric, replace non-numeric with 'N/A'
    combined_df['Salary'] = pd.to_numeric(combined_df['Salary'].str.extract(r'(\d+\.?\d*)')[0],errors='coerce')
    combined_df['Salary'].fillna('N/A', inplace=True)

    # Convert 'Date Posted' to numeric days
    combined_df['Date Posted'] = combined_df['Date Posted'].apply(convert_date_posted)

    # Save the cleaned dataframe
    combined_df.to_csv('cleaned_xxx_jobs.csv', index=False)
    print(combined_df)
    print('Data cleaned !')

#############################################    MAIN    #############################################
def main():

    # Clean Data
    dataPath1 = "xxx.csv"
    dataPath2 = "xx.csv"
    data_clean(dataPath1, dataPath2)

if __name__ == '__main__':
    main()
