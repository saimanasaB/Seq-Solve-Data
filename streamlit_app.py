import streamlit as st
import pandas as pd
import altair as alt

# Sample data
data = pd.read_csv('jobs.csv')

# Create DataFrame
df = pd.DataFrame(data)

def job_sequencing(df):
    # Sort jobs by profit in descending order
    df = df.sort_values(by='profit', ascending=False)

    # Initialize empty sequence and profits
    sequence = []
    total_profit = 0

    # Initialize time slots
    max_deadline = max(df['deadline'])
    time_slots = [False] * max_deadline

    # Iterate through jobs
    for i in range(len(df)):
        # Find a time slot before or at the deadline
        for j in range(min(df['deadline'].iloc[i] - 1, max_deadline - 1), -1, -1):
            if not time_slots[j]:
                # Assign job to the time slot
                time_slots[j] = True
                sequence.append(df['jobID'].iloc[i])
                total_profit += df['profit'].iloc[i]
                break
        else:
            continue  # No available time slot found
        # If no available time slot is found before the deadline, skip the job

    return sequence, total_profit

# Streamlit app
def main():
    st.title("Job Sequencing with Streamlit")
    
    # Display sample data
    st.subheader("Sample Data")
    st.write(df)

    # Perform job sequencing
    sequence, total_profit = job_sequencing(df)

    # Display results
    st.subheader("Job Sequence")
    st.write(sequence)
    st.subheader("Total Profit")
    st.write(total_profit)

    # Visualize selected jobs with deadlines and profits
    selected_jobs = df[df['jobID'].isin(sequence)]
    selected_jobs_chart = alt.Chart(selected_jobs).mark_circle(size=100).encode(
        x='deadline',
        y='profit',
        color='jobID:N',
        tooltip=['jobID', 'deadline', 'profit']
    ).properties(
        title='Selected Jobs with Deadlines and Profits'
    ).interactive()

    st.altair_chart(selected_jobs_chart, use_container_width=True)

if __name__ == "__main__":
    main()
