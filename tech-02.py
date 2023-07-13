import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import io
import time

# Define the app layout
st.title('Waveform Tech 02')

# Generate text inputs for adjusting phi and amplitude
col1, col2 = st.columns(2)

with col1:
    phi_input = st.empty()
    phi = phi_input.text_input('Phi', value='0.0')

with col2:
    amplitude_input = st.empty()
    amplitude = amplitude_input.text_input('Amplitude', value='0.0')

# Convert phi and amplitude values to float
phi = float(phi) * np.pi
amplitude = float(amplitude)

# Generate sample data for sine wave, square wave, and sawtooth wave
num_cycles = np.abs(phi / (2 * np.pi))  # Number of cycles desired
x = np.linspace(0, num_cycles * 2 * np.pi, 1000)

current_wave = None
current_data = None  # Store the current waveform data

# Initialize the figure
figure = go.Figure()

# Create buttons for selecting the waveforms
col1, col2, col3 = st.columns(3)
with col1:
    if st.button('Sine Wave'):
        current_wave = amplitude * np.sin(x + phi)
        current_data = {'Time': x, 'Amplitude': current_wave}  # Store the current waveform data
        figure = go.Figure(data=go.Scatter(x=x, y=current_wave, mode='lines'))

with col2:
    if st.button('Square Wave'):
        current_wave = amplitude * np.sign(np.sin(x + phi))
        current_data = {'Time': x, 'Amplitude': current_wave}  # Store the current waveform data
        figure = go.Figure(data=go.Scatter(x=x, y=current_wave, mode='lines'))

with col3:
    if st.button('Sawtooth Wave'):
        current_wave = amplitude * (2 * ((x + phi) % (2 * np.pi)) / (2 * np.pi) - 1)
        current_data = {'Time': x, 'Amplitude': current_wave}  # Store the current waveform data
        figure = go.Figure(data=go.Scatter(x=x, y=current_wave, mode='lines'))

# Plot the selected waveform
figure.update_layout(
    title='Waveform',
    xaxis_title='Phi',
    yaxis_title='Amplitude'
)

# Display the plot
chart_placeholder = st.empty()
chart = chart_placeholder.plotly_chart(figure)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button('Reset'):
        phi = 0.0
        amplitude = 0.0
        current_wave = np.zeros_like(x)
        current_data = {'Time': x, 'Amplitude': current_wave}  # Update the current waveform data
        figure = go.Figure(data=go.Scatter(x=x, y=current_wave, mode='lines'))
        phi_input.text_input('Phi', value='1.0', key=f'phi_input_{time.time()}')

        amplitude_input.text_input('Amplitude', value='0.0', key=f'amplitude_input_{time.time()}')

with col2:
        with st.spinner('Generating CSV...'):
            data = current_data  # Use the current waveform data for CSV generation
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            csv_bytes = csv.encode()
            csv_io = io.BytesIO(csv_bytes)
            st.download_button(label="Download CSV", data=csv_io, file_name="waveform.csv", mime='text/csv')

with col3:
        with st.spinner('Generating JPG...'):
            fig = figure.to_image(format="jpeg")
            fig_io = io.BytesIO(fig)
            st.download_button(label="Download JPG", data=fig_io, file_name="waveform.jpg", mime="image/jpeg")