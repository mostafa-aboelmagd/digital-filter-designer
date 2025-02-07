import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from typing import Optional, Tuple, Union


"""     self.lib_combobox.setItemText(0,"butterworth")
        self.lib_combobox.setItemText(1,"chebyshev1")
        self.lib_combobox.setItemText(2,"chebyshev2")
        self.lib_combobox.setItemText(3,"bessel")
        self.lib_combobox.setItemText(4,"elliptic")
        self.lib_combobox.setItemText(5,"fir")
        self.lib_combobox.setItemText(6,"gaussian")
        self.lib_combobox.setItemText(7,"median")
        self.lib_combobox.setItemText(8,"Savitzky-Golay")
        self.lib_combobox.setItemText(9,"kalman")
    
"""

"""
    self.type_combobox.setItemText(0,"lowpass")
    self.type_combobox.setItemText(1,"highpass")
    self.type_combobox.setItemText(2,"bandpass")
"""
class FilterDesigner:
    @staticmethod
    def design_iir(
        family: str,
        ftype: str,
        order: int,
        cutoff: Union[float, Tuple[float, float]],
        fs: float = 1.0,
        rp: Optional[float] = None,
        rs: Optional[float] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        design_methods = {
            'butterworth': signal.butter,
            'chebyshev1': signal.cheby1,
            'chebyshev2': signal.cheby2,
            'bessel': signal.bessel,
            'elliptic': signal.ellip
        }
        
        kwargs = {}
        if family in {'chebyshev1', 'elliptic'}:
            kwargs['rp'] = rp
        if family in {'chebyshev2', 'elliptic'}:
            kwargs['rs'] = rs
            
        return design_methods[family](order, cutoff, btype=ftype, fs=fs, **kwargs)

    @staticmethod
    def design_fir(
        ftype: str,
        numtaps: int,
        cutoff: Union[float, Tuple[float, float]],
        fs: float = 1.0,
        window: str = 'hamming'
    ) -> Tuple[np.ndarray, float]:
        pass_zero = {'lowpass': True, 'highpass': False, 'bandpass': False}.get(ftype, True)
        coeffs = signal.firwin(numtaps, cutoff, window=window, pass_zero=pass_zero, fs=fs)
        return coeffs, 1.0

    @staticmethod
    def design_gaussian(
        numtaps: int,
        cutoff: float,
        fs: float = 1.0
    ) -> Tuple[np.ndarray, float]:
        sigma = (np.sqrt(np.log(2)) / (2 * np.pi * cutoff)) * fs
        window = signal.windows.gaussian(numtaps, sigma, sym=True)
        return window / window.sum(), 1.0

class FilterApplier:
    @staticmethod
    def apply_iir_fir(
        b: np.ndarray,
        a: Union[np.ndarray, float],
        input_signal: np.ndarray,
        zero_phase: bool = False
    ) -> np.ndarray:
        # If zero_phase is True, use filtfilt (forward-backward for zero phase shift)
        # otherwise apply a one-pass filter with lfilter.
        return signal.filtfilt(b, a, input_signal) if zero_phase else signal.lfilter(b, a, input_signal)

    @staticmethod
    def apply_median( #median filter
        input_signal: np.ndarray,
        kernel_size: int
    ) -> np.ndarray:
        return signal.medfilt(input_signal, kernel_size=kernel_size)

    @staticmethod
    def apply_savgol( #Savitzky-Golay filter
        input_signal: np.ndarray,
        window_length: int,
        polyorder: int
    ) -> np.ndarray:
        return signal.savgol_filter(input_signal, window_length, polyorder)

class KalmanFilter1D:
    __slots__ = ('state', 'covariance', 'process_noise', 'measurement_noise')
    
    def __init__(
        self,
        initial_state: float,
        initial_covariance: float,
        process_noise: float,
        measurement_noise: float
    ):
        self.state = initial_state
        self.covariance = initial_covariance
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

    def update(self, measurement: float) -> None:
        K = self.covariance / (self.covariance + self.measurement_noise)
        self.state += K * (measurement - self.state)
        self.covariance *= (1 - K)

    def predict(self) -> None:
        self.covariance += self.process_noise

    def filter(self, measurements: np.ndarray) -> np.ndarray:
        filtered = np.empty_like(measurements)
        for i, z in enumerate(measurements):
            self.predict()
            self.update(z)
            filtered[i] = self.state
        return filtered

def plot_response(
    b: np.ndarray,
    a: Union[np.ndarray, float],
    fs: float = 1.0,
    title: str = "Frequency Response"
) -> None:
    w, h = signal.freqz(b, a, fs=fs)
    plt.figure()
    plt.plot(w, 20 * np.log10(np.abs(h)))
    plt.ylim(-80, 5)
    plt.xlim(0, fs/2)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain (dB)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    fs = 1000
    t = np.linspace(0, 1, fs)
    sig = np.sin(2*np.pi*5*t) + 0.5*np.random.randn(fs)

    # 1. Butterworth Lowpass
    b, a = FilterDesigner.design_iir('butterworth', 'lowpass', 4, 300, fs=fs)
    filtered = FilterApplier.apply_iir_fir(b, a, sig, zero_phase=True)

    # 2. FIR Highpass
    b_fir, a_fir = FilterDesigner.design_fir('highpass', 65, 20, fs=fs)
    plot_response(b_fir, a_fir,fs= fs)
    filtered_fir = FilterApplier.apply_iir_fir(b_fir, a_fir, sig)
    # 3. Gaussian Filter
    b_gauss, a_gauss = FilterDesigner.design_gaussian(31, 10, fs=fs)
    filtered_gauss = FilterApplier.apply_iir_fir(b_gauss, a_gauss, sig)
    # 4. Savitzky-Golay
    filtered_savgol = FilterApplier.apply_savgol(sig, 21, 3)
    
    # 5. Median Filter
    filtered_median = FilterApplier.apply_median(sig, 5)
    
    # 6. Kalman Filter
    kf = KalmanFilter1D(sig[0], 1.0, 0.1, 0.5)
    filtered_kalman = kf.filter(sig)
