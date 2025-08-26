import streamlit as st
from snowflake.snowpark.functions import col

st.title(":briefcase: Employee Management Portal")
st.write("Manage your employee records efficiently.")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("employee_crud.public.employee").select(
    col('ID'), col('FirstName'), col('LastName'), col('DOB'),
    col('Gender'), col('Department'), col('Salary')
)

# Use st.toggle for true toggle UI/UX
show_table = st.toggle(
    "Click to Hide" if st.session_state.get("show_table", False) else "Click to View",
    value=st.session_state.get("show_table", False),
    key="show_table"
)

if show_table:
    st.dataframe(data=my_dataframe, use_container_width=True)