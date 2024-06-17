# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split

# Load the CSV files
event_details_path = 'ufc_event_details.csv'
fight_results_path = 'ufc_fight_results.csv'
fight_stats_path = 'ufc_fight_stats.csv'

# create dataframes
event_details_df = pd.read_csv(event_details_path)
fight_results_df = pd.read_csv(fight_results_path)
fight_stats_df = pd.read_csv(fight_stats_path)

# convert 'event_date' to datetime format in the event details DataFrame
event_details_df['DATE'] = pd.to_datetime(event_details_df['DATE'])

# define a function to filter events based on a date range
def filter_events_by_date_range(df, start_date, end_date):
    mask = (df['DATE'] >= start_date) & (df['DATE'] <= end_date)
    return df.loc[mask]

# input date range for filtering
start_date = '2020-01-01'
end_date = '2022-12-31'

#filter the events based on the date range
filter_events_df = filter_events_by_date_range(event_details_df, start_date, end_date)
print('events in date range: ', filter_events_df)

# extract the event names
filtered_event_names = filter_events_df['EVENT'].tolist()
print('filtered_event_names: ', filtered_event_names)

# remove space after last word in event name in fight_results.csv
fight_results_df['EVENT'] = fight_results_df['EVENT'].str.strip()

# filter fight results and stats based on the filtered event names
filtered_fight_results_df = fight_results_df[fight_results_df['EVENT'].isin(filtered_event_names)]
filtered_fight_stats_df = fight_stats_df[fight_stats_df['EVENT'].isin(filtered_event_names)]
print(filtered_fight_results_df)
print(filtered_fight_stats_df)

# merge the filtered fight results and stats DataFrames on the relevant columns
merged_df = pd.merge(filtered_fight_results_df, filtered_fight_stats_df, on=['EVENT'])
print(merged_df)

# Split the merged DataFrame into training, validation, and test sets
train_df, temp_df = train_test_split(merged_df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

# Display the sizes of the datasets
print(f'Training set size: {len(train_df)}')
print(f'Validation set size: {len(val_df)}')
print(f'Test set size: {len(test_df)}')

# Save the datasets to new CSV files
train_df.to_csv('ufc_fight_stats_train.csv', index=False)
val_df.to_csv('ufc_fight_stats_val.csv', index=False)
test_df.to_csv('ufc_fight_stats_test.csv', index=False)

# Display a message indicating completion
print('Datasets created and saved successfully.')