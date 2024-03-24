import streamlit as st
import pandas as pd

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

    # Initialize lists to store deadlines and profits of selected jobs
    selected_deadlines = []
    selected_profits = []

    # Iterate through jobs
    for i in range(len(df)):
        # Find a time slot before or at the deadline
        for j in range(min(df['deadline'].iloc[i] - 1, max_deadline - 1), -1, -1):
            if not time_slots[j]:
                # Assign job to the time slot
                time_slots[j] = True
                sequence.append(df['jobID'].iloc[i])
                total_profit += df['profit'].iloc[i]
                selected_deadlines.append(df['deadline'].iloc[i])
                selected_profits.append(df['profit'].iloc[i])
                break
        else:
            continue  # No available time slot found
        # If no available time slot is found before the deadline, skip the job

    return sequence, total_profit, selected_deadlines, selected_profits

# Streamlit app
def main():
    st.title("Job Sequencing with Streamlit")
    
    # Display sample data
    st.subheader("Sample Data")
    st.write(df)

    # Perform job sequencing
    sequence, total_profit, selected_deadlines, selected_profits = job_sequencing(df)

    # Display results
    st.subheader("Job Sequence")
    st.write(sequence)
    st.subheader("Total Profit")
    st.write(total_profit)

    # Visualization of selected jobs
    st.subheader("Visualization of Selected Jobs")
    selected_jobs_df = pd.DataFrame({'Job ID': sequence, 'Profit': selected_profits, 'Deadline': selected_deadlines})
    st.bar_chart(selected_jobs_df.set_index('Job ID')['Profit'])
    st.line_chart(selected_jobs_df.set_index('Job ID')['Deadline'])

if __name__ == "__main__":
    main()

