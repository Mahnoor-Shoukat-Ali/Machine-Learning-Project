import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("HR Management System")

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{API_URL}/token", data={"username": username, "password": password})
        if response.status_code == 200:
            token = response.json()["access_token"]
            st.session_state["token"] = token
            st.success("Logged in successfully")
        else:
            st.error("Invalid username or password")

def send_notification():
    st.subheader("Send Notification")
    content = st.text_area("Content")
    if st.button("Send"):
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.post(f"{API_URL}/notifications/", json={"content": content}, headers=headers)
        if response.status_code == 200:
            st.success("Notification sent")
        else:
            st.error("Failed to send notification")

def view_notifications():
    st.subheader("View Notifications")
    headers = {"Authorization": f"Bearer {st.session_state['token']}"}
    response = requests.get(f"{API_URL}/notifications/", headers=headers)
    if response.status_code == 200:
        notifications = response.json()
        for notification in notifications:
            st.write(notification["content"])
    else:
        st.error("Failed to fetch notifications")

if "token" not in st.session_state:
    login()
else:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.pop("token"))
    send_notification()
    view_notifications()
