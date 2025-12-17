"""
YMCA Program Particiaption and Retention Analysis
Author: Ashley Payne
Description:
Analyzes YMCA program participation data to identify
attendnace trends and participant retention patterns using Python.
"""


import pandas as pd
import matplotlib.pyplot as plt

# Steps:

# 1. Load data
df = pd.read_csv("program_participation.csv")
print(df.head())
print(df.info())

# ============================================
# 2. Clean data
## Convert date columns to datetime
df["enrollment_date"] = pd.to_datetime(df["enrollment_date"])
df["attendance_date"] = pd.to_datetime(df["attendance_date"])

print(df.dtypes)

## Check for missing values
print(df.isnull().sum())

## Create month column for trend analysis
df["attendance_month"] = df["attendance_date"].dt.strftime("%Y-%m")

## Check unqiue programs and age groups
print(df["program_name"].unique())
print(df["age_group"].unique())

# ============================================
# 3. Participation analysis
## Calculate attendance rate by program
attendance_by_program = ( df.groupby("program_name")["attended"].mean().reset_index())

attendance_by_program["attendance_rate"] = attendance_by_program["attended"] * 100
print(attendance_by_program)

## Plot attendance rate by program
plt.figure()
plt.bar(
    attendance_by_program["program_name"],
    attendance_by_program["attendance_rate"]
)

plt.title("Attendance Rate by Program")
plt.xlabel("Program")
plt.ylabel("Attendance Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

## Insights:
## 	Youth Sports and After School Care show a higher attendance rate than the remaining three
## 	There is stronger engagement with consistent afterschool care through the school years, than seasonal activities such as clubs and sports
   
## Calculate monthly attendance rates
monthly_attendance = ( df.groupby("attendance_month")["attended"].mean().reset_index())

monthly_attendance["attendance_rate"] = monthly_attendance["attended"] * 100
print(monthly_attendance.head())

## Plot monthly attendance trend
plt.figure()
plt.plot(
    monthly_attendance["attendance_month"],
    monthly_attendance["attendance_rate"],
    marker="o"
)

plt.title("Monthly Attendance Trend")
plt.xlabel("Month")
plt.ylabel("Attendance Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

## Insights:
##	The monthly attendance trend has a downward slope and decreases from Jan to September.
##	This indicates that parents are pulling children out of program as the school year ends and summer begins.
##	The spike from September to October shows that parents are registering children back in programs as the school year starts again.

## Monthly attendance trend by program
monthly_program_attendance = ( df.groupby(["attendance_month", "program_name"])["attended"].mean().reset_index())

monthly_program_attendance["attendance_rate"] = monthly_program_attendance["attended"] * 100
print(monthly_program_attendance.head())

## Plot monthly attendance per program
plt.figure()

for program in monthly_program_attendance["program_name"].unique():
    program_data = monthly_program_attendance[
        monthly_program_attendance["program_name"] == program
    ]
    plt.plot(
        program_data["attendance_month"],
        program_data["attendance_rate"],
        label=program
    )

plt.title("Monthly Attendance Trend by Program")
plt.xlabel("Month")
plt.ylabel("Attendance Rate (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()

## Insights:
##	There are various high and low points for each program thorughout the year.
##	After School Care curves downward and back up to show kids being out of school in the summer months and attending the new school year
##	Youth Sports stays relatively high during summer which shows that children are participating in summer sport activities
##	Summer camp has it's lowest point in April and spikes up in May. This shows parents registering their children for summer camp after the end of the school year.
##	These different variations indicate seasonal effects on engagement

# ============================================
# 4. Retention Analysis
## Calculate first and last attendance per participant
retention = (
    df.groupby("participant_id").agg(
        enrollment_date=("enrollment_date", "first"),
        first_attendance=("attendance_date", "min"),
        last_attendance=("attendance_date", "max")
    )
    .reset_index()
)

## Calculate retetnion duration in days
retention["retention_days"] = (
    retention["last_attendance"] - retention["first_attendance"]
    ).dt.days

print(retention.head())

## Summary stats
print(retention["retention_days"].describe())

## Plot retention
plt.figure()
plt.hist(retention["retention_days"], bins=20)
plt.title("Distribution of Participant Retention (Days)")
plt.xlabel("Days Active")
plt.ylabel("Number of Participants")
plt.tight_layout()

plt.show()

## Merge program info
participant_program = (
    df.groupby("participant_id")["program_name"]
    .first()
    .reset_index()
)

retention = retention.merge(participant_program, on="participant_id")

## Average retention by program
program_retention = (
    retention.groupby("program_name")["retention_days"]
    .mean()
    .reset_index()
)

print(program_retention)

## Plot average retention by program
plt.figure()
plt.bar(
    program_retention["program_name"],
    program_retention["retention_days"]
)

plt.title("Average Participant Retention by Program")
plt.xlabel("Program")
plt.ylabel("Average Days Active")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Insights:
##	The program with the highest amount of participants is the After School Care, followed by Arts & Crafts
##	This can mean that there is more engagement in these programs compared to the rest.
##	Programs that have a shorter duration (such as STEM) show to have a lower retention
##	Although Youth Sports and Summer Camp and more seasonal, these have high retention. This can mean that there is more engagement for the children.

# ============================================
# 6. Insights
#==================================
# Summary
# ================================
# This analysis examined youth program participation and retention data
# to identify engagement trends and program performance
#
# Key findings:
# - Certain program sdemonstrated consistently higher attendance rates,
# indicating stronger participant engagement.
# - Attendance patterns showed seasonal variation, particularly during the
# beginning and end of the summer months, as well as the beginning and end
# of the school years
# - Retention analysis revealed that some programs retained participants
# significiantly longer than others, highlighting opportunities to
# improve engagement strategies for lower-retention programs.
#
# These insights could be used by program leadership to optimize
# scheduling, resource allocation, and participant retention efforts.