# BCG-heart-rate-detection

# BCG Heart Rate Detection

The primary goal of this project is to measure heart and respiratory rates using signals
acquired from a microbend fiber optic sensor. This sensor is placed under a subject's
mattress, approximately below their chest and stomach, to capture the mechanical activity
of the heart and respiratory movements.

## Project Workflow :

The project follows a structured approach to process Ballistocardiography (BCG) and
Reference (RR) data to ultimately compare heart rates derived from BCG signals against a
reference.

*1. Timestamp Standardization:*
- BCG Timestamps: Raw BCG timestamps are processed and converted to UTC format. The
convert_timestamp_format_BCG.py script handles this, calculating subsequent timestamps
based on an initial timestamp and a sampling frequency (e.g., 140 Hz).
- RR Timestamps: Timestamps from reference heart rate data (RR files) are also converted
to UTC format. This is handled by convert_timestamp_format_RR.py.
- The patient folders from 21 to 30 were not used due to absence of reference RR heart rate
files.
BCG:


### RR:

*2. Data Synchronization:*
- The timestamps from the BCG and RR datasets are unified and synchronized. This
crucial step ensures that data points from both sources correspond to the same moments in
time. The sync_BCG_RR_timestamps.py script appears to perform this, merging datasets
based on the nearest timestamps within a defined tolerance.
- The patients folders 6,13,20,32 were neglected due to the absence of any matching
sensors reading at the same time stamps.

*3. BCG Signal Resampling:*
- The BCG signal, originally sampled at a higher frequency (e.g., 140 Hz), is resampled to a
lower frequency (e.g., 50 Hz). This is a common preprocessing step to standardize the data
or reduce computational load. Scripts like resample_BCG.py or resressppple.py (likely a typo
for resample) are used for this, employing methods like Fourier-based interpolation.

*4. Signal Processing and Feature Extraction (primarily in main.py ):*
    - Data Loading: The main.py script iterates through patient data folders, loading CSV
       files containing BCG and RR data. and on processing a single, pre-processed
       (synchronized and resampled) CSV file.
    - Body Movement Detection: The detect_patterns function (from
       detect_body_movements.py ) is used to identify and potentially segment or handle
       periods of significant body movement in the BCG signal, as these can interfere with
       heart rate extraction.
    - Band-Pass Filtering: The raw BCG data is filtered to isolate specific frequency bands
       corresponding to BCG (heart activity) and respiratory signals. This is done by the
       band_pass_filtering function.


- Wavelet Transform: Maximal Overlap Discrete Wavelet Transform (MODWT) and its
    Multi-Resolution Analysis (MRA) are applied to the filtered BCG signal (movement
    component). This is handled by modwt (from modwt_matlab_fft.py ) and modwtmra
    (from modwt_mra_matlab_fft.py ). The 'bior3.9' wavelet is used, and a specific level
    (e.g., level 4) of the MRA decomposition ( dc[4] ) is selected as the wavelet_cycle for
    heart rate estimation.
- Heart Rate Estimation:
- In main.py , the heart_rate function is called to estimate beats per minute (BPM) from
    the wavelet_cycle.
- Reference Heart Rate Processing: The reference heart rates ( rr_heart_rates ) are read
from the input CSV.
- Resampling/Alignment for Comparison (in main.py ): To compare the BCG-derived heart
rates with the reference RR heart rates, the RR heart rates are resampled (or averaged
within windows) to match the length/timing of the BCG-derived heart rate array. This
ensures a fair comparison.
*5. Performance Evaluation and Analysis :*
- Metrics Calculation: Statistical metrics such as Mean Absolute Error (MAE), Root Mean
Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE) are calculated to


quantify the accuracy of the BCG-derived heart rate against the reference RR data for each
patient seperately.

- Statistical Summary: Minimum, maximum, and average heart rates are printed for both
BCG and reference signals, along with the absolute difference between their means.


- Data Logging: Key information, including patient ID, average RR heart rate, average BCG
heart rate, and the calculated error metrics, are appended to a dataInfo list, which is later
converted to a Pandas DataFrame and can be saved to a CSV file (e.g., patientinfo.csv ).
- Plotting: The create_analysis_plots function generates and saves:
- Correlation Plots: Scatter plots of reference heart rates vs. BCG heart rates, with a line of
best fit and Pearson correlation coefficient.
- Bland-Altman Plots: Plots showing the agreement between the two measurement
methods (BCG vs. Reference) by plotting the difference against the mean of the two heart
rates.
