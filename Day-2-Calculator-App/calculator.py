import streamlit as st
import numpy as np
import math
from datetime import datetime
import re

# Set page configuration
st.set_page_config(
    page_title="Advanced Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'theme' not in st.session_state:
    st.session_state.theme = "Light"
if 'memory' not in st.session_state:
    st.session_state.memory = 0
if 'history' not in st.session_state:
    st.session_state.history = []
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Theme-specific CSS
def get_theme_css(theme):
    if theme == "Dark":
        return """
        .main {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.02);
        }
        .result {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 1px solid #3D3D3D;
        }
        .stSelectbox, .stNumberInput, .stTextInput {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        h1, h2, h3 {
            color: #FFFFFF;
        }
        .sidebar .sidebar-content {
            background-color: #2D2D2D;
            color: #FFFFFF;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #2D2D2D;
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
        }
        .error-message {
            color: #ff6b6b;
            background-color: #2D2D2D;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        """
    else:  # Light theme
        return """
        .main {
            background-color: #f5f5f5;
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: scale(1.02);
        }
        .result {
            background-color: white;
            color: #2c3e50;
            border: 1px solid #e0e0e0;
        }
        .stSelectbox, .stNumberInput, .stTextInput {
            background-color: white;
            color: #2c3e50;
        }
        h1, h2, h3 {
            color: #2c3e50;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: white;
        }
        .stTabs [data-baseweb="tab"] {
            color: #2c3e50;
        }
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: white;
        }
        .error-message {
            color: #dc3545;
            background-color: #f8d7da;
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
        }
        """

# Apply theme CSS
st.markdown(f"""
    <style>
    {get_theme_css(st.session_state.theme)}
    
    /* Common styles */
    .stButton>button {{
        width: 100%;
        height: 50px;
        font-size: 20px;
        margin: 2px;
        border-radius: 10px;
    }}
    .result {{
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    .stSelectbox, .stNumberInput, .stTextInput {{
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# Error handling functions
def validate_number_input(value, field_name):
    try:
        float(value)
        return True, None
    except ValueError:
        return False, f"Invalid input for {field_name}. Please enter a valid number."

def validate_statistics_input(numbers_str):
    try:
        # Remove any whitespace and split by comma
        numbers = [x.strip() for x in numbers_str.split(",")]
        # Validate each number
        for num in numbers:
            if not num:  # Skip empty strings
                continue
            try:
                float(num)
            except ValueError:
                return False, f"Invalid number found: {num}"
        return True, None
    except Exception as e:
        return False, f"Error processing input: {str(e)}"

def format_result(result):
    """Format the result to avoid scientific notation for small numbers"""
    if isinstance(result, (int, float)):
        if abs(result) < 1e-10:
            return "0"
        elif abs(result) < 1e-6:
            return f"{result:.10f}"
        else:
            return f"{result:.4f}"
    return str(result)

# Sidebar
with st.sidebar:
    st.title("🧮 Calculator")
    st.markdown("---")
    
    # Theme selector
    st.markdown("### Theme")
    theme = st.radio(
        "Choose Theme",
        ["Light", "Dark"],
        horizontal=True,
        key="theme_selector",
        label_visibility="collapsed"
    )
    
    # Update theme in session state
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.experimental_rerun()
    
    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("- [Basic Operations](#basic-operations)")
    st.markdown("- [Scientific Functions](#scientific-functions)")
    st.markdown("- [Unit Converter](#unit-converter)")
    st.markdown("- [Statistics](#statistics-calculator)")
    st.markdown("---")
    st.markdown("### Current Time")
    st.markdown(f"🕒 {datetime.now().strftime('%H:%M:%S')}")

# Main content
st.title("🧮 Advanced Scientific Calculator By Syed Mujtaba Abbas")
st.markdown("A powerful calculator with advanced mathematical functions and unit conversions")

# Create tabs for different calculator sections
tab1, tab2, tab3, tab4 = st.tabs(["Basic Operations", "Scientific Functions", "Unit Converter", "Statistics"])

with tab1:
    st.header("Basic Operations")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        num1 = st.number_input("First Number", value=0.0, step=0.1)
        num2 = st.number_input("Second Number", value=0.0, step=0.1)
        
        operation = st.selectbox(
            "Select Operation",
            ["Addition", "Subtraction", "Multiplication", "Division", "Power", "Square Root", "Logarithm"]
        )
        
        if st.button("Calculate", key="basic_calc"):
            try:
                if operation == "Addition":
                    result = num1 + num2
                elif operation == "Subtraction":
                    result = num1 - num2
                elif operation == "Multiplication":
                    result = num1 * num2
                elif operation == "Division":
                    if num2 == 0:
                        st.error("Cannot divide by zero!")
                        result = None
                    else:
                        result = num1 / num2
                elif operation == "Power":
                    result = num1 ** num2
                elif operation == "Square Root":
                    if num1 < 0:
                        st.error("Cannot calculate square root of negative number!")
                        result = None
                    else:
                        result = math.sqrt(num1)
                elif operation == "Logarithm":
                    if num1 <= 0:
                        st.error("Cannot calculate logarithm of non-positive number!")
                        result = None
                    elif num2 <= 0 or num2 == 1:
                        st.error("Logarithm base must be positive and not equal to 1!")
                        result = None
                    else:
                        result = math.log(num1, num2)
                
                if result is not None:
                    formatted_result = format_result(result)
                    st.markdown(f'<div class="result">Result: {formatted_result}</div>', unsafe_allow_html=True)
                    st.session_state.memory = result
                    st.session_state.last_result = result
                    st.session_state.history.append(f"{num1} {operation} {num2} = {formatted_result}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with col2:
        st.subheader("Memory Operations")
        if st.button("Store in Memory"):
            st.session_state.memory = num1
            st.success(f"Stored {format_result(num1)} in memory")
        
        if st.button("Recall Memory"):
            st.markdown(f'<div class="result">Memory Value: {format_result(st.session_state.memory)}</div>', unsafe_allow_html=True)
        
        if st.button("Clear Memory"):
            st.session_state.memory = 0
            st.success("Memory cleared")
        
        st.subheader("Calculation History")
        for calc in reversed(st.session_state.history[-5:]):
            st.markdown(f"- {calc}")

with tab2:
    st.header("Scientific Functions")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trigonometric Functions")
        angle = st.number_input("Angle (in degrees)", value=0.0, step=0.1, key="angle")
        if st.button("Calculate Trig Functions"):
            try:
                rad = math.radians(angle)
                sin_val = math.sin(rad)
                cos_val = math.cos(rad)
                tan_val = math.tan(rad)
                
                st.markdown(f"""
                <div class="result">
                sin({angle}°) = {format_result(sin_val)}<br>
                cos({angle}°) = {format_result(cos_val)}<br>
                tan({angle}°) = {format_result(tan_val)}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error calculating trigonometric functions: {str(e)}")
    
    with col2:
        st.subheader("Other Scientific Functions")
        num = st.number_input("Enter a number", value=0.0, step=0.1, key="scientific")
        function = st.selectbox(
            "Select Function",
            ["Factorial", "Exponential", "Natural Logarithm", "Absolute Value", "Floor", "Ceiling"]
        )
        
        if st.button("Calculate"):
            try:
                if function == "Factorial":
                    if num < 0 or num != int(num):
                        st.error("Factorial is only defined for non-negative integers!")
                        result = None
                    else:
                        result = math.factorial(int(num))
                elif function == "Exponential":
                    result = math.exp(num)
                elif function == "Natural Logarithm":
                    if num <= 0:
                        st.error("Natural logarithm is only defined for positive numbers!")
                        result = None
                    else:
                        result = math.log(num)
                elif function == "Absolute Value":
                    result = abs(num)
                elif function == "Floor":
                    result = math.floor(num)
                elif function == "Ceiling":
                    result = math.ceil(num)
                
                if result is not None:
                    formatted_result = format_result(result)
                    st.markdown(f'<div class="result">Result: {formatted_result}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

with tab3:
    st.header("Unit Converter")
    col1, col2 = st.columns(2)
    
    with col1:
        conversion_type = st.selectbox(
            "Select Conversion Type",
            ["Length", "Weight", "Temperature", "Time"]
        )
        
        if conversion_type == "Length":
            from_unit = st.selectbox("From", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Inches", "Feet", "Yards", "Miles"])
            to_unit = st.selectbox("To", ["Meters", "Kilometers", "Centimeters", "Millimeters", "Inches", "Feet", "Yards", "Miles"])
        elif conversion_type == "Weight":
            from_unit = st.selectbox("From", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
            to_unit = st.selectbox("To", ["Kilograms", "Grams", "Milligrams", "Pounds", "Ounces"])
        elif conversion_type == "Temperature":
            from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
            to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])
        else:  # Time
            from_unit = st.selectbox("From", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"])
            to_unit = st.selectbox("To", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"])
    
    with col2:
        value = st.number_input("Enter value to convert", value=0.0, step=0.1)
        
        if st.button("Convert"):
            try:
                # Conversion logic would go here
                # This is a simplified example
                result = value * 1.0  # Placeholder conversion
                formatted_result = format_result(result)
                st.markdown(f'<div class="result">{value} {from_unit} = {formatted_result} {to_unit}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred during conversion: {str(e)}")

with tab4:
    st.header("Statistics Calculator")
    
    numbers = st.text_input("Enter numbers (comma-separated)", "1,2,3,4,5")
    if st.button("Calculate Statistics"):
        try:
            # Validate input
            is_valid, error_msg = validate_statistics_input(numbers)
            if not is_valid:
                st.error(error_msg)
            else:
                num_list = [float(x.strip()) for x in numbers.split(",") if x.strip()]
                if not num_list:
                    st.error("Please enter at least one number")
                else:
                    mean = np.mean(num_list)
                    median = np.median(num_list)
                    std = np.std(num_list)
                    variance = np.var(num_list)
                    min_val = np.min(num_list)
                    max_val = np.max(num_list)
                    
                    st.markdown(f"""
                    <div class="result">
                    Mean: {format_result(mean)}<br>
                    Median: {format_result(median)}<br>
                    Standard Deviation: {format_result(std)}<br>
                    Variance: {format_result(variance)}<br>
                    Minimum: {format_result(min_val)}<br>
                    Maximum: {format_result(max_val)}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Create a simple histogram
                    st.subheader("Data Distribution")
                    st.bar_chart(num_list)
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit") 