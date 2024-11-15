import GS_Coding_Exercise as gs
from openpyxl import load_workbook
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# Load a copy of input data from the GS_Coding_Exercise module
data = gs.get_input_data().copy()

def add_row(input_data, country, client_names, product_type, notional_traded):
    """Add a new row with specified client data to the input DataFrame."""
    new_row = pd.DataFrame([{
        'country': country, 
        'client_names': client_names,
        'product_type': product_type, 
        'notional_traded': notional_traded
    }])
    # Concatenate the new row to the input DataFrame and return the updated DataFrame
    return pd.concat([input_data, new_row], ignore_index=True)

def delete_row(input_data, country, client_names, product_type, notional_traded):
    """Delete a row that matches specified client data from the input DataFrame."""
    # Filter rows that match the specified conditions
    client = input_data[
        (input_data['country'] == country) &
        (input_data['client_names'] == client_names) &
        (input_data['product_type'] == product_type) &
        (input_data['notional_traded'] == notional_traded)
    ]
    # Return the matching client row(s) and the updated DataFrame with the row(s) removed
    return client, input_data.drop(client.index).reset_index(drop=True)

def plot_histogram(output_df, group_by):
    """Group data by specified column and return the total notional traded for each group."""
    grouped_data = output_df.groupby(group_by)['notional_traded'].sum().reset_index()
    # Rename the column for clarity in visualization
    grouped_data = grouped_data.rename(columns={'notional_traded': 'Total Notional Traded'})
    return grouped_data

def clear_all():
    """Clear all data by returning a DataFrame with empty fields for all columns."""
    df = pd.DataFrame([{
        'country': None, 
        'client_names': None,
        'product_type': None, 
        'notional_traded': None
    }])
    return df

def reset():
    """Reset data by returning a fresh copy of the original data loaded from GS_Coding_Exercise."""
    return data

def save_data(data, input_output, excel_path="Coding_Exercise.xlsx"):
    """Save the DataFrame to the specified sheet in an Excel file and adjust column layout."""
    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        # Write data to specified sheet in Excel without the index
        data.to_excel(writer, sheet_name=input_output, index=False)
    # Adjust column layout for better readability
    data_layout(excel_path)

def data_layout(excel_path):
    """Auto-fit column widths in all sheets of the workbook based on maximum data length."""
    workbook = load_workbook(excel_path)
    # Iterate over all worksheets to adjust column widths
    for worksheet in workbook.worksheets:
        for column_cells in worksheet.columns:
            # Determine max length of content in each column for proper sizing
            max_length = max(len(str(cell.value)) for cell in column_cells if cell.value is not None)
            adjusted_width = max_length + 2  # Add padding for readability
            worksheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width
    # Save workbook with adjusted column widths for all worksheets
    workbook.save(excel_path)
