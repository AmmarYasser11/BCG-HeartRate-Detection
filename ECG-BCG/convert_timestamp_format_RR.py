# import pandas as pd
# from datetime import datetime, timedelta, timezone
# print("before")
# # Load the CSV file
# df = pd.read_csv(r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\BCG\01_20231104_BCG.csv")

# print("after")
# # Convert first timestamp from ms to a timezone-aware datetime
# start_time_ms = float(df['Timestamp'].iloc[0])
# start_time = datetime.fromtimestamp(start_time_ms / 1000, tz=timezone.utc)

# # Sampling frequency (assume constant)
# sampling_frequency = float(df['fs'].iloc[0])
# time_step = timedelta(seconds=1 / sampling_frequency)

# # Generate full timestamp column
# df['Timestamp'] = [start_time + i * time_step for i in range(len(df))]

# # Save to CSV
# df.to_csv(r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\BCG\aaa.csv", index=False)
# print("finish")

# import pandas as pd

# # Load RR data
# rr_df = pd.read_csv(r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\Reference\RR\01_20231105_RR.csv")

# # Convert to UTC-aware datetime (assume original timestamps were in UTC)
# rr_df['Timestamp'] = pd.to_datetime(rr_df['Timestamp'].str.strip(), utc=True)
# # Save a new CSV with the parsed UTC timestamps
# rr_df.to_csv(r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\R5_converted_UTC.csv", index=False)



#import pandas as pd

# Load RR data
#rr_df = pd.read_csv(r"G:\spring 2025\data analytics\project\dataset\dataset\data\01\Reference\RR\01_20231105_RR.csv")

# Convert to UTC-aware datetime (assume original timestamps were in UTC)
#rr_df['Timestamp'] = pd.to_datetime(rr_df['Timestamp'].str.strip(), utc=True)
# Save a new CSV with the parsed UTC timestamps
#rr_df.to_csv("R5_converted_UTC.csv", index=False)
# import pandas as pd
# import os

# === Set input and output folder paths ===
# input_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\Reference\RR"
# output_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01"
# input_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02\Reference\RR"
# output_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02"

# file_numbers = [f"{i:02d}" for i in range(2, 21) if i != 7] + ["31", "32"]

# # Loop through each folder number and create the corresponding input/output paths
# for num in file_numbers:
#     input_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\Reference\RR"
#     output_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}"

# # Ensure the output folder exists
#     os.makedirs(output_folder, exist_ok=True)

#     # Loop through all files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".csv"):
#             file_path = os.path.join(input_folder, filename)

#             # Load the CSV file
#             rr_df = pd.read_csv(file_path)

#             # Convert 'Timestamp' to UTC-aware datetime
#             rr_df['Timestamp'] = pd.to_datetime(rr_df['Timestamp'].str.strip(), utc=True)

#             # Save to output folder with the same filename
#             # output_folder = os.path.join(output_folder, f"converted_{filename}")
#             rr_df.to_csv(output_folder, index=False)

#             print(f"Processed: {filename} -> converted_{filename}")







# input_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02\Reference\RR"
# output_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\02"






# os.makedirs(output_folder, exist_ok=True)

#     # Loop through all files in the input folder
# for filename in os.listdir(input_folder):
#     if filename.endswith(".csv"):
#         file_path = os.path.join(input_folder, filename)

#             # Load the CSV file
#         rr_df = pd.read_csv(file_path)

#             # Convert 'Timestamp' to UTC-aware datetime
#         rr_df['Timestamp'] = pd.to_datetime(rr_df['Timestamp'].str.strip(), utc=True)

#             # Save to output folder with the same filename
#             # output_folder = os.path.join(output_folder, f"converted_{filename}")
#         rr_df.to_csv(output_folder, index=False)

#         print(f"Processed: {filename} -> converted_{filename}")


import os
import pandas as pd

file_numbers = [f"{i:02d}" for i in range(2, 21) if i != 7] + ["31", "32"]

# Loop through each folder number and create the corresponding input/output paths
for num in file_numbers:
    input_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\Reference\RR"
    output_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}\Reference\RR_converted"

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)

            # Load the CSV file
            rr_df = pd.read_csv(file_path)

            # Convert 'Timestamp' to UTC-aware datetime
            rr_df['Timestamp'] = pd.to_datetime(rr_df['Timestamp'].str.strip(), utc=True)

            # Construct full output file path
            output_file_path = os.path.join(output_folder, f"converted_{filename}")
            rr_df.to_csv(output_file_path, index=False)

            print(f"Processed: {filename} -> converted_{filename}")
