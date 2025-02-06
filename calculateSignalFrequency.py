from PySide6.QtWidgets import QApplication, QMessageBox, QFileDialog
import numpy as np
import pandas as pd

def browseFile():
        filePath, _ = QFileDialog.getOpenFileName(None, "Select a CSV file", "", "CSV Files (*.csv);;All Files (*)")
        
        if filePath:
            try:
                df = pd.read_csv(filePath, header=None)

                browsedSignal = df.iloc[0].values  # Get the first row as signal
                signalFreq = calculateFrequency(browsedSignal, max(np.abs(browsedSignal)) - 0.3)
                print(signalFreq)
                
            except Exception as e:
                QMessageBox.critical(None, "Error", f"Failed to read CSV: {str(e)}")

def calculateFrequency(signal, threshold):
        peaks = []
        for i in range(len(signal)):
            if i > 0 and i < len(signal) - 1:
                if signal[i] > signal[i - 1] and signal[i] > signal[i + 1] and signal[i] > threshold:
                    peaks.append(i)
        currSignalTime = np.linspace(0, 1, len(signal))
        cycleTimes = []
        for i in range(len(peaks) - 1, 0, -1):
            cycleTimes.append(currSignalTime[peaks[i]] - currSignalTime[peaks[i - 1]])
        
        periodicTime = np.average(cycleTimes)
        return round(1 / periodicTime)

# Run a Qt application loop if this is a standalone script
if __name__ == "__main__":
    app = QApplication([])  # Create QApplication instance before any widget
    browseFile()  # Start the file browsing
    app.exec()  # Start the event loop
