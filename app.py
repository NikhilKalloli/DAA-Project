import numpy as np
import matplotlib.pyplot as plt

# Generate a sample signal
def generate_signal(N, sampling_rate=1000):
    t = np.linspace(0, 1, N, endpoint=False)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)
    return t, signal

# Perform FFT and separate frequency components
def separate_frequencies(signal, sampling_rate=1000):
    N = len(signal)
    # Compute FFT
    fft_result = np.fft.fft(signal)
    # Compute frequencies
    freqs = np.fft.fftfreq(N, 1 / sampling_rate)
    
    # Create a mask for positive frequencies
    mask = freqs > 0
    
    # Get amplitude and phase
    amplitudes = 2 / N * np.abs(fft_result[mask])
    phases = np.angle(fft_result[mask])
    
    return freqs[mask], amplitudes, phases

# Reconstruct the signal from selected frequencies
def reconstruct_signal(freqs, amplitudes, phases, t):
    N = len(t)
    reconstructed_signal = np.zeros(N)
    
    for i, freq in enumerate(freqs):
        reconstructed_signal += amplitudes[i] * np.cos(2 * np.pi * freq * t + phases[i])
    
    return reconstructed_signal

# Parameters
N = 1024
sampling_rate = 1000

# Generate signal
t, signal = generate_signal(N, sampling_rate)

# Separate frequencies using FFT
freqs, amplitudes, phases = separate_frequencies(signal, sampling_rate)

# Reconstruct signal using only the dominant frequencies
dominant_freqs = freqs[:2]  # Only use the first two frequencies (5 Hz and 10 Hz)
dominant_amplitudes = amplitudes[:2]
dominant_phases = phases[:2]
reconstructed_signal = reconstruct_signal(dominant_freqs, dominant_amplitudes, dominant_phases, t)

# Plot original and reconstructed signals
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('Original Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.plot(t, reconstructed_signal)
plt.title('Reconstructed Signal from Dominant Frequencies')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

# Plot the frequency spectrum
plt.figure(figsize=(10, 6))
plt.stem(freqs, amplitudes, use_line_collection=True)
plt.title('Frequency Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()
