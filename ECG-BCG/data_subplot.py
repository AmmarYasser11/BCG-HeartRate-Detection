import matplotlib.pyplot as plt
import numpy as np



def bland_altman_plot(data1, data2, ax, *args, **kwargs):
    mean      = np.mean([data1, data2], axis=0)
    diff      = data1 - data2                   # Difference between data1 and data2
    md        = np.mean(diff)                   # Mean of the difference
    sd        = np.std(diff, axis=0)            # Standard deviation of the difference

    ax.scatter(mean, diff, *args, **kwargs)
    ax.axhline(md,           color='gray', linestyle='--')
    ax.axhline(md + 1.96*sd, color='gray', linestyle='--')
    ax.axhline(md - 1.96*sd, color='gray', linestyle='--')
    
    return ax

def pearson_correlation_plot(data1, data2,ax):   
    # plot the data
    ax.scatter(data1, data2)    
    # fits the best fitting line to the data
    ax.plot(np.unique(data1),
            np.poly1d(np.polyfit(data1, data2, 1))
            (np.unique(data1)), color='red')

    return ax

def box_plot(data1,data2,ax1, ax2):    
    # create another grouped boxplot 
    ax1 = ax1.boxplot(data1)
    ax2 = ax2.boxplot(data2)
    return ax1, ax2



def data_subplot(data_bcg, data_ecg, name ,show=True,):
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    ax1 = bland_altman_plot(data_bcg, data_ecg, ax1)
    #sm.graphics.mean_diff_plot(data_bcg, data_ecg, ax = ax1)
    plt.subplots_adjust(hspace=0.9)

    ax2 = pearson_correlation_plot(data_bcg, data_ecg, ax=ax2)
    plt.subplots_adjust(hspace=0.9)

    ax3, ax4 = box_plot(data_bcg, data_ecg, ax1=ax3, ax2=ax4)
    plt.subplots_adjust(hspace=0.9)

    plt.savefig(f'G:\spring 2025\data analytics\lastproject\ECG-BCG\results\{name}.png',dpi=500)
    
    if show == True:
        plt.show()
