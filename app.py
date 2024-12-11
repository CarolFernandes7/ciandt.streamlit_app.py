import os
import pandas as pd
import streamlit as st

# Function to load data for a segment
def load_data(segment, group=None):
    folder = os.path.join("data", segment)
    questions = {
        "Q5": "Which of the following best describes your combined household income?",
        "Q6": "Which statement best describes your household finances?",
        "Q7": "Do you own or rent your home?",
        "Q8": "What type of home do you own and live in?",
        "Q15": "What energy products do you currently own?",
        "Q22": "What is your home energy situation?"
    }
    data = {}
    total_respondents = 0

    for key, question in questions.items():
        # Adjust the file path based on the group
        if group == "Group B (Own Flat)":
            file_path = os.path.join(folder, "group b", f"{key}_Low_Group_B.csv")
        elif group == "Group C (Low Income)":
            file_mapping = {
                "Q5": "Q5_combined_household_income.csv",
                "Q6": "Q6_household_finances.csv",
                "Q7": "Q7_home_ownership.csv",
                "Q8": "Q8_home_type.csv",
                "Q15": "Q15_current_ownership.csv",
                "Q22": "Q22_home_energy_situation.csv"
            }
            file_path = os.path.join(folder, "group c", file_mapping[key])
        else:
            file_path = os.path.join(folder, f"{key}_{segment}.csv") if segment != "no_filter" else os.path.join(folder, f"{key}.csv")

        try:
            df = pd.read_csv(file_path)
            total_respondents = len(df)
            # Add % sign to all numeric columns
            for column in df.select_dtypes(include=['number']).columns:
                df[column] = df[column].apply(lambda x: f"{x:.2f}%" if not pd.isna(x) else x)

            data[question] = df
        except FileNotFoundError:
            if group == "Group A (Renters)":
                return None, 0
        except Exception as e:
            st.error(f"Error loading {file_path}: {e}")
            return None, 0

    return data, total_respondents


# Streamlit configuration
st.title("Data Analysis by Segment")
st.sidebar.title("Segment Selector")

# Sidebar options for selecting the segment
segment = st.sidebar.selectbox("Select Segment", ["No Filter", "High", "Medium", "Low"])

# If "Low" is selected, show options for subgroups
group = None
if segment == "Low":
    group = st.sidebar.selectbox("Select Low Group", ["Group A (Renters)", "Group B (Own Flat)", "Group C (Low Income)"])

# Load data based on selection
data, total_respondents = load_data(segment.lower().replace(" ", "_"), group)

# Display the total number of respondents and summary for each segment
if segment == "High":
    st.header("High Segment Summary")
    st.write("**SUMMARY**")
    st.write("Number of Responses: 71")
    st.write("Filtered Out: 95%")
    st.write("Confidence Level: 95%")
elif segment == "Medium":
    st.header("Medium Segment Summary")
    st.write("**SUMMARY**")
    st.write("Number of Responses: 738")
    st.write("Filtered Out: 52%")
    st.write("Confidence Level: 95%")
elif segment == "Low":
    if group == "Group A (Renters)":
        st.header("Low Segment - Group A (Renters)")
        st.warning("No data available for Group A (Renters).")
    elif group == "Group B (Own Flat)":
        st.header("Low Segment - Group B (Own Flat)")
        st.write("**SUMMARY**")
        st.write("Number of Responses: 138")
        st.write("Filtered Out: 91%")
        st.write("Confidence Level: 95%")
    elif group == "Group C (Low Income)":
        st.header("Low Segment - Group C (Low Income)")
        st.write("**SUMMARY**")
        st.write("Number of Responses: 27")
        st.write("Filtered Out: 98%")
        st.write("Confidence Level: 95%")

# Display the data in the app
if data:
    for question, df in data.items():
        st.subheader(question)
        st.write(df)
else:
    if segment != "Low" or (segment == "Low" and group != "Group A (Renters)"):
        st.error("Unable to load data. Please ensure the files are correctly structured.")