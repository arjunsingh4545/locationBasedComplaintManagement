import streamlit as st
from website import display_complaint_form, display_complaints,  display_refresh_button
from table import init_db

def main():
    # Initialize the database
    init_db()

    # Streamlit application title
    st.title("Location-Based Complaint System")

    # Display the complaint submission form
    display_complaint_form()

    # Display the button to delete and recreate the table
   # display_recreate_button()

    # Display the button to refresh the complaints table
    display_refresh_button()

    # Display the list of complaints
    st.subheader("Complaints List")
    display_complaints()  # Call to display the complaints

if __name__ == "__main__":
    main()