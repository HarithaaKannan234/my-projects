import streamlit as st
import easyocr
from PIL import Image
import pandas as pd
import io
import numpy as np
from sqlalchemy import create_engine, text
import re

# Replace these with your PostgreSQL credentials
postgres_user = 'postgres'
postgres_password = 'Sukan%4001'
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db = 'bisx'
table_name = 'bisx_details'

# Create a PostgreSQL connection
engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}')

def extracted_data(result_text):
    ext_data = {'Name': [], 'Designation': [], 'Company name': [], 'Contact': [], 'Email': [], 'Website': [],
                'Address': [], 'Pincode': []}
    if not result_text:
        return ext_data
    ext_data['Name'].append(result_text[0])
    ext_data['Designation'].append(result_text[1])
    for i in range(2, len(result_text)):
        if (result_text[i].startswith('+')) or (result_text[i].replace('-', '').isdigit() and '-' in result_text[i]):
            ext_data['Contact'].append(result_text[i])
        elif '@' in result_text[i] and '.com' in result_text[i]:
            small = result_text[i].lower()
            ext_data['Email'].append(small)
        elif 'www' in result_text[i] or 'WWW' in result_text[i] or 'wwW' in result_text[i]:
            small = result_text[i].lower()
            ext_data['Website'].append(small)
        elif 'TamilNadu' in result_text[i] or 'Tamil Nadu' in result_text[i] or result_text[i].isdigit():
            ext_data['Pincode'].append(result_text[i])
        elif re.match(r'^[A-Za-z]', result_text[i]):
            ext_data['Company name'].append(result_text[i])
        else:
            removed_colon = re.sub(r'[,;]', '', result_text[i])
            ext_data['Address'].append(removed_colon)
    for key, value in ext_data.items():
        if len(value) > 0:
            concatenated_string = ' '.join(value)
            ext_data[key] = [concatenated_string]
        else:
            value = 'NA'
            ext_data[key] = [value]

    return ext_data

def read_text(image):
    reader = easyocr.Reader(['en'], model_storage_directory='.')
    result = reader.readtext(image, detail=0)
    return result

def read_uploaded_image():
    image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if image is not None:
        # Use PIL to open the image
        img = Image.open(image)
        st.image(img, caption="Uploaded Image", use_column_width=True)
        return img
    else:
        st.warning("Please upload an image.")
        return None

def upload_and_extract_tab():
    st.title('Upload and Extract')
    uploaded_image = read_uploaded_image()
    if uploaded_image is not None:
        image_np = np.array(uploaded_image)
        result_text = read_text(image_np)
       
        ext_data = extracted_data(result_text)

        # Create a DataFrame for extracted data
        extracted_df = pd.DataFrame(ext_data)

        # Display extracted data DataFrame
        for col in extracted_df.columns:
            edited_value = st.text_input(f"Edit {col}", extracted_df[col][0])
            extracted_df[col] = [edited_value]

        # Display the updated DataFrame
        st.write("Updated Data:")
        st.dataframe(extracted_df)
        if st.button("Save to PostgreSQL"):
            save_to_postgres(extracted_df)

def save_to_postgres(dataframe):
    # Check if the data already exists in the database
    conditions = []
    for col in dataframe.columns:
        # Use double quotes to handle column names with spaces or reserved keywords
        conditions.append(f'"{col}" = \'{dataframe[col][0]}\'')
    where_clause = " AND ".join(conditions)
    existing_data_query = text(f'SELECT * FROM "{table_name}" WHERE {where_clause}')

    connection = engine.connect()
    existing_data_result = connection.execute(existing_data_query)
    existing_data = existing_data_result.fetchall()
    connection.close()

    if not existing_data:
        # Data doesn't exist, save DataFrame to PostgreSQL
        dataframe.to_sql(table_name, engine, if_exists='append', index=False)
        st.success("Data saved to PostgreSQL!")
    else:
        st.warning("Data already exists in the database. Cannot save duplicate data.")

def edit_and_add_tab(engine):
    connection = engine.connect()
    query = text(f"SELECT * FROM {table_name}")
    result = connection.execute(query)
    data_from_db = result.fetchall()
    connection.close()

    # Display the data in a DataFrame
    data_df = pd.DataFrame(data_from_db, columns=['Name', 'Designation', 'Company name', 'Contact', 'Email', 'Website', 'Address', 'Pincode'])

    # Display the DataFrame before selecting delete or update
    st.write("Original Data:")
    st.dataframe(data_df)

    # Use a dictionary to store the updated values
    updated_values = {}

    for index, row in data_df.iterrows():
        delete_button = st.button(f"Delete {row['Name']}")
        update_button = st.button(f"Update {row['Name']}")

        if delete_button:
            delete_from_db(row['Name'])
            st.success(f"Deleted {row['Name']} from the database!")

        if update_button:
            # Display editable fields for update
            updated_name = st.text_input("Name", row['Name'])
            updated_designation = st.text_input("Designation", row['Designation'])
            updated_company_name = st.text_input("Company name", row['Company name'])
            updated_contact = st.text_input("Contact", row['Contact'])
            updated_email = st.text_input("Email", row['Email'])
            updated_website = st.text_input("Website", row['Website'])
            updated_address = st.text_input("Address", row['Address'])
            updated_pincode = st.text_input("Pincode", row['Pincode'])

            # Store updated values in the dictionary
            updated_values[index] = {
                'Name': updated_name,
                'Designation': updated_designation,
                'Company name': updated_company_name,
                'Contact': updated_contact,
                'Email': updated_email,
                'Website': updated_website,
                'Address': updated_address,
                'Pincode': updated_pincode
            }

    # Process the updates after iterating through the entire DataFrame
    for index, updated_data in updated_values.items():
        update_to_db(
            row['Name'],
            updated_data['Name'],
            updated_data['Designation'],
            updated_data['Company name'],
            updated_data['Contact'],
            updated_data['Email'],
            updated_data['Website'],
            updated_data['Address'],
            updated_data['Pincode']
        )
        st.success(f"Updated {row['Name']} in the database!")

def update_to_db(old_name, new_name, new_designation, new_company_name, new_contact, new_email, new_website, new_address, new_pincode):
    connection = engine.connect()

    # Execute the UPDATE query
    update_query = text(f"UPDATE {table_name} SET \"Name\" = :new_name, \"Designation\" = :new_designation, "
                        f"\"Company name\" = :new_company_name, \"Contact\" = :new_contact, \"Email\" = :new_email, "
                        f"\"Website\" = :new_website, \"Address\" = :new_address, \"Pincode\" = :new_pincode "
                        f"WHERE \"Name\" = :old_name")

    # Bind parameters to the query
    params = {
        'old_name': old_name,
        'new_name': new_name,
        'new_designation': new_designation,
        'new_company_name': new_company_name,
        'new_contact': new_contact,
        'new_email': new_email,
        'new_website': new_website,
        'new_address': new_address,
        'new_pincode': new_pincode
    }

    connection.execute(update_query, params)
    connection.commit()
    connection.close()

def delete_from_db(name):
    print(f"Deleting record with Name: {name}")
    connection = engine.connect()
    delete_query = text(f"DELETE FROM {table_name} WHERE \"Name\" = '{name}'")
    print(f"Executing query: {delete_query}")
    connection.execute(delete_query)
    connection.commit() 
    connection.close()

def view_dataframes_tab():
    st.title("View Dataframes")

tab1, tab2= st.tabs(["Upload", "Edit"])
with tab1:
    upload_and_extract_tab()
with tab2:
    edit_and_add_tab(engine)

