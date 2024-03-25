import pandas as pd

def extract_columns_from_csv(file_path, output_file_path):
    """
    Extracts specific columns from a CSV file and saves them into another CSV file.

    Parameters:
    file_path (str): The path to the input CSV file.
    output_file_path (str): The path to the output CSV file.
    """
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract the required columns
    extracted_df = df[['well_tag_number', 'distance_geocode', 'distance_to_matching_pid', 
                       'score_address', 'score_city', 'xref_ind', 'nr_region_name']]

    # Save the extracted data to a new CSV file
    extracted_df.to_csv(output_file_path, index=False)

    print(f"Extracted data saved to {output_file_path}")


file_path = 'gwells_locationqa.csv'
output_file_path = 'qaqc_well_data.csv' # Output file path
extract_columns_from_csv(file_path, output_file_path)
