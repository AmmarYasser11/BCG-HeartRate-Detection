import numpy as np
import pandas as pd
from scipy.signal import resample

def downsample_general(df, original_fs, new_fs, bcg_col='BCG', timestamp_col='Timestamp_x', hr_col='Heart Rate'):
        """
        Downsamples the BCG signal using Fourier-based interpolation.
        Works for arbitrary sampling rate ratios.
        """
        duration = len(df) / original_fs    # total time in seconds
        num_new_samples = int(duration * new_fs)

        # Resample BCG signal using Fourier method
        bcg_resampled = resample(df[bcg_col].values, num_new_samples)

        # Create time axes for interpolation
        time_original = np.linspace(0, duration, len(df))
        time_new = np.linspace(0, duration, num_new_samples)

        # Linearly interpolate timestamp and heart rate to match new time points
        timestamp_resampled = np.interp(time_new, time_original, df[timestamp_col].values)
   # convert timestamp_resampled to utc format 
        # timestamp_resampled_utc = pd.to_datetime(timestamp_resampled, unit='ms', utc=True)  # Convert to utc

        hr_resampled = np.interp(time_new, time_original, df[hr_col].values)

        # Create new DataFrame with downsampled values
        downsampled_df = pd.DataFrame({
                f'{bcg_col}_downsampled': bcg_resampled,
                # f'{timestamp_col}_downsampled': timestamp_resampled_utc,
                f'{timestamp_col}_downsampled': timestamp_resampled,
                f'{hr_col}_downsampled': hr_resampled
        })

        return downsampled_df

# --- Example usage ---
# input_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\synchronized_bcg_rr_data.csv"
# output_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\resampled_sync_bcg_rr_data.csv"
# input_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\07\synced\synchronized_bcg_rr_data.csv"
# output_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\07\synced\resampled_sync_bcg_rr_data.csv"
file_numbers = [f"{i:02d}" for i in range(31, 33) if i != 7]## + ["31", "32"]
# 6 and 13  20 32 no sync
# Loop through each folder number and create the corresponding input/output paths
for num in file_numbers:
#     user_input_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\BCG"
#     user_output_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}"
		input_file = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\synced\synchronized_bcg_rr_data.csv"
		output_file = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\synced\resampled_sync_bcg_rr_data.csv"
		original_fs = 140
		new_fs = 50     # Can now be any arbitrary value
    
    # Load data
		df = pd.read_csv(input_file)
    
    # Downsample
		downsampled_df = downsample_general(df, original_fs, new_fs)
    
    # Save to CSV
		downsampled_df.to_csv(output_file, index=False)








# import pandas as pd

# def downsample_pandas_resample(df, original_fs, new_fs, timestamp_col='Timestamp_x', bcg_col='BCG', hr_col='Heart Rate'):
#     """Downsamples using pandas resample, assuming timestamps can be converted to datetime."""
#     try:
#         # Convert timestamp column to datetime objects (adjusted to milliseconds)
#         df['datetime'] = pd.to_datetime(df[timestamp_col], unit='ms', origin='unix')
#         df = df.set_index('datetime')
#     except Exception as e:
#         raise ValueError(f"Could not convert timestamp column to datetime: {e}")

#     # Calculate the resampling period string (e.g., '20ms' if going from 100Hz to 50Hz)
#     resample_period = f'{1000 / new_fs}ms'  # Resampling interval in milliseconds

#     # Downsample using pandas' resample
#     downsampled_df = df.resample(resample_period).first()

#     # Reset index and rename columns
#     downsampled_df = downsampled_df.reset_index()
#     downsampled_df = downsampled_df.rename(columns={
#         bcg_col: f'{bcg_col}_downsampled',
#         timestamp_col: f'{timestamp_col}_downsampled',
#         hr_col: f'{hr_col}_downsampled',
#         'datetime': timestamp_col  # Rename back to original timestamp name
#     })

#     return downsampled_df

# # Example usage (adjust paths and column names as needed)
# input_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\synchronized_bcg_rr_data.csv"
# output_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\resampled_bcg_rr_data.csv"
# original_fs = 140  # Original sampling frequency in Hz
# new_fs = 50        # Desired sampling frequency in Hz

# # Load input data
# df = pd.read_csv(input_file)

# # Downsample
# downsampled_df = downsample_pandas_resample(df, original_fs, new_fs)

# # Save output
# downsampled_df.to_csv(output_file, index=False)










# import numpy as np
# import pandas as pd
# from scipy.signal import resample_poly

# def downsample_bcg_with_synchronized_hr_chunked(input_csv_path, output_csv_path, original_fs=140, new_fs=50, bcg_col='BCG', timestamp_col='Timestamp_x', hr_col='Heart Rate', chunk_size=1000):
#     """
#     Reads a CSV file, downsamples BCG, and finds corresponding HR (chunked to avoid memory issues).

#     Args:
#         input_csv_path (str): Path to the input CSV file.
#         output_csv_path (str): Path to save the output CSV file.
#         original_fs (int): Original sampling frequency (Hz).
#         new_fs (int): New sampling frequency (Hz).
#         bcg_col (str): Name of BCG column.
#         timestamp_col (str): Name of timestamp column (numerical).
#         hr_col (str): Name of heart rate column.
#         chunk_size (int): Number of downsampled timestamps to process at once.
#     """
#     try:
#         df = pd.read_csv(input_csv_path)
#         bcg_signal = df[bcg_col].values
#         original_timestamps = df[timestamp_col].values
#         heart_rate_original = df[hr_col].values

#         up = new_fs
#         down = original_fs
#         downsampled_bcg = resample_poly(bcg_signal, up, down)

#         start_time = original_timestamps[0]
#         num_original_samples = len(bcg_signal)
#         num_downsampled_samples = len(downsampled_bcg)
#         new_timestamps = np.linspace(start_time,
#                                      start_time + (num_original_samples - 1) / original_fs,
#                                      num_downsampled_samples)

#         downsampled_hr = np.empty(num_downsampled_samples)

#         for i in range(0, num_downsampled_samples, chunk_size):
#             end_index = min(i + chunk_size, num_downsampled_samples)
#             current_downsampled_ts = new_timestamps[i:end_index]
#             corresponding_hr_chunk = []
#             for ts in current_downsampled_ts:
#                 closest_index = np.argmin(np.abs(original_timestamps - ts))
#                 corresponding_hr_chunk.append(heart_rate_original[closest_index])
#             downsampled_hr[i:end_index] = np.array(corresponding_hr_chunk)

#         downsampled_df = pd.DataFrame({f'{bcg_col}_downsampled': downsampled_bcg,
#                                        f'{timestamp_col}_downsampled': new_timestamps,
#                                        f'{hr_col}_downsampled': downsampled_hr})

#         downsampled_df.to_csv(output_csv_path, index=False)

#         print(f"Downsampled data saved to: {output_csv_path}")
#         print("Original BCG signal length:", len(bcg_signal))
#         print("Downsampled BCG signal length:", len(downsampled_bcg))

#     except FileNotFoundError:
#         print(f"Error: Input CSV file not found at {input_csv_path}")
#     except KeyError as e:
#         print(f"Error: Column not found in the CSV file: {e}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage:
# input_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\synchronized_bcg_rr_data.csv"
# output_file = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced\resampled_bcg_rr_data.csv"

# downsample_bcg_with_synchronized_hr_chunked(input_file, output_file)