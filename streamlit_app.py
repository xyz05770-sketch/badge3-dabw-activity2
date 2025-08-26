import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":briefcase: Employee Management Portal")
st.write("Manage your employee records efficiently.")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("employee_crud.public.employee").select(
    col('ID'), col('FirstName'), col('LastName'), col('DOB'),
    col('Gender'), col('Department'), col('Salary')
)

if "show_table" not in st.session_state:
    st.session_state.show_table = False

if st.button("Click to Hide" if st.session_state.show_table else "Click to View"):
    st.session_state.show_table = not st.session_state.show_table

if st.session_state.show_table:
    st.dataframe(data=my_dataframe, use_container_width=True)
