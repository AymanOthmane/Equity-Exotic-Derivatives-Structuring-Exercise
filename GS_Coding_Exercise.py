import pandas as pd

excel_path = "Coding_Exercise.xlsx"

def get_input_data(excel_path=None):
    """Retrieve data from the 'input' sheet in the specified Excel file or use sample data if no file is provided."""
    if excel_path is None:
        input_df = pd.DataFrame({
            'country': ['USA', 'USA', 'USA', 'Canada', 'Canada', 'Canada', 'France', 'Italy'],
            'client_names': ['Client U', 'Client S', 'Client S', 'Client C', 'Client A', 'Client C', 'Client F', 'Client I'],
            'product_type': ['Stocks', 'Stocks', 'Bonds', 'FX', 'Credit', 'Bonds', 'FX', 'Bonds'],
            'notional_traded': [1000, 2000, 1500, 3000, 1200, 2500, 4500, 10000]
        })
    else:
        input_df = pd.read_excel(excel_path, sheet_name='input')
    return input_df

def aggregate_data(input_df):
    """Aggregate notional traded by country and client names, with non-repeating country names."""
    # Perform the aggregation
    output_df = input_df.groupby(['country', 'client_names'])['notional_traded'].sum().reset_index()
    # Replace subsequent occurrences of each country with an empty string
    output_df['country'] = output_df['country'].where(output_df['country'].ne(output_df['country'].shift()))
    output_df['country'] = output_df['country'].fillna('')
    return output_df

def main():
    """Main function to handle reading, processing, and saving aggregated data."""
    input_df = get_input_data(excel_path)
    output_df = aggregate_data(input_df)

    # Write to "output" sheet in the same Excel file
    with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        output_df.to_excel(writer, sheet_name='output', index=False)
    print(output_df)
    return output_df

if __name__ == "__main__":
    main()
