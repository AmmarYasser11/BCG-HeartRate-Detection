import pandas as pd
from datetime import datetime, timezone, timedelta
import math
import os
import glob

def convert_to_utc_format(timestamp_val):
    """
    Converts a Unix epoch timestamp in milliseconds
    to a UTC string in the format 'YYYY-MM-DD HH:MM:SS.ssssss+00:00'.

    Handles potential NaN or None values.
    This version is simplified as it expects numeric millisecond input
    when called after the timestamp generation step.
    The original more general version could be kept if direct conversion
    from various formats is still needed elsewhere.
    """
    if pd.isna(timestamp_val):
        return None
    if isinstance(timestamp_val, float) and math.isnan(timestamp_val):
        return None

    try:
        # Expecting timestamp_val to be Unix epoch in milliseconds (numeric)
        if isinstance(timestamp_val, (int, float)):
            timestamp_seconds_exact = timestamp_val / 1000.0
            # Create a datetime object in UTC
            dt_object = datetime.fromtimestamp(timestamp_seconds_exact, tz=timezone.utc)
            # Format to the desired string format (ensure 6 decimal places for microseconds)
            return dt_object.strftime('%Y-%m-%d %H:%M:%S.%f') + "+00:00"
        else:
            # This case should ideally not be hit if called after timestamp generation
            return f"Error: Expected numeric ms timestamp, got {type(timestamp_val)}"
    except OverflowError:
        return f"Error: Timestamp value out of range for conversion: {timestamp_val}"
    except Exception as e:
        return f"Error converting timestamp {timestamp_val}: {e}"

def process_csv_folder(input_folder_path, output_folder_path, timestamp_column_name='Timestamp', sampling_frequency=140.0):
    """
    Reads all CSV files from an input folder. For each file:
    1. Determines a starting timestamp from the first entry in 'timestamp_column_name'.
    2. Recalculates all entries in 'timestamp_column_name' to increment from the
       start time by 1/sampling_frequency seconds. These will be Unix ms.
    3. Converts these millisecond timestamps to UTC string format in a new column.
    Saves the modified files to an output folder.
    """
    if not os.path.isdir(input_folder_path):
        print(f"Error: Input folder '{input_folder_path}' not found.")
        return

    os.makedirs(output_folder_path, exist_ok=True)
    print(f"Output will be saved to: {output_folder_path}")

    csv_files = glob.glob(os.path.join(input_folder_path, "*.csv"))

    if not csv_files:
        print(f"No CSV files found in '{input_folder_path}'.")
        return

    time_increment_ms = (1.0 / sampling_frequency) * 1000.0

    for csv_file_path in csv_files:
        base_filename = os.path.basename(csv_file_path)
        output_file_path = os.path.join(output_folder_path, base_filename)
        print(f"\nProcessing file: {csv_file_path}...")

        try:
            df = pd.read_csv(csv_file_path)

            if timestamp_column_name not in df.columns:
                print(f"  Warning: Timestamp column '{timestamp_column_name}' not found in '{base_filename}'. Skipping file.")
                continue

            if df.empty:
                print(f"  Warning: CSV file '{base_filename}' is empty. Skipping file.")
                df.to_csv(output_file_path, index=False) # Save empty file as is
                continue

            start_timestamp_val = df[timestamp_column_name].iloc[0]
            initial_timestamp_ms_utc = None

            if pd.isna(start_timestamp_val):
                print(f"  Error: Starting timestamp (first row) in '{timestamp_column_name}' is missing in '{base_filename}'. Skipping file.")
                continue

            try:
                if isinstance(start_timestamp_val, (int, float)):
                    if math.isnan(start_timestamp_val):
                        raise ValueError("Starting timestamp is NaN")
                    initial_timestamp_ms_utc = float(start_timestamp_val) # Assume it's already UTC ms
                elif isinstance(start_timestamp_val, str):
                    # Try parsing common "MM/DD/YYYY HH:MM:SS AM/PM"
                    # If your string format is different, this part needs adjustment
                    naive_dt = datetime.strptime(start_timestamp_val, "%m/%d/%Y %I:%M:%S %p")
                    # IMPORTANT ASSUMPTION: Parsed string datetime is in local timezone
                    local_dt = naive_dt.astimezone(None)
                    utc_dt = local_dt.astimezone(timezone.utc)
                    initial_timestamp_ms_utc = utc_dt.timestamp() * 1000.0
                else:
                    raise TypeError(f"Unsupported type for starting timestamp: {type(start_timestamp_val)}")
            except (ValueError, TypeError) as e:
                print(f"  Error: Could not parse starting timestamp '{start_timestamp_val}' in '{base_filename}': {e}. Skipping.")
                continue

            # Generate new timestamps in milliseconds
            calculated_timestamps_ms = []
            for i in range(len(df)):
                calculated_timestamps_ms.append(initial_timestamp_ms_utc + (i * time_increment_ms))

            # Overwrite the original timestamp column with the new millisecond values
            df[timestamp_column_name] = calculated_timestamps_ms

            # Convert the new millisecond timestamps to UTC string format in a new column
            converted_column_name = f"{timestamp_column_name}_UTC"
            df[converted_column_name] = df[timestamp_column_name].apply(convert_to_utc_format)

            df.to_csv(output_file_path, index=False)
            print(f"  Successfully processed. Converted file saved to: {output_file_path}")

        except FileNotFoundError:
            print(f"  Error: File '{csv_file_path}' not found during processing.")
        except pd.errors.EmptyDataError: # Should be caught by df.empty check, but good to have
            print(f"  Warning: File '{csv_file_path}' is empty. Skipping.")
        except Exception as e:
            print(f"  Error processing file '{csv_file_path}': {e}")


# --- How to use the function ---

# 1. Create dummy files and folders for a quick test (optional)
def setup_dummy_test_environment(base_dir="test_timestamp_increment_conversion"):
    input_dir = os.path.join(base_dir, "input_csvs")
    output_dir = os.path.join(base_dir, "output_csvs_incremented")
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Data where the first timestamp is Unix ms
    data1 = {
        'RecordID': [1, 2, 3, 4, 5],
        'Timestamp': [1699451083498, "ignored", "also ignored", None, 123], # Only first value is used for start
        'Value': ['A', 'B', 'C', 'D', 'E']
    }
    df1 = pd.DataFrame(data1)
    df1.to_csv(os.path.join(input_dir, "bcg_data_unix_start.csv"), index=False)

    # Data where the first timestamp is a string
    data2 = {
        'EventID': ['E1', 'E2', 'E3'],
        'Timestamp': ["11/03/2023 10:30:00 PM", 1699020000000.0, "invalid_date"], # Only first value
        'Details': ['X', 'Y', 'Z']
    }
    df2 = pd.DataFrame(data2)
    df2.to_csv(os.path.join(input_dir, "rr_data_string_start.csv"), index=False)

    # Data with a different timestamp column name
    data3 = {
        'LogID': [101, 102, 103, 104],
        'TimeOfEvent': [1699500000000, "11/05/2023 05:30:00 AM", None, 0],
        'Message': ['Msg1', 'Msg2', 'Msg3', 'Msg4']
    }
    df3 = pd.DataFrame(data3)
    df3.to_csv(os.path.join(input_dir, "log_data_custom_ts_col.csv"), index=False)

    # Empty file
    df_empty = pd.DataFrame()
    df_empty.to_csv(os.path.join(input_dir, "empty_data.csv"), index=False)

    # File with missing first timestamp
    data_missing_start = {
        'RecordID': [1,2],
        'Timestamp': [None, 1699451083498],
        'Value': ['A', 'B']
    }
    df_missing = pd.DataFrame(data_missing_start)
    df_missing.to_csv(os.path.join(input_dir, "missing_start_timestamp.csv"), index=False)


    print(f"Dummy test environment created in folder: '{base_dir}'")
    return input_dir, output_dir

# --- Option 1: Run with dummy data for testing ---
# print("--- Running with DUMMY data for testing ---")
# dummy_base_dir = "timestamp_increment_test_area"
# test_input_folder, test_output_folder = setup_dummy_test_environment(dummy_base_dir)
#
# print("\nProcessing dummy files with 'Timestamp' column (fs=140):")
# process_csv_folder(test_input_folder, test_output_folder, timestamp_column_name='Timestamp', sampling_frequency=140.0)
#
# print("\nProcessing dummy log_data.csv with 'TimeOfEvent' column (fs=10):") # Example with different fs
# process_csv_folder(test_input_folder, os.path.join(test_output_folder, "log_specific"), timestamp_column_name='TimeOfEvent', sampling_frequency=10.0)
# print("--- Dummy data processing finished ---")


# --- Option 2: Run with YOUR specified folders and parameters ---
# Ensure the paths below are correct for your system.
# The input_folder should contain the CSVs (e.g., the 'BCG' subfolder).
# The output_folder is where the converted files will be saved. 21,22,23,24,25,26,27,28,29,30,7,1

print("\n--- Running with USER-SPECIFIED data ---")
# user_input_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02\BCG"
# user_output_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02"
# # Outputting to the parent folder of 'BCG', as in your example
# Default timestamp column name is 'Timestamp' and sampling frequency is 140.0
# If your column is named differently or fs varies per file type, adjust the call.

file_numbers = [f"{i:02d}" for i in range(14, 21) if i != 7] + ["31", "32"]

# Loop through each folder number and create the corresponding input/output paths
for num in file_numbers:
    user_input_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\BCG"
    user_output_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}"
    
    print(f"Processing folder number: {num}")
    process_csv_folder(
    input_folder_path=user_input_folder,
    output_folder_path=user_output_folder,
    timestamp_column_name='Timestamp', # Adjust if your main timestamp column has a different name
    sampling_frequency=140.0
)



    print(f"\n--- User-specified data processing finished. Check the output folder. {num}---")