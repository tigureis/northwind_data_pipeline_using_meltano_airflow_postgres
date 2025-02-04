import os
import pandas as pd
from datetime import datetime

def merge_orders():
    
    # Get the current date as'yyyy-mm-dd')
    current_date = datetime.today().strftime('%Y-%m-%d')
    print(f"Current date: {current_date}")

    # Define the imput data folder paths
    orders_folder_path = f'/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/raw/orders/{current_date}/'
    order_details_folder_path = f'/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/raw/order_details/{current_date}/'

    # Build the full file paths
    orders_file_path = os.path.join(orders_folder_path, f'raw_public-orders_{current_date}.csv')
    order_details_file_path = os.path.join(order_details_folder_path, f'raw_order_details_{current_date}.csv')

    # Check if the directories and files exist. If they do not, raise an error with a detailed message.
    if not os.path.exists(orders_folder_path) or not os.path.exists(orders_file_path):
        raise FileNotFoundError(f"Could not find the file: {orders_file_path}. Please ensure the directory and file exist.")
    
    if not os.path.exists(order_details_folder_path) or not os.path.exists(order_details_file_path):
        raise FileNotFoundError(f"Could not find the file: {order_details_file_path}. Please ensure the directory and file exist.")

    # Load the data using pandas
    orders = pd.read_csv(orders_file_path)
    order_details = pd.read_csv(order_details_file_path)

    # Perform the join based on the 'order_id' field
    merged_data = pd.merge(orders, order_details, on='order_id', how='inner')

    # Define the output folder path to save the final file
    output_folder_path = f'/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/grouped/{current_date}/'

    # Create the output directory if it does not exist
    os.makedirs(output_folder_path, exist_ok=True)

    # Define the full path for the output file
    output_file_path = os.path.join(output_folder_path, f'order_merged_detail_{current_date}.csv')

    # Save the merged DataFrame as a CSV file
    merged_data.to_csv(output_file_path, index=False)
    print(f"File saved at: {output_file_path}")
