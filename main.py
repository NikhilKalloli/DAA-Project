import numpy as np
import time
import matplotlib.pyplot as plt

# Generate a sample signal
def generate_signal(N):
    t = np.linspace(0, 1, N)
    signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 10 * t)
    return t, signal

# Brute Force Fourier Series Analysis
def brute_force_fourier(signal, t, terms):
    N = len(signal)
    a0 = np.mean(signal)
    a = np.zeros(terms)
    b = np.zeros(terms)
    for n in range(1, terms + 1):
        a[n - 1] = 2 / N * np.sum(signal * np.cos(2 * np.pi * n * t))
        b[n - 1] = 2 / N * np.sum(signal * np.sin(2 * np.pi * n * t))
    return a0, a, b

# Optimized Brute Force Fourier Series Analysis using numpy vectorization
def optimized_brute_force_fourier(signal, t, terms):
    N = len(signal)
    a0 = np.mean(signal)
    n = np.arange(1, terms + 1).reshape(-1, 1)
    cos_terms = np.cos(2 * np.pi * n * t)
    sin_terms = np.sin(2 * np.pi * n * t)
    a = 2 / N * np.sum(signal * cos_terms, axis=1)
    b = 2 / N * np.sum(signal * sin_terms, axis=1)
    return a0, a, b


# Function to measure execution time
def measure_time(func, *args, repetitions=10):
    times = []
    for _ in range(repetitions):
        start_time = time.time()
        func(*args)
        times.append(time.time() - start_time)
    return np.mean(times)

# Measure times for different input sizes
sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]
brute_force_times = []
optimized_brute_force_times = []
fft_times = []

for size in sizes:
    t, signal = generate_signal(size)

    # Measure time for brute force method
    brute_force_time = measure_time(optimized_brute_force_fourier, signal, t, 10)
    brute_force_times.append(brute_force_time)

    # Measure time for optimized brute force method
    optimized_brute_force_time = measure_time(brute_force_fourier, signal, t, 10)
    optimized_brute_force_times.append(optimized_brute_force_time)


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(sizes, brute_force_times, label='Unoptimized', marker='o')
plt.plot(sizes, optimized_brute_force_times, label='Optimized', marker='o')
plt.xlabel('Input Size')
plt.ylabel('Time (seconds)')
plt.title('Time Comparison of Fourier Analysis Methods')
plt.legend()
plt.grid(True)
plt.show()
