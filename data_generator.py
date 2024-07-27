import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import streamlit as st

fake = Faker()

def generate_synthetic_data(input_df, selected_columns, num_rows):
    synthetic_data = pd.DataFrame()
    primary_key_column = None

    for index, row in input_df.iterrows():
        name = row['names']
        if name not in selected_columns:
            continue

        dtype = row['type']
        value = row['values']
        is_primary_key = row.get('primary_key', False)

        if is_primary_key:
            primary_key_column = name

        if 'varchar' in dtype or 'char' in dtype:
            length = int(''.join(filter(str.isdigit, dtype)))
            synthetic_data[name] = [fake.text(max_nb_chars=length).strip() for _ in range(num_rows)]
        elif 'decimal' in dtype:
            precision, scale = map(int, dtype[dtype.find('(') + 1:dtype.find(')')].split(','))
            synthetic_data[name] = [round(random.uniform(1, 10**precision), scale) for _ in range(num_rows)]
        elif 'int' in dtype:
            digits = int(dtype[dtype.find('(') + 1:dtype.find(')')])
            synthetic_data[name] = [random.randint(10**(digits-1), 10**digits - 1) for _ in range(num_rows)]
        elif 'date' in dtype or 'datetime' in dtype or 'timestamp' in dtype:
            if value:
                try:
                    start_date = datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    start_date = datetime(1970, 1, 1)
            else:
                start_date = datetime(1970, 1, 1)
                
            end_date = datetime.now()
            delta = end_date - start_date
            
            if 'date' in dtype:
                synthetic_data[name] = [start_date + timedelta(days=random.randint(0, delta.days)) for _ in range(num_rows)]
            else:
                synthetic_data[name] = [start_date + timedelta(seconds=random.randint(0, int(delta.total_seconds()))) for _ in range(num_rows)]
        elif 'category' in dtype:
            categories = value.split(',')
            synthetic_data[name] = [random.choice(categories) for _ in range(num_rows)]
        elif 'boolean' in dtype:
            synthetic_data[name] = [random.choice([True, False]) for _ in range(num_rows)]
        else:
            categories = value.split(',')
            synthetic_data[name] = [random.choice(categories) for _ in range(num_rows)]
    
    if primary_key_column:
        dtype = input_df.loc[input_df['names'] == primary_key_column, 'type'].values[0]
        value = input_df.loc[input_df['names'] == primary_key_column, 'values'].values[0]
        
        if 'category' in dtype or 'boolean' in dtype:
            synthetic_data[primary_key_column] = range(1, num_rows + 1)
        elif 'varchar' in dtype or 'char' in dtype:
            length = int(''.join(filter(str.isdigit, dtype)))
            base_str = value[:length] if value else 'PK'
            synthetic_data[primary_key_column] = [f"{base_str}{i}" for i in range(1, num_rows + 1)]
        elif 'decimal' in dtype or 'int' in dtype:
            if value:
                base_value = int(value)
            else:
                base_value = 1
            synthetic_data[primary_key_column] = [base_value + i for i in range(num_rows)]
        elif 'date' in dtype or 'datetime' in dtype or 'timestamp' in dtype:
            if value:
                try:
                    base_date = datetime.strptime(value, '%Y-%m-%d')
                except ValueError:
                    base_date = datetime(1970, 1, 1)
            else:
                base_date = datetime(1970, 1, 1)
                
            synthetic_data[primary_key_column] = [base_date + timedelta(days=i) for i in range(num_rows)]

    return synthetic_data

st.title("Synthetic Data Generator")

uploaded_file = st.file_uploader("Upload your input CSV file", type=["csv"])

if uploaded_file:
    input_df = pd.read_csv(uploaded_file)
    st.subheader("Input DataFrame")
    st.dataframe(input_df)
    
    selected_columns = st.multiselect("Select columns to generate synthetic data for", input_df['names'].tolist())
    num_rows = st.number_input("Number of rows to generate", min_value=1, max_value=1000000, value=100)

    if st.button("Generate Synthetic Data"):
        synthetic_df = generate_synthetic_data(input_df, selected_columns, num_rows)
        st.subheader("Synthetic Data")
        st.dataframe(synthetic_df)

        csv = synthetic_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='synthetic_data.csv',
            mime='text/csv',
        )
else:
    st.info("Please upload an input CSV file to proceed.")
