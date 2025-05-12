import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF
import os
import numpy as np
from PIL import Image

# Initialize session state for all tracking features
if 'bmi_history' not in st.session_state:
    st.session_state.bmi_history = []
if 'goals' not in st.session_state:
    st.session_state.goals = {
        'target_bmi': None,
        'target_date': None,
        'current_bmi': None
    }
if 'water_intake' not in st.session_state:
    st.session_state.water_intake = []
if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = []
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'meals' not in st.session_state:
    st.session_state.meals = []

# Page config
st.set_page_config(page_title="Advanced Health Tracker", page_icon="⚖️", layout="wide")

# Sidebar
st.sidebar.title("Settings")
height_unit = st.sidebar.radio("Height Unit", ["cm", "m"])
weight_unit = st.sidebar.radio("Weight Unit", ["kg", "lbs"])

# Main content
st.title("🏥 Advanced Health & Fitness Tracker")
st.write("""
Track your BMI, nutrition, workouts, and overall health metrics in one place.
""")

# Create tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs(["BMI & Health", "Nutrition", "Workouts", "Lifestyle", "Reports"])

with tab1:
    # Original BMI calculator content with enhancements
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.subheader("Basic Information")
        age = st.number_input("Age", min_value=2, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity_level = st.selectbox("Activity Level", 
            ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"])

        height = st.number_input(f"Height ({height_unit})", min_value=50.0, max_value=250.0, value=170.0, step=0.1)
        weight = st.number_input(f"Weight ({weight_unit})", min_value=10.0, max_value=300.0, value=70.0, step=0.1)
        
        if height_unit == "m":
            height_m = height
        else:
            height_m = height / 100
            
        if weight_unit == "lbs":
            weight_kg = weight * 0.453592
        else:
            weight_kg = weight

        if st.button("Calculate Health Metrics"):
            # Calculate BMI and other metrics
            bmi = weight_kg / (height_m ** 2)
            bmi_rounded = round(bmi, 2)

            # Calculate Body Fat Percentage
            if gender == "Male":
                body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
            else:
                body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
            body_fat = round(body_fat, 1)

            # Calculate BMR and TDEE
            if gender == "Male":
                bmr = (10 * weight_kg) + (6.25 * height_m * 100) - (5 * age) + 5
            else:
                bmr = (10 * weight_kg) + (6.25 * height_m * 100) - (5 * age) - 161

            activity_multipliers = {
                "Sedentary": 1.2,
                "Lightly Active": 1.375,
                "Moderately Active": 1.55,
                "Very Active": 1.725,
                "Extra Active": 1.9
            }
            tdee = bmr * activity_multipliers[activity_level]

            # Store metrics
            st.session_state.bmi_history.append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'bmi': bmi_rounded,
                'weight': weight_kg,
                'height': height_m,
                'body_fat': body_fat,
                'tdee': round(tdee, 0)
            })

            # Display results
            st.markdown(f"""
            <div style='padding: 1em; border-radius: 10px; background-color: {color}; color: white; text-align: center;'>
                <h2>BMI: {bmi_rounded}</h2>
                <h3>Category: {category}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style='padding: 1em; border-radius: 10px; background-color: #f8f9fa;'>
                <h4>Additional Metrics:</h4>
                <p>Body Fat Percentage: {body_fat}%</p>
                <p>BMR (Basal Metabolic Rate): {round(bmr, 0)} calories/day</p>
                <p>TDEE (Total Daily Energy Expenditure): {round(tdee, 0)} calories/day</p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # BMI Range Chart
        st.subheader("BMI Categories")
        bmi_ranges = pd.DataFrame({
            'Category': ['Underweight', 'Normal', 'Overweight', 'Obese'],
            'Range': ['< 18.5', '18.5 - 24.9', '25 - 29.9', '≥ 30'],
            'Color': ['#3498db', '#2ecc71', '#f1c40f', '#e74c3c']
        })
        st.dataframe(bmi_ranges, hide_index=True)

    with col3:
        # Goal Setting
        st.subheader("Set Your Goals")
        target_bmi = st.number_input("Target BMI", min_value=18.5, max_value=30.0, value=22.0, step=0.1)
        target_date = st.date_input("Target Date", value=datetime.now())
        
        if st.button("Set Goal"):
            st.session_state.goals = {
                'target_bmi': target_bmi,
                'target_date': target_date,
                'current_bmi': st.session_state.bmi_history[-1]['bmi'] if st.session_state.bmi_history else None
            }
            st.success("Goal set successfully!")

with tab2:
    # Nutrition Tracking
    st.subheader("Meal Planner & Calorie Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Meal Input
        meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        food_item = st.text_input("Food Item")
        calories = st.number_input("Calories", min_value=0, value=0)
        
        if st.button("Add Meal"):
            st.session_state.meals.append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'meal_type': meal_type,
                'food_item': food_item,
                'calories': calories
            })
            st.success("Meal added successfully!")
    
    with col2:
        # Daily Summary
        if st.session_state.meals:
            today_meals = [meal for meal in st.session_state.meals 
                         if meal['date'] == datetime.now().strftime("%Y-%m-%d")]
            total_calories = sum(meal['calories'] for meal in today_meals)
            
            st.metric("Today's Total Calories", total_calories)
            
            # Calorie distribution chart
            meal_calories = pd.DataFrame(today_meals)
            if not meal_calories.empty:
                fig = px.pie(meal_calories, values='calories', names='meal_type',
                           title='Calorie Distribution by Meal')
                st.plotly_chart(fig)

with tab3:
    # Workout Recommendations
    st.subheader("Workout Recommendations")
    
    # Get user's current BMI category
    current_bmi = st.session_state.bmi_history[-1]['bmi'] if st.session_state.bmi_history else None
    
    if current_bmi:
        if current_bmi < 18.5:
            st.write("""
            ### Recommended Workouts for Underweight:
            - Strength training 3-4 times per week
            - Compound exercises (squats, deadlifts, bench press)
            - Progressive overload
            - Adequate rest between sets
            """)
        elif 18.5 <= current_bmi < 25:
            st.write("""
            ### Recommended Workouts for Normal Weight:
            - Mix of cardio and strength training
            - HIIT workouts 2-3 times per week
            - Yoga or flexibility training
            - Sports or recreational activities
            """)
        elif 25 <= current_bmi < 30:
            st.write("""
            ### Recommended Workouts for Overweight:
            - Low-impact cardio (walking, swimming)
            - Bodyweight exercises
            - Circuit training
            - Gradual intensity progression
            """)
        else:
            st.write("""
            ### Recommended Workouts for Obese:
            - Walking
            - Swimming
            - Chair exercises
            - Light stretching
            - Consult a healthcare provider before starting
            """)

with tab4:
    # Lifestyle Tracking
    st.subheader("Lifestyle Tracking")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Water Intake Tracker
        st.write("### Water Intake")
        water_amount = st.number_input("Water (ml)", min_value=0, value=0)
        if st.button("Add Water"):
            st.session_state.water_intake.append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'amount': water_amount
            })
            st.success("Water intake recorded!")
        
        # Sleep Tracker
        st.write("### Sleep Tracker")
        sleep_hours = st.number_input("Sleep Hours", min_value=0.0, max_value=24.0, value=8.0, step=0.5)
        sleep_quality = st.slider("Sleep Quality", 1, 10, 7)
        if st.button("Record Sleep"):
            st.session_state.sleep_data.append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'hours': sleep_hours,
                'quality': sleep_quality
            })
            st.success("Sleep recorded!")
    
    with col2:
        # Mood Tracker
        st.write("### Mood Tracker")
        mood = st.select_slider("How are you feeling?", 
                              options=["😢", "😕", "😐", "🙂", "😄"],
                              value="😐")
        mood_note = st.text_area("Notes (optional)")
        if st.button("Record Mood"):
            st.session_state.mood_data.append({
                'date': datetime.now().strftime("%Y-%m-%d"),
                'mood': mood,
                'note': mood_note
            })
            st.success("Mood recorded!")

with tab5:
    # Reports and Analytics
    st.subheader("Health Reports & Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                 value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    if st.button("Generate Report"):
        # Create comprehensive report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Comprehensive Health Report", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        
        # Add BMI history
        if st.session_state.bmi_history:
            pdf.cell(200, 10, "BMI History:", ln=True)
            for entry in st.session_state.bmi_history:
                pdf.cell(200, 10, f"Date: {entry['date']}, BMI: {entry['bmi']}", ln=True)
        
        # Add nutrition summary
        if st.session_state.meals:
            pdf.cell(200, 10, "Nutrition Summary:", ln=True)
            for meal in st.session_state.meals:
                pdf.cell(200, 10, f"Date: {meal['date']}, {meal['meal_type']}: {meal['food_item']} ({meal['calories']} cal)", ln=True)
        
        # Add lifestyle data
        if st.session_state.water_intake:
            pdf.cell(200, 10, "Water Intake:", ln=True)
            for entry in st.session_state.water_intake:
                pdf.cell(200, 10, f"Date: {entry['date']}, Amount: {entry['amount']}ml", ln=True)
        
        if st.session_state.sleep_data:
            pdf.cell(200, 10, "Sleep Data:", ln=True)
            for entry in st.session_state.sleep_data:
                pdf.cell(200, 10, f"Date: {entry['date']}, Hours: {entry['hours']}, Quality: {entry['quality']}/10", ln=True)
        
        # Save and provide download
        pdf_path = "health_report.pdf"
        pdf.output(pdf_path)
        st.success("Report generated successfully!")
        
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Download Health Report",
                data=file,
                file_name="health_report.pdf",
                mime="application/pdf"
            )

# Add a clear all data button in the sidebar
if st.sidebar.button("Clear All Data"):
    st.session_state.bmi_history = []
    st.session_state.goals = {
        'target_bmi': None,
        'target_date': None,
        'current_bmi': None
    }
    st.session_state.water_intake = []
    st.session_state.sleep_data = []
    st.session_state.mood_data = []
    st.session_state.meals = []
    st.experimental_rerun() 