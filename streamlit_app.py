import streamlit as st
from snowflake.snowpark.functions import col
import datetime

st.title(":briefcase: Employee Management Portal")
st.write("Manage your employee records efficiently.")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("employee_crud.public.employee")\
    .select(
        col('ID'), col('FirstName'), col('LastName'), col('DOB'),
        col('Gender'), col('Department'), col('Salary')
    )\
    .order_by(col("ID"))

# For Max calc -> Snowpark dataframe to pandas
my_dataframe_pd = my_dataframe.to_pandas()

show_table = st.toggle(
    "Click to Hide Employee Table" if st.session_state.get("show_table", False) else "Click to View Employee Table",
    value=st.session_state.get("show_table", False),
    key="show_table"
)

if show_table:
    st.dataframe(data=my_dataframe, use_container_width=True)

crud_operations = st.multiselect(
    "Select Operation",
    options=["Add Employee Details", "Update Employee Details", "Delete Employee Details"],
    max_selections=1
)

if crud_operations:
    st.write(f"You selected: {crud_operations[0]}")

    if crud_operations[0] == "Add Employee Details":
        with st.form("add_employee_form"):
            st.subheader("Add New Employee")

            current_id = my_dataframe_pd['ID'].max() + 1
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
            dob = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1))
            gender = st.selectbox("Gender", options=["Male", "Female", "Other"])
            department = st.selectbox("Department", options=["HR", "Engineering", "Sales", "Marketing", "Finance", "IT"])
            salary = st.number_input("Salary", min_value=0.0, format="%.2f")

            submitted = st.form_submit_button("Add Employee")
            if submitted:
                my_insert_stmt = (
                    "insert into employee_crud.public.employee (ID, FirstName, LastName, DOB, Gender, Department, Salary) "
                    "values (" + str(int(current_id)) + ", '" + first_name + "', '" + last_name + "', '" + str(dob) + "', '" + gender + "', '" + department + "', " + str(float(salary)) + ")"
                )
                session.sql(my_insert_stmt).collect()
                st.success("Employee added successfully!")
    
    elif crud_operations[0] == "Update Employee Details":
        st.write("Select attribute(s) to update:")
        attributes = ["First Name", "Last Name", "DOB", "Gender", "Department", "Salary"]
        selected_attributes = st.multiselect("Attributes", options=attributes)

        if selected_attributes:
            st.write("Update values for selected attributes:")
            updated_values = {}
            current_id = my_dataframe_pd['ID'].max() + 1
            for attr in selected_attributes:
                if attr == "DOB":
                    updated_values[attr] = str(st.date_input(attr, value=datetime.date(2000, 1, 1)))
                elif attr == "Salary":
                    updated_values[attr] = float(st.number_input(attr, min_value=0.0, format="%.2f"))
                else:
                    updated_values[attr] = st.text_input(attr)

            if st.button("Update Employee"):
                update_stmt = f"""
                UPDATE employee_crud.public.employee
                SET {', '.join([f"{k} = '{v}'" for k, v in updated_values.items()])}
                WHERE ID = {current_id}
                """
                st.write(update_stmt)
                st.stop()
                # session.sql(update_stmt).collect()
                # st.success("Employee updated successfully!")

