import streamlit as st
from location import get_lat_long
from table import submit_complaint, fetch_complaints, recreate_db


def display_complaint_form():
    # Address input first
    address = st.text_input("Enter your address:")

    # Initialize latitude and longitude
    latitude, longitude = None, None
    location = None

    if address:
        # Get latitude and longitude from the address
        latitude, longitude = get_lat_long(address)
        location = address  # Store the address as the location

    # If address is not provided, allow latitude and longitude input
    if latitude is None or longitude is None:
        location = st.text_input("Or enter your location (latitude, longitude):", "37.7749, -122.4194")
        if location:
            latitude, longitude = map(float, location.split(','))
        else:
            latitude = 37.7749  # Default latitude
            longitude = -122.4194  # Default longitude

    # Complaint submission form
    with st.form(key='complaint_form'):
        subject = st.text_input("Subject", max_chars=100)  # Subject input
        description = st.text_area("Complaint Description")
        image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        submit_button = st.form_submit_button("Submit Complaint")

        if submit_button:
            if not subject:
                st.error("Subject is required!")
            elif not description:
                st.error("Description is required!")
            else:
                image_data = image.read() if image else None
                submit_complaint(subject, description, image_data, location, latitude, longitude)
                st.success("Complaint submitted successfully!")


def display_complaints():
    refresh_complaints()  # Fetch the latest data and update the display
    # Display the complaints
    if 'complaints_df' in st.session_state:
        complaints_df = st.session_state.complaints_df
    else:
        complaints_df = fetch_complaints()  # Initial fetch
        st.session_state.complaints_df = complaints_df  # Store in session state

    if not complaints_df.empty:
        st.write(complaints_df)
        st.map(complaints_df[['latitude', 'longitude']])
    else:
        st.write("No complaints found.")

    refresh_complaints()  # Fetch the latest data and update the display


def refresh_complaints():
    """Function to refresh the complaints table."""
    complaints_df = fetch_complaints()  # Fetch the latest data
    st.session_state.complaints_df = complaints_df  # Store in session state
    # st.success("Complaints refreshed!")


def display_refresh_button():
    """Display a button to refresh the complaints table."""
    if st.button("Refresh Complaints Table"):
        refresh_complaints()  # Call the refresh function
        st.success("Complaints refreshed!")
        display_complaints()  # Display the updated complaints


def display_recreate_button():
    if st.button("Delete and Recreate Complaints Table"):
        recreate_db()  # Call the function to recreate the database
        st.success("Complaints table deleted and recreated successfully!")

        # Automatically refresh the complaints list
        refresh_complaints()  # Fetch the latest data and update the display