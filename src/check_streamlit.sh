#!/bin/bash

# Streamlit Process Monitor Script
# This script finds the Streamlit process and monitors it with psrecord

echo "=== Streamlit Process Monitor ==="
echo

# Get the PID for the streamlit app
echo "Looking for Streamlit processes..."
STREAMLIT_PID=$(pgrep -f "streamlit run")

# Check if we found a process
if [ -z "$STREAMLIT_PID" ]; then
    echo "No Streamlit process found!"
    echo "Make sure your Streamlit app is running first."
    echo "Start it with: streamlit run app.py"
    exit 1
fi

# Check if multiple processes found
PID_COUNT=$(echo "$STREAMLIT_PID" | wc -l)
if [ "$PID_COUNT" -gt 1 ]; then
    echo "Multiple Streamlit processes found:"
    echo "$STREAMLIT_PID"
    echo
    echo "Please specify which PID to monitor:"
    echo "Usage: $0 <PID>"
    echo "Or kill extra processes with: pkill -f 'streamlit run'"
    exit 1
fi

echo "Found Streamlit process with PID: $STREAMLIT_PID"
echo

# Allow manual PID override
if [ ! -z "$1" ]; then
    STREAMLIT_PID=$1
    echo "Using manually specified PID: $STREAMLIT_PID"
fi

# Check if psrecord is installed
if ! command -v psrecord &> /dev/null; then
    echo "psrecord is not installed!"
    echo "Install it with: pip install psrecord"
    exit 1
fi

# Create plot filename
PLOT_FILE="streamlit_plot.png"

echo "Starting monitoring"
echo "PID: $STREAMLIT_PID"
echo "Plot file: $PLOT_FILE"
echo "Press Ctrl+C to stop monitoring"
echo

# Start monitoring
psrecord $STREAMLIT_PID --plot $PLOT_FILE --interval 1

echo
echo "Monitoring stopped. Plot saved as: $PLOT_FILE"

# Try to open the plot
if command -v eog &> /dev/null; then
    echo "Opening plot with image viewer..."
    eog $PLOT_FILE &
elif command -v xdg-open &> /dev/null; then
    echo "Opening plot with default viewer"
    xdg-open $PLOT_FILE &
else
    echo "Plot saved. Open manually with your image viewer:"
    echo "    eog $PLOT_FILE"
fi