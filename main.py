# Graduate Software Engineer role at Cobblestone Energy | Dubai, United Arab Emirates
# Juan Manuel García Delgado | me@juanmagd.dev | https://juanmagd.dev | Sept 15 2024


# Required Libraries
import time
import os
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

try:
    import numpy as np
    import matplotlib.pyplot as plt
    print("All required libraries are installed.")
except ImportError as e:
    print(f"Library missing: {e}")


hours = 24 # Number of hours, perform a day
days = 30 # Number of days, perform a month    <- Change this value to simulate more days


def generate_transaction_number(std):
    """Create a list of transactions per hour for a day.

    This function simulates the number of transactions occurring each hour during a day. 
    The simulation takes into account a standard deviation (`std`) to add some variation 
    to the transaction numbers (noise).
    
    Args:
        std (float): Standard deviation used in the Gaussian distribution to introduce variability in the transaction counts.

    Returns:
        list: A list of 24 integers, each representing the number of transactions in a given hour of the day.
    """

    transactions_per_hour_laboral_days = [ 
        random.randint(3, 15) + abs(int(random.gauss(0, std))),    # 00:00
        random.randint(0, 10) + abs(int(random.gauss(0, std))),    # 01:00
        random.randint(1, 10) + abs(int(random.gauss(0, std))),    # 02:00
        random.randint(1, 10) + abs(int(random.gauss(0, std))),    # 03:00
        random.randint(2, 10) + abs(int(random.gauss(0, std))),    # 04:00
        random.randint(4, 10) + abs(int(random.gauss(0, std))),    # 05:00
        random.randint(10, 20) + abs(int(random.gauss(0, std))),   # 06:00
        random.randint(10, 30) + abs(int(random.gauss(0, std))),   # 07:00
        random.randint(20, 60) + abs(int(random.gauss(0, std))),   # 08:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 09:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 10:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 11:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 12:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 13:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 14:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 15:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 16:00
        random.randint(30, 100) + abs(int(random.gauss(0, std))),  # 17:00
        random.randint(20, 80) + abs(int(random.gauss(0, std))),   # 18:00
        random.randint(20, 60) + abs(int(random.gauss(0, std))),   # 19:00
        random.randint(20, 60) + abs(int(random.gauss(0, std))),   # 20:00
        random.randint(10, 40) + abs(int(random.gauss(0, std))),   # 21:00
        random.randint(10, 30) + abs(int(random.gauss(0, std))),   # 22:00
        random.randint(5, 20) + abs(int(random.gauss(0, std)))     # 23:00
     
    ] 
    
    return transactions_per_hour_laboral_days
  

def generate_transaction_value():
    """Generate a random transaction value based on a normal distribution.

    This function creates a transaction value using a normal distribution with a specified mean and standard deviation. 
    It ensures that the transaction value is not negative by taking the absolute value if the generated value is negative.
    We assume that the mean transaction value is 20,000 euros with a standard deviation of 50,000 euros. This is just for simulation purposes.
    We suppose most transaction are around 20,000 euros, but there are some transactions with higher values and some with lower values.

    Returns:
        float: A non-negative transaction value.
    """
    
    mean_value = 20000  # Mean value of the transactions
    std_deviation = 50000  # Standard deviation, adjusts the dispersion of values
    transaction_value = np.random.normal(mean_value, std_deviation)
    
    # Ensure the generated value is non-negative. If negative, return the absolute value
    return abs(transaction_value)


def simulate_day_transactions(day, std=2):
    """Simulate transactions for a given day.

    This function generates a map of transaction values for each hour of a specific day. It uses the `generate_transaction_number`
    function to determine the number of transactions per hour based.
    Then, for each hour, it generates the transaction values using `generate_transaction_value` and stores them in a dictionary.

    Args:
        day (int): The day number for which transactions are simulated.
        std (float, optional): The standard deviation used to generate transaction numbers. Defaults to 2.

    Returns:
        dict: A dictionary where the key is a string in the format 'Day_X_Hour_Y' and the value is a list of transaction values for that hour.
    """
    
    # Get the number of transactions per hour for the day
    transactions_per_hour = generate_transaction_number(std)
    day_transactions_map = {}
    
    for hour in range(hours):
        # Determine the number of transactions for the current hour
        num_transactions = transactions_per_hour[hour]
        
        # Generate a list of transaction values for this hour
        hourly_transactions = [round(generate_transaction_value(), 2) for _ in range(num_transactions)]
        
        # Create the dictionary key as 'Day_X_Hour_Y'
        key = f"Day_{day}_Hour_{hour}"
        day_transactions_map[key] = hourly_transactions
    
    return day_transactions_map


def calculate_average(transactions):
    """Calculate the average value of a list of transactions.

    This function computes the average (mean) of a list of transaction values. 
    If the list is empty, it returns 0 to avoid division by zero.

    Args:
        transactions (list): A list of transaction values (numbers).

    Returns:
        float: The average of the transaction values. Returns 0 if the list is empty.
    """
    
    # If the list is empty, return 0 to avoid division by zero
    if not transactions:
        return 0
    
    # Return the average of the transaction values
    return sum(transactions) / len(transactions)


def recollect_information(day_transactions_map, current_day, hourly_transactions_count=None):
    """Gather and process transaction data up to the current day.

    This function collects transaction information from a dictionary of daily transactions, 
    calculates the average transaction value across all days up to and including the current day,
    and returns hourly transaction counts. It also tracks the number of transactions for each hour on the current day.

    Args:
        day_transactions_map (dict): A dictionary where the keys are formatted as 'Day_X_Hour_Y' and the values 
                                     are lists of transaction values for each hour of each day.
        current_day (int): The current day to process transactions up to.
        hourly_transactions_count (list, optional): A list to accumulate the total number of transactions per hour 
                                                    across all days. If not provided, it initializes a list of zeros.

    Returns:
        tuple: A tuple containing:
            - float: The average transaction value for all days up to the current day.
            - list: The total number of transactions per hour across all days up to the current day.
            - list: The number of transactions per hour on the current day.
    """
    
    hours = 24  # Define the number of hours in a day
    hourly_transactions_count = [0] * hours  # Initialize the hourly transaction counts if not provided
    hourly_transactions_count_current_day = [0] * hours  # Initialize for tracking the current day's transactions
    
    # Combine all transactions from day 0 up to the current day
    total_transactions = []
    
    for day in range(current_day + 1):  # Iterate over all days from 0 to current_day
        for hour in range(hours):
            key = f"Day_{day}_Hour_{hour}"  # Create the key in the format 'Day_X_Hour_Y'
            if key in day_transactions_map:
                total_transactions.extend(day_transactions_map[key])  # Add all transactions for this hour
                # Accumulate the number of transactions for this hour
                hourly_transactions_count[hour] += len(day_transactions_map[key])
                
                # If we're processing the current day, record the hourly count separately
                if day == current_day:
                    hourly_transactions_count_current_day[hour] = len(day_transactions_map[key])
    
    # Calculate the average value of all accumulated transactions
    average_value = calculate_average(total_transactions)
    print(f"\nDay {current_day}: Average transaction value: {round(average_value, 2)} euros\n")
    
    # Return the average transaction value, total hourly transaction counts, and current day's hourly counts
    return round(average_value, 2), hourly_transactions_count, hourly_transactions_count_current_day


def simulate_month():
    """Simulate transaction activity over the course of a month, detect anomalies, and visualize daily transaction data.
    
    This function performs the following tasks:
    - Simulates daily transaction data for an entire month using previously defined functions.
    - Identifies anomalies in both the number and value of transactions based on predefined thresholds. Two types of anomalies are detected:
        1. **Anomalies in the number of transactions per hour**: 
           - These are based on upper and lower thresholds derived from the average hourly transactions.
           - The average is calculated from accumulated data up to the current day, but anomaly detection is skipped for the first week to prevent false positives.
        2. **Anomalies in transaction values**: 
           - Detected when transaction values exceed or fall below specific thresholds.
           - The upper threshold is set at 4 times the average transaction value (calculated from all previous transactions).
           - The lower threshold is set at 100 euros, assuming any transaction below this is unusually small.
           - These thresholds are arbitrary and can be adjusted based on the characteristics of the dataset. Setting the upper threshold to 4x the average 
             and the lower one to 100 euros is a way to flag abnormally high or low transaction amounts.
    - Generates daily visual plots:
        - Displays both the average number of hourly transactions and the current day's transaction data.
        - Marks any detected anomalies for easy visualization.
    - Logs any anomalous transactions in a text file for record-keeping.

    The function uses interactive plotting to update visual data for each day, helping track trends and highlight potential anomalies throughout the month.
    """

    # Remove the anomaly log file if it exists from a previous run
    if os.path.exists("anomalous_transactions.txt"):
        os.remove("anomalous_transactions.txt")
    
    all_transactions_map = {}  # Dictionary to store all transaction data for the month
    hourly_transactions_count = None  # Initialize to track cumulative transaction counts by hour
    average_value = 0  # Variable to track the running average of transaction values
    anomaly_threshold_upper = 2.5  # Upper threshold for anomalies (250% of the average)
    anomaly_threshold_lower = 0.25  # Lower threshold for anomalies (25% of the average)

    # Enable interactive mode for live updating of plots
    plt.ion()

    # Create the figure and axes using gridspec for multiple subplots
    fig = plt.figure(figsize=(15, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])  # 2 rows, 2 columns (lower row for logs)

    # Define axes for the plots and log area
    ax1 = fig.add_subplot(gs[0, 0])  # First row, first column (plot 1)
    ax2 = fig.add_subplot(gs[0, 1])  # First row, second column (plot 2)
    ax3 = fig.add_subplot(gs[1, :])  # Second row spans both columns (log area)

    # Loop through each day of the month to simulate transactions
    for day in range(days):
        time.sleep(1)  # Add a small delay to simulate the passing of a day
        
        # Simulate the day's transactions
        daily_transactions = simulate_day_transactions(day, std=10)
        all_transactions_map.update(daily_transactions)  # Add the day's data to the total map

        # Recollect data to update the average and transaction counts
        average_value, hourly_transactions_count, hourly_transactions_count_current_day = recollect_information(
            all_transactions_map, 
            current_day=day, 
            hourly_transactions_count=hourly_transactions_count
        )
        log_text = (f"    Hourly transactions count for current day: {hourly_transactions_count_current_day}\n\n")
        
        anomalies_indices = []  # To store indices of anomalous transactions
        anomaly_hours = []  # To store hours with anomalous transaction counts

        # Check for anomalies in the number of transactions for each hour
        for hour in range(24):
            accumulated_transactions = hourly_transactions_count[hour]
            current_day_transactions = hourly_transactions_count_current_day[hour]
            accumulated_transactions -= current_day_transactions  # Subtract current day's transactions
            
            if accumulated_transactions > 0 and day > 6:  # Avoid division by zero early in the month
                average_transactions_per_hour = accumulated_transactions / day
                
                # Check for upper threshold anomalies
                if current_day_transactions >= anomaly_threshold_upper * average_transactions_per_hour:
                    anomaly_hours.append(hour)  # Record the hour with an anomaly
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Upper threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Upper threshold)\n")
                
                # Check for lower threshold anomalies
                elif current_day_transactions <= anomaly_threshold_lower * average_transactions_per_hour:
                    anomaly_hours.append(hour)  # Record the hour with an anomaly
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Lower threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Lower threshold)\n")

        # Check for anomalies in transaction values
        daily_transactions_by_hour = {}  # Group transactions by hour
        for key in daily_transactions:
            hour = int(key.split('_')[-1])  # Extract hour from the key
            if hour not in daily_transactions_by_hour:
                daily_transactions_by_hour[hour] = []
            daily_transactions_by_hour[hour].extend(daily_transactions[key])

        daily_transaction_values = []  # Flatten the transaction values for anomaly detection
        for key in daily_transactions:
            for transaction in daily_transactions[key]:
                daily_transaction_values.append(transaction)
                # Check for value anomalies
                if transaction >= 4 * average_value:  # Upper threshold for anomalous values
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Store the index of the anomaly
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Upper threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")
                elif transaction <= 100:  # Lower threshold for anomalous values
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Store the index of the anomaly
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Lower threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")

        # Update plots with the current day's data
        hourly_transactions_avg = [count / (day + 1) for count in hourly_transactions_count]
        plot_daily_data(day, hourly_transactions_avg, hourly_transactions_count_current_day, daily_transactions_by_hour, anomalies_indices, fig, ax1, ax2, ax3, log_text, anomaly_hours)

    plt.ioff()  # Disable interactive mode when done
    plt.show()  # Display the final plot


def plot_daily_data(day, hourly_transactions_avg, hourly_transactions_current, daily_transactions_by_hour, anomalies, fig, ax1, ax2, ax3, log_text, anomaly_hours):
    """Plot daily transaction data, including anomalies and transaction details.

    This function creates three visual plots for a given day:
    1. A line chart showing average transactions per hour and a bar chart of current day transactions.
    2. A scatter plot of transaction values, highlighting anomalous transactions.
    3. A text area to display logs or additional information about the transactions.

    Args:
        day (int): The current day being plotted.
        hourly_transactions_avg (list): The average number of transactions per hour.
        hourly_transactions_current (list): The number of transactions for each hour on the current day.
        daily_transactions_by_hour (dict): A dictionary mapping each hour to a list of transaction values.
        anomalies (list): List of indexes marking anomalous transactions.
        fig (Figure): The matplotlib figure object used for plotting.
        ax1 (Axes): Axis for the average vs current transaction plot.
        ax2 (Axes): Axis for the transaction values scatter plot.
        ax3 (Axes): Axis for the log text display.
        log_text (str): Text to display in the third plot, summarizing log details.
        anomaly_hours (list): List of hours containing anomalous transactions.

    """
    
    hours = list(range(24))  # Define the list of hours from 0 to 23

    # Clear the axes before redrawing to avoid overlapping plots
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Plot 1: Average transactions per hour (line) and current day transactions (bar chart)
    bar_colors = ['red' if hour in anomaly_hours else 'orange' for hour in hours]  # Highlight bars for anomaly hours in red

    ax1.plot(hours, hourly_transactions_avg, label='Average Transactions per Hour', color='blue', marker='o')  # Plot average transactions as a line
    ax1.bar(hours, hourly_transactions_current, label='Current Day Transactions', color=bar_colors, alpha=0.6)  # Plot current day's transactions as bars

    # Set axis labels, title, and legend for the first plot
    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Number of Transactions')
    ax1.set_title(f'Day {day}: Transactions per Hour')
    ax1.legend()

    # Plot 2: Scatter plot of current day's transaction values by hour
    transaction_values = [daily_transactions_by_hour.get(hour, []) for hour in hours]  # Get the list of transactions per hour

    # Flatten the transaction values for easier plotting
    flat_transactions = [val for sublist in transaction_values for val in sublist]
    flat_hours = [hour for hour, sublist in enumerate(transaction_values) for _ in sublist]

    ax2.scatter(flat_hours, flat_transactions, label='Transaction Value', color='green')  # Scatter plot for transaction values

    # Highlight anomalous transactions in red
    for idx, hour in enumerate(flat_hours):
        if idx in anomalies:
            ax2.scatter(hour, flat_transactions[idx], color='red', label='Anomalous Transaction' if idx == anomalies[0] else "")  # Highlight anomalies

    # Set axis labels, title, and legend for the second plot
    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Transaction Value (Euros)')
    ax2.set_title(f'Day {day}: Transaction Values')
    ax2.legend()

    # Plot 3: Display log information in the third plot (ax3)
    ax3.text(0.5, 0.5, log_text, ha='center', va='center', wrap=True, fontsize=12)  # Display the log text
    ax3.axis('off')  # Hide the axis and borders around the text area

    # Update the global figure title
    fig.suptitle(f'Transactions Overview for Day {day}')
    
    # Redraw the figure to reflect the new plots
    plt.draw()
    plt.pause(1.5)  # Pause for 1.5 seconds to allow visualization before updating the plot


def main():
    """Main function to run the transaction simulation.

    This function serves as the entry point for the program. 
    It prints a starting message, runs the month-long simulation, 
    and prints a message when the simulation is complete.
    """
    
    print("Starting the simulation...")
    simulate_month()
    print("Simulation finished.")


if __name__ == "__main__":
    main()
