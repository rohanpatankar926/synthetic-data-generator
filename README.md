# Synthetic Data Generator

This project is a synthetic data generator built with Streamlit. It allows users to upload a CSV file defining the structure of the data they need, and then generates synthetic data based on that structure. The generator supports various data types and ensures that primary key columns have unique values.

## Features

- **Upload CSV Schema**: Define the structure of the data using a CSV file.
- **Select Columns**: Choose which columns to generate synthetic data for.
- **Generate Synthetic Data**: Create synthetic data based on the selected columns and data types.
- **Download Synthetic Data**: Download the generated synthetic data as a CSV file.

## Supported Data Types

- **varchar** or **char**: Generates random text.
- **decimal**: Generates random decimal numbers with specified precision and scale.
- **int**: Generates random integers with a specified number of digits.
- **date**: Generates random dates.
- **datetime**: Generates random date and time values.
- **timestamp**: Generates random timestamps.
- **category**: Generates random values from a provided list of categories.
- **boolean**: Generates random boolean values.

## Primary Key Handling

- **Primary Key**: The `primary_key` column in the schema CSV indicates which column should be the primary key. The generator ensures that this column has unique values:
  - **Category or Boolean**: Generates a counter.
  - **Varchar or Char**: Uses a base string from the `values` column, followed by a counter.
  - **Decimal or Int**: Uses a base value from the `values` column and increments it.
  - **Date, Datetime, or Timestamp**: Uses a base date from the `values` column and increments it by days.

## CSV Schema Format

The input CSV file should have the following columns:

- `names`: The name of the column.
- `type`: The data type of the column (e.g., `varchar(255)`, `int(10)`, `decimal(5,2)`, `date`, `datetime`, `timestamp`, `category`, `boolean`).
- `values`: A comma-separated list of values for categorical data, or a base value for other types.
- `primary_key`: Set to `true` for the primary key column, otherwise `false`.

## Example CSV Schema

```csv
names,type,values,primary_key
id,int(10),,true
name,varchar(255),,false
age,int(2),,false
salary,decimal(10,2),,false
hire_date,date,1970-01-01,false
status,category,active,inactive,pending,false
is_manager,boolean,,false
```
## How to run
```
pip install pandas faker streamlit
streamlit run data_generator.py
```
