import math
import os
import glob
import warnings

import matplotlib.pyplot as plt
from scipy import stats

import numpy as np
import pandas as pd
from detect_body_movements import detect_patterns

from heart_rate import heart_rate
from modwt_matlab_fft import modwt
from band_pass_filtering import band_pass_filtering

from modwt_mra_matlab_fft import modwtmra

from data_subplot import data_subplot
from scipy.signal import resample
from sklearn.metrics import mean_absolute_error , mean_absolute_percentage_error , mean_squared_error, root_mean_squared_error
#from stats import *
# ======================================================================================================================
warnings.simplefilter("ignore")
# Main program starts here
print('\nstart processing ...')
# ======================================================================================================================

# Add this function before your main processing loop

def create_analysis_plots(rr_rates, bcg_rates, patient_id, folder_path):
    """Create correlation and Bland-Altman plots for each patient"""
    
    # Create plots directory in patient folder
    plots_dir = os.path.join(folder_path, 'analysis_plots')
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    # Correlation Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(rr_rates, bcg_rates, alpha=0.5)
    z = np.polyfit(rr_rates, bcg_rates, 1)
    p = np.poly1d(z)
    plt.plot(rr_rates, p(rr_rates), "r--", alpha=0.8)
    correlation = stats.pearsonr(rr_rates, bcg_rates)[0]
    
    plt.title(f'Correlation Plot (r={correlation:.2f})\nPatient {patient_id}')
    plt.xlabel('Reference Heart Rates (bpm)')
    plt.ylabel('BCG Heart Rates (bpm)')
    plt.grid(True)
    correlation_plot_path = os.path.join(plots_dir, f'correlation_patient_{patient_id}.png')
    plt.savefig(correlation_plot_path)
    plt.close()

    # Bland-Altman Plot
    mean_hrs = (rr_rates + bcg_rates) / 2
    diff_hrs = bcg_rates - rr_rates
    mean_diff = np.mean(diff_hrs)
    std_diff = np.std(diff_hrs)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(mean_hrs, diff_hrs, alpha=0.5)
    plt.axhline(y=mean_diff, color='r', linestyle='--', label='Mean difference')
    plt.axhline(y=mean_diff + 1.96*std_diff, color='g', linestyle='--', label='+1.96 SD')
    plt.axhline(y=mean_diff - 1.96*std_diff, color='g', linestyle='--', label='-1.96 SD')
    
    plt.title(f'Bland-Altman Plot\nPatient {patient_id}')
    plt.xlabel('Mean of Reference and BCG Heart Rates (bpm)')
    plt.ylabel('Difference (BCG - Reference) (bpm)')
    plt.legend()
    plt.grid(True)
    bland_altman_path = os.path.join(plots_dir, f'bland_altman_patient_{patient_id}.png')
    plt.savefig(bland_altman_path)
    plt.close()




  
root_dir = r"G:\spring 2025\data analytics\project\dataset\dataset\data"

# Prepare the output structure
dataInfo = [["PatientID", "RR AVG", "AVG BCG", "MAE", "RMSE", "MAPE"]]

# Walk through each sub-folder
for folder_name in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder_name)
    
    # Make sure it's a directory
    if os.path.isdir(folder_path):
        # Look for CSV files inside this subfolder
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        
        for csv_file in csv_files:
            if csv_file.endswith(".csv") and os.stat(csv_file).st_size != 0:
                # Extract patient ID (number from folder name like "X123")
                patient_id = ''.join(filter(str.isdigit, folder_name))


                rawData = pd.read_csv(csv_file, sep=None, header=None, skiprows=1, engine="python").values
                start_point, end_point, window_shift = 0, 500, 500 # Constants
            # ==========================================================================================================
            
            # BCG Processing
            utc_time = rawData[:, 1]
            data_stream_bcg = rawData[:, 0] # Read BCG data
            rr_heart_rates = rawData[:, 2]
            
            # ==========================================================================================================
           
            data_stream_bcg, utc_time = detect_patterns(start_point, end_point, window_shift, data_stream_bcg, utc_time, plot=1)
        # ==========================================================================================================
        # BCG signal extraction
            movement = band_pass_filtering(data_stream_bcg, 50, "bcg")

            # ==========================================================================================================
            #Wavelet transformation
            w = modwt(movement, 'bior3.9', 4)
            dc = modwtmra(w, 'bior3.9')
            wavelet_cycle = dc[4]
            # ==========================================================================================================
            # Vital Signs estimation - (10 seconds window is an optimal size for vital signs measurement)
            limit = int(math.floor(data_stream_bcg.size / window_shift))
            # ==========================================================================================================
            # Heart Rate of BCG
            bcg_bpm= heart_rate(start_point, end_point, window_shift, limit, wavelet_cycle, mpd=1, sig_type="bcg", plot=0)
            
            min_bcg = np.around(np.min(bcg_bpm))
            max_bcg = np.around(np.max(bcg_bpm))
            avg_bcg = np.around(np.mean(bcg_bpm))

            # Replace the resampling code with:
            window_size = len(rr_heart_rates) // len(bcg_bpm)
            rr_heart_rates_resampled = np.array([
                np.mean(rr_heart_rates[i:i+window_size]) 
                for i in range(0, len(rr_heart_rates)-window_size+1, window_size)
            ])

            # Ensure both arrays have the same length
            min_length = min(len(rr_heart_rates_resampled), len(bcg_bpm))
            rr_heart_rates_resampled = rr_heart_rates_resampled[:min_length]
            bcg_bpm = bcg_bpm[:min_length]

            # Now calculate the metrics
            mae = mean_absolute_error(rr_heart_rates_resampled, bcg_bpm)
            rmse = root_mean_squared_error(rr_heart_rates_resampled, bcg_bpm)
            mape = mean_absolute_percentage_error(rr_heart_rates_resampled, bcg_bpm)

            print('\nHeart Rate Information:')
            print("==========================================================================================================\n")
            
            print("Mean absolute error: ", mae)
            print("==========================================================================================================")
            print("Root mean square error: ", rmse)
            print("==========================================================================================================")
            print("Mean absolute percentage error: ", mape)
            print("==========================================================================================================")
            print("==========================================================================================================")
            # ==========================================================================================================
            # Write data
            dataInfo.append([patient_id,rr_heart_rates_resampled,avg_bcg,mae,rmse,mape])
            

            
        
        # RR file heart rate
            rr_hr_stats = {
            'min': np.around(np.min(rr_heart_rates_resampled)),
            'max': np.around(np.max(rr_heart_rates_resampled)),
            'mean': np.around(np.mean(rr_heart_rates_resampled))
        }
        
        # Print statistics
            print('\nBCG Heart Rate Information')
            print('Minimum pulse : ', min_bcg)
            print('Maximum pulse : ', max_bcg)
            print('Average pulse : ', avg_bcg)
        
            print('\nReference Heart Rate Information')
            print('Minimum pulse : ', rr_hr_stats['min'])
            print('Maximum pulse : ', rr_hr_stats['max'])
            print('Average pulse : ', rr_hr_stats['mean'])
        
        # Calculate heart rate difference
            hr_diff = np.abs(avg_bcg - rr_hr_stats['mean'])
            print('\nHeart Rate Difference (BCG vs Reference):', hr_diff)

            # Create analysis plots
            create_analysis_plots(rr_heart_rates_resampled, bcg_bpm, patient_id, folder_path)












dataInfo = pd.DataFrame(dataInfo)
#dataInfo.to_csv("./results/patientinfo.csv", header=False)
# ======================================================================================================================

print('\nEnd processing ...')
