import json
from prettytable import PrettyTable
from execute import print_in_color

def display_log_data(file_path='my_logs.json'):
    """
    Reads a JSON log file, displays the contents in a formatted table using PrettyTable,
    and prints out the summary statistics of task statuses.
    
    :param file_path: Path to the JSON log file.
    """
    try:
        # Open the file and load the data
        with open(file_path, 'r') as file:
            logs = json.load(file)
    except FileNotFoundError:
        print_in_color("No log file found. Please make sure the log data has been created.", "\033[31m")
        return
    except json.JSONDecodeError:
        print_in_color("Error reading the log file. Please check the file format.", "\033[31m")
        return
    
    # Create a PrettyTable object with headers
    table = PrettyTable()
    table.field_names = ["WalletAddr","CompletedTime", "TrainRuntime", "Status"]

    total_tasks = len(logs)
    success_count = 0
    fail_count = 0

    # Add each log entry to the table and count statuses
    for entry in logs:
        table.add_row([entry['WalletAddr'],entry['CompletedTime'], entry['TrainRuntime'], entry['Status']])
        if entry['Status'].lower() == "success":
            success_count += 1
        elif entry['Status'].lower() == "failed":
            fail_count += 1
    nim_expected = success_count * 3
    # Print the table
    print_in_color(table, "\033[97m")
    print_in_color(f"Total tasks: {total_tasks}, Tasks successful: {success_count}, Tasks failed: {fail_count}, Rewards Expected: {nim_expected} $NIM", "\033[32m")

# Example usage:
display_log_data()
