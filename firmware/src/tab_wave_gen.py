import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import resample
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import os

def generate_wave():
    # Parameter aus den Eingabefeldern holen
    sampling_rate = int(sampling_rate_entry.get())
    frequency = int(frequency_entry.get())
    duration = float(duration_entry.get())
    decay_constant = int(decay_constant_entry.get())
    amplitude = float(amplitude_entry.get())
    second_harmonic = float(second_harmonic_entry.get())
    third_harmonic = float(third_harmonic_entry.get())
    fourth_harmonic = float(fourth_harmonic_entry.get())
    fifth_harmonic = float(fifth_harmonic_entry.get())
    sixth_harmonic = float(sixth_harmonic_entry.get())
    seventh_harmonic = float(seventh_harmonic_entry.get())

    # Amplitudes for fundamental frequency and overtones
    amplitudes = [
        amplitude * 1.0,
        amplitude * second_harmonic,
        amplitude * third_harmonic,
        amplitude * fourth_harmonic,
        amplitude * fifth_harmonic,
        amplitude * sixth_harmonic,
        amplitude * seventh_harmonic
    ]

    # Calculate time step and number of samples
    sample_time = 1.0 / sampling_rate
    sample_count = int(round(duration / sample_time))

    # Create time axis and envelope
    time = np.linspace(0, duration, sample_count, endpoint=False)
    envelope = np.exp(-decay_constant * time)

    # Generate damped oscillation with overtones
    oscillation = envelope * sum(
        amplitudes[n] * np.sin(2 * np.pi * (n + 1) * frequency * time)
        for n in range(len(amplitudes))
    )

    # Scale and shift the oscillation (for range [0, 1024])
    oscillation_shifted = oscillation - np.min(oscillation)
    oscillation_scaled = (oscillation_shifted / np.max(oscillation_shifted)) * 1023 * amplitude
    oscillation_scaled = np.round(oscillation_scaled).astype(int)

    # Generate absolute path to script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate C array
    c_array_name = "sine_wave"
    num_samples = len(oscillation_scaled)
    
    c_code = f"#define NUM_OF_SAMPLES ({num_samples})\n\n"
    c_code += f"const uint16_t {c_array_name}[NUM_OF_SAMPLES] = {{\n"

    for i in range(0, num_samples, 8):
        group = oscillation_scaled[i:i+8]
        line = ",\t".join(f"0x{value:03X}" for value in group)
        c_code += line + ",\n"

    c_code = c_code.rstrip(",\n") + "\n};"

    # Save C file
    header_file = os.path.join(script_dir, "wave_array.h")
    
    with open(header_file, "w") as file:
        file.write(c_code)

    # Normalize the signal for WAV file
    oscillation_normalized = np.int16((oscillation / np.max(np.abs(oscillation))) * 32767)

    # Target sampling rate for WAV file
    target_sampling_rate = 44100
    num_samples_target = int(round(duration * target_sampling_rate))
    
    oscillation_resampled = resample(oscillation_normalized, num_samples_target)
    oscillation_resampled = np.round(oscillation_resampled).astype(np.int16)

    # Save WAV file
    wav_file = os.path.join(script_dir, "test_44100Hz.wav")
    
    write(wav_file, target_sampling_rate, oscillation_resampled)

    # Visualization
    ax.clear()
    
    ax.plot(time, oscillation, plot_style.get())  # Use the selected plot style
    
    ax.set_title('Oscillation with overtones')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    
    ax.grid(True)
    
    canvas.draw()

def toggle_plot_style():
    if plot_style.get() == "o-":
        plot_style.set("-")
    else:
        plot_style.set("o-")
    
    generate_wave()  # Update the plot when toggling

# Tkinter GUI setup
root = tk.Tk()
root.geometry("1000x700")
root.title("Waveform Generator")

# Create a frame for input fields
input_frame = ttk.Frame(root)
input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

# Input fields for parameters
ttk.Label(input_frame, text="Sampling Rate (Hz):").pack(anchor=tk.W, pady=2)
sampling_rate_entry = ttk.Entry(input_frame)
sampling_rate_entry.insert(0, "500000")
sampling_rate_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="Fundamental Frequency (Hz):").pack(anchor=tk.W, pady=2)
frequency_entry = ttk.Entry(input_frame)
frequency_entry.insert(0, "10000")
frequency_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="2nd Harmonic (factor):").pack(anchor=tk.W, pady=2)
second_harmonic_entry = ttk.Entry(input_frame)
second_harmonic_entry.insert(0, "0.2")
second_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="3rd Harmonic (factor):").pack(anchor=tk.W, pady=2)
third_harmonic_entry = ttk.Entry(input_frame)
third_harmonic_entry.insert(0, "0.4")
third_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="4th Harmonic (factor):").pack(anchor=tk.W, pady=2)
fourth_harmonic_entry = ttk.Entry(input_frame)
fourth_harmonic_entry.insert(0, "0.1")
fourth_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="5th Harmonic (factor):").pack(anchor=tk.W, pady=2)
fifth_harmonic_entry = ttk.Entry(input_frame)
fifth_harmonic_entry.insert(0, "0.0")
fifth_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="6th Harmonic (factor):").pack(anchor=tk.W, pady=2)
sixth_harmonic_entry = ttk.Entry(input_frame)
sixth_harmonic_entry.insert(0, "0.0")
sixth_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="7th Harmonic (factor):").pack(anchor=tk.W, pady=2)
seventh_harmonic_entry = ttk.Entry(input_frame)
seventh_harmonic_entry.insert(0, "0.0")
seventh_harmonic_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="Duration (s):").pack(anchor=tk.W, pady=2)
duration_entry = ttk.Entry(input_frame)
duration_entry.insert(0, "0.01")
duration_entry.pack(fill=tk.X, pady=2)

ttk.Label(input_frame, text="Decay Constant:").pack(anchor=tk.W, pady=2)
decay_constant_entry = ttk.Entry(input_frame)
decay_constant_entry.insert(0,"1000")
decay_constant_entry.pack(fill=tk.X,pady=2)

ttk.Label(input_frame,text="Amplitude:").pack(anchor=tk.W,pady=2)
amplitude_entry=ttk.Entry(input_frame)
amplitude_entry.insert(0,"1.0")
amplitude_entry.pack(fill=tk.X,pady=2)

# Button to generate wave
generate_button = ttk.Button(input_frame,text="Generate Wave",command=generate_wave)
generate_button.pack(pady=10)

# Frame for the plot
plot_frame = ttk.Frame(root)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH , expand=True , padx=10 , pady=10)

# Matplotlib figure setup
fig , ax = plt.subplots(figsize=(3 , 2))
canvas = FigureCanvasTkAgg(fig , master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH , expand=True)

# Toolbar for navigation
toolbar = NavigationToolbar2Tk(canvas , plot_frame )
toolbar.pack(side=tk.BOTTOM , fill=tk.X )

# Variable to store plot style and default value 
plot_style = tk.StringVar(value="-")

# Button to toggle plot style 
toggle_button = ttk.Button(input_frame , text="Toggle Dot's" , command=toggle_plot_style )
toggle_button.pack(pady=10)

root.mainloop()
