import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Student Placement Analysis",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("placement_dataset.csv")

df = load_data()

# -----------------------------
# Title
# -----------------------------
st.title("🎓 Student Placement Analysis Dashboard")
st.markdown(
    "Analyze student academic performance, skills, internships "
    "and placement outcomes."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

degrees = st.sidebar.multiselect(
    "Select Degree",
    options=sorted(df["Degree"].unique()),
    default=sorted(df["Degree"].unique())
)

status = st.sidebar.multiselect(
    "Placement Status",
    options=sorted(df["Placement_Status"].unique()),
    default=sorted(df["Placement_Status"].unique())
)

domains = st.sidebar.multiselect(
    "Preferred Domain",
    options=sorted(df["Preferred_Domain"].unique()),
    default=sorted(df["Preferred_Domain"].unique())
)

filtered_df = df[
    (df["Degree"].isin(degrees)) &
    (df["Placement_Status"].isin(status)) &
    (df["Preferred_Domain"].isin(domains))
]

# -----------------------------
# KPI Calculations
# -----------------------------
total_students = len(filtered_df)

placed_students = len(
    filtered_df[filtered_df["Placement_Status"] == "Placed"]
)

placement_rate = (
    placed_students / total_students * 100
    if total_students > 0 else 0
)

placed_data = filtered_df[
    filtered_df["Placement_Status"] == "Placed"
]

average_package = (
    placed_data["Package_LPA"].mean()
    if len(placed_data) > 0 else 0
)

average_cgpa = (
    filtered_df["CGPA"].mean()
    if total_students > 0 else 0
)

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "👨‍🎓 Total Students",
    total_students
)

col2.metric(
    "✅ Placed Students",
    placed_students
)

col3.metric(
    "📊 Placement Rate",
    f"{placement_rate:.1f}%"
)

col4.metric(
    "💰 Average Package",
    f"{average_package:.2f} LPA"
)

st.divider()

# -----------------------------
# Placement Distribution
# -----------------------------
st.subheader("📊 Placement Status")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()

    sns.countplot(
        data=filtered_df,
        x="Placement_Status",
        ax=ax
    )

    ax.set_title("Placed vs Not Placed")
    ax.set_xlabel("Placement Status")
    ax.set_ylabel("Number of Students")

    st.pyplot(fig)

with col2:
    status_counts = filtered_df["Placement_Status"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        status_counts.values,
        labels=status_counts.index,
        autopct="%1.1f%%"
    )

    ax.set_title("Placement Distribution")

    st.pyplot(fig)

# -----------------------------
# CGPA vs Placement
# -----------------------------
st.subheader("🎓 CGPA vs Placement")

fig, ax = plt.subplots()

sns.boxplot(
    data=filtered_df,
    x="Placement_Status",
    y="CGPA",
    ax=ax
)

ax.set_title("CGPA Distribution by Placement Status")

st.pyplot(fig)

# -----------------------------
# Internship Analysis
# -----------------------------
st.subheader("💼 Internship vs Placement")

internship_analysis = pd.crosstab(
    filtered_df["Internship"],
    filtered_df["Placement_Status"]
)

fig, ax = plt.subplots()

internship_analysis.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Internship Experience vs Placement")
ax.set_xlabel("Internship")
ax.set_ylabel("Number of Students")

plt.xticks(rotation=0)

st.pyplot(fig)

# -----------------------------
# Skills Analysis
# -----------------------------
st.subheader("🧠 Skills Analysis")

col1, col2 = st.columns(2)

with col1:

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="Technical_Skills",
        y="CGPA",
        hue="Placement_Status",
        ax=ax
    )

    ax.set_title("Technical Skills vs CGPA")

    st.pyplot(fig)

with col2:

    fig, ax = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="Communication_Skills",
        y="Aptitude_Score",
        hue="Placement_Status",
        ax=ax
    )

    ax.set_title("Communication Skills vs Aptitude")

    st.pyplot(fig)

# -----------------------------
# Domain Analysis
# -----------------------------
st.subheader("🌐 Placement by Preferred Domain")

domain_analysis = pd.crosstab(
    filtered_df["Preferred_Domain"],
    filtered_df["Placement_Status"]
)

fig, ax = plt.subplots(figsize=(10, 5))

domain_analysis.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Placement by Preferred Domain")
ax.set_xlabel("Preferred Domain")
ax.set_ylabel("Number of Students")

plt.xticks(rotation=30)

st.pyplot(fig)

# -----------------------------
# Package Analysis
# -----------------------------
st.subheader("💰 Salary Package Analysis")

if len(placed_data) > 0:

    fig, ax = plt.subplots()

    sns.histplot(
        placed_data["Package_LPA"],
        bins=15,
        kde=True,
        ax=ax
    )

    ax.set_title("Salary Package Distribution")
    ax.set_xlabel("Package (LPA)")
    ax.set_ylabel("Number of Students")

    st.pyplot(fig)

else:
    st.warning("No placed students available for the selected filters.")

# -----------------------------
# Academic Performance
# -----------------------------
st.subheader("📚 Academic Performance")

academic_columns = [
    "CGPA",
    "10th_Percentage",
    "12th_Percentage",
    "Aptitude_Score",
    "Coding_Score"
]

academic_average = filtered_df[academic_columns].mean()

fig, ax = plt.subplots()

academic_average.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Average Academic & Skill Scores")
ax.set_ylabel("Average Score")

plt.xticks(rotation=30)

st.pyplot(fig)

# -----------------------------
# Student Data
# -----------------------------
st.subheader("📋 Student Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------
# Download Filtered Data
# -----------------------------
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv,
    file_name="filtered_placement_dataset.csv",
    mime="text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Student Placement Analysis | Educational Project using Streamlit"
)