import streamlit as st
import pandas as pd 
import plotly.express as px
from db_fn import *

def main():
    st.title("To Do")
    menu = ["Add", "View", "Edit", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_table()
    if choice == "Add":
        st.subheader("Add a task")

        col1, col2 = st.columns(2)

        with col1:
            task = st.text_area("Task To Do")
        with col2:
            status = st.selectbox("Status", ["To Do", "In Progress", "Complete"])
            due_date = st.date_input("Due Date")

        if st.button("Add Task"):
            add_data(task,status,due_date)
            st.success(f"Successfully added task: {task}")

    elif choice == "View":
        st.subheader("View all your tasks")
        result = view_all_data()
        df = pd.DataFrame(result,columns=['Task','Status','Due Date'])
        st.dataframe(df)
        
        with st.expander("Task Status"):
            task_df = df['Status'].value_counts().to_frame()
            stat = task_df.reset_index()
            stat.columns = ['Status','Tasks']
            st.dataframe(stat)

            pi = px.pie(stat,names='Status',values='Tasks')
            st.plotly_chart(pi)
            


    elif choice == "Edit":
        st.subheader("Edit your tasks")
        
        #st.write(view_unique_task())
        list_of_tasks = [i[0] for i in view_unique_task()]
        #st.write(list_of_tasks)

        selected_task = st.selectbox("Task To Edit",list_of_tasks)

        selected_result = get_task(selected_task)
        #st.write(selected_result)
        if selected_result:
            task = selected_result[0][0]
            status = selected_result[0][1]
            due_date = selected_result[0][2]

            col1, col2 = st.columns(2)

        with col1:
            new_task = st.text_area("Task To Do",task)
        with col2:
            new_status = st.selectbox(status, ["To Do", "In Progress", "Complete"])
            new_due_date = st.date_input(due_date)

        if st.button("Edit Task"):
            edit_task(new_task,new_status,new_due_date,task,status,due_date)
            st.success(f"Successfully edited {task} to {new_task}")
            
        result2 = view_all_data()
        df2 = pd.DataFrame(result2,columns=['Task','Status','Due Date'])
        with st.expander("Edited Tasks"):
            st.dataframe(df2)
    


    elif choice == "Delete":
        st.subheader("Delete a task")

        list_of_tasks = [i[0] for i in view_unique_task()]

        selected_task = st.selectbox("Task To Delete",list_of_tasks)
        st.warning(f"Are you sure you want to delete {selected_task}?")
        if st.button("Delete Task"):
            delete_data(selected_task)
            st.success(f"Task {selected_task} has been successfully deleted")

        new_result = view_all_data()
        new_df = pd.DataFrame(new_result,columns=['Task','Status','Due Date'])
        with st.expander("Updated Task List"):
            st.dataframe(new_df)

                

if __name__ == '__main__':
    main()