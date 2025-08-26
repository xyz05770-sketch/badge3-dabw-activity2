import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":briefcase: Employee Management Portal :briefcase:")
st.write("Manage your employee records efficiently.")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("employee_crud.public.employee").select(col('ID'), col('FirstName'), col('LastName'), col('DOB'), col('Gender'), col('Department'), col('Salary'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
