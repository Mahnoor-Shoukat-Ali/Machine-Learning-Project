import streamlit as st
import requests

API_URL = "http://localhost:8000"

def fetch_todos():
    response = requests.get(f"{API_URL}/todos/")
    return response.json()

def create_todo():
    title = st.text_input("Title")
    description = st.text_area("Description")
    if st.button("Add Todo"):
        response = requests.post(
            f"{API_URL}/todos/", 
            json={"title": title, "description": description}
        )
        if response.status_code == 200:
            st.success("Added in list successfully")
        else:
            st.error("Error adding todo")

def delete_todo():
    todo_id = st.number_input("Todo ID to delete", min_value=1)
    if st.button("Delete Todo"):
        response = requests.delete(f"{API_URL}/todos/{todo_id}")
        if response.status_code == 200:
            st.success("Todo deleted successfully")
        else:
            st.error("Error deleting todo")

def main():
    st.title("Mahnoor Shoukat NED University")
    st.title("ToDo App")
    
    menu = ["View Todos", "Add Todo", "Delete Todo"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "View Todos":
        todos = fetch_todos()
        for todo in todos:
            st.write(f"ID: {todo['id']}, Title: {todo['title']}, Description: {todo['description']}")
    elif choice == "Add Todo":
        create_todo()
    elif choice == "Delete Todo":
        delete_todo()

if __name__ == "__main__":
    main()
