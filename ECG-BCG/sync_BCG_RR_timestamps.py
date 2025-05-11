import pandas as pd
import glob
import os

def process_bcg_files(bcg_path):
    """Read and combine all BCG files"""
    bcg_files = glob.glob(os.path.join(bcg_path, "*BCG.csv"))
    bcg_dfs = []
    
    for file in bcg_files:
        df = pd.read_csv(file)
        # Ensure Timestamp_UTC column exists and convert to UTC
        if 'Timestamp_UTC' in df.columns:
            df['Timestamp_UTC'] = pd.to_datetime(df['Timestamp_UTC']).dt.tz_localize(None)
            bcg_dfs.append(df)
            
    return pd.concat(bcg_dfs, ignore_index=True) if bcg_dfs else None

def process_rr_files(rr_path):
    """Read and combine all RR files"""
    rr_files = glob.glob(os.path.join(rr_path, "*RR.csv"))
    rr_dfs = []
    
    for file in rr_files:
        df = pd.read_csv(file)
        if 'Timestamp' in df.columns:
            # Convert to datetime and ensure it's timezone-naive
            df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.tz_localize(None)
            rr_dfs.append(df)
            
    return pd.concat(rr_dfs, ignore_index=True) if rr_dfs else None

def sync_bcg_rr_data(base_folder, output_path):
    """Main function to sync BCG and RR data"""
    # Define paths 
    bcg_path = base_folder
    rr_path = os.path.join(base_folder, "Reference", "RR")
    
    # Process BCG files
    bcg_df = process_bcg_files(bcg_path)
    if bcg_df is None:
        print("No BCG files found or processed")
        return
    
    # Process RR files
    rr_df = process_rr_files(rr_path)
    if rr_df is None:
        print("No RR files found or processed")
        return
    
    # Sort dataframes by timestamp
    bcg_df = bcg_df.sort_values('Timestamp_UTC')
    rr_df = rr_df.sort_values('Timestamp')
    
    # Merge using merge_asof to find nearest timestamps
    merged_df = pd.merge_asof(
        bcg_df,
        rr_df,
        left_on='Timestamp_UTC',
        right_on='Timestamp',
        direction='nearest',
        tolerance=pd.Timedelta(milliseconds=300)
    )
    
    # Remove rows where there was no match within tolerance
    merged_df = merged_df.dropna(subset=['Heart Rate', 'RR Interval in seconds'])
    
    # Save the synchronized data
    output_file = os.path.join(output_path, "synchronized_bcg_rr_data.csv")
    merged_df.to_csv(output_file, index=False)
    print(f"Synchronized data saved to: {output_file}")
    
    # Print summary statistics
    print(f"\nSummary:")
    print(f"Total BCG records processed: {len(bcg_df)}")
    print(f"Total RR records processed: {len(rr_df)}")
    print(f"Total synchronized records: {len(merged_df)}")

# Usage
# base_folder = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01"
# output_path = r"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\01\synced"


file_numbers = [f"{i:02d}" for i in range(2, 21) if i != 7] + ["31", "32"]

# Loop through each folder number and create the corresponding input/output paths
for num in file_numbers:
    base_folder = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}"
    output_path = rf"D:\oneDrive\Desktop\BCG-Heart rate-detection\dataset\data\{num}"

# Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

# Run the synchronization
    sync_bcg_rr_data(base_folder, output_path)