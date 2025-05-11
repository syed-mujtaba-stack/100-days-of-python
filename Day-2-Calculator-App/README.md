# Advanced Calculator App

A powerful calculator application built with Python and Streamlit, featuring both basic and advanced mathematical functions.

## Features

### Basic Operations
- Addition
- Subtraction
- Multiplication
- Division
- Power
- Square Root
- Logarithm

### Advanced Functions
- Trigonometric Functions (sin, cos, tan)
- Memory Operations (Store, Recall, Clear)
- Statistics Calculator (Mean, Median, Standard Deviation)

## Installation

1. Make sure you have Python installed on your system
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the calculator, use the following command:
```bash
streamlit run calculator.py
```

The application will open in your default web browser.

## Usage

1. **Basic Operations**
   - Enter two numbers
   - Select the desired operation
   - Click "Calculate" to see the result

2. **Advanced Functions**
   - Enter an angle in degrees to calculate trigonometric functions
   - Use memory operations to store and recall values
   - Enter comma-separated numbers for statistical calculations

## Error Handling

The calculator includes error handling for:
- Division by zero
- Square root of negative numbers
- Logarithm of non-positive numbers
- Invalid input formats

## Built With

- Python
- Streamlit
- NumPy
- Math module 