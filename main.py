import time
import os
import random
import numpy as np

days = 4 # Number of days, perform a month
hours = 24 # Number of hours, perform a day
s=2 # Standard deviation
transactions_per_hour_laboral_days = [ # The number of transactions per hour in laboral days (24h) is different for each hour
    max(0, random.randint(0, 15) + int(random.gauss(0, s))), # 00:00
    max(0, random.randint(0, 10) + int(random.gauss(0, s))), # 01:00
    max(0, random.randint(0, 10) + int(random.gauss(0, s))), # 02:00
    max(0, random.randint(0, 10) + int(random.gauss(0, s))), # 03:00
    max(0, random.randint(0, 10) + int(random.gauss(0, s))), # 04:00
    max(0, random.randint(0, 10) + int(random.gauss(0, s))), # 05:00
    max(0, random.randint(10, 20) + int(random.gauss(0, s))), # 06:00
    max(0, random.randint(10, 30) + int(random.gauss(0, s))), # 07:00
    max(0, random.randint(20, 60) + int(random.gauss(0, s))), # 08:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 09:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 10:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 11:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 12:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 13:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 14:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 15:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 16:00
    max(0, random.randint(30, 100) + int(random.gauss(0, s))), # 17:00
    max(0, random.randint(20, 80) + int(random.gauss(0, s))),  # 18:00
    max(0, random.randint(20, 60) + int(random.gauss(0, s))),  # 19:00
    max(0, random.randint(20, 60) + int(random.gauss(0, s))),  # 20:00
    max(0, random.randint(10, 40) + int(random.gauss(0, s))),  # 21:00
    max(0, random.randint(10, 30) + int(random.gauss(0, s))),  # 22:00
    max(0, random.randint(5, 20) + int(random.gauss(0, s)))   # 23:00
]
average_value = 0   
# The number of transactions per hour in weekend days (24h) is 1/3 of the number of transactions in laboral days
transactions_per_hour_weekend = [transactions_per_hour_laboral_days[i] // 3 for i in range(hours)]

def generate_transaction_value():
    mean_value = 20000  # Valor promedio de las transacciones
    std_deviation = 20000  # Desviación estándar, ajusta para controlar la dispersión
    transaction_value = np.random.normal(mean_value, std_deviation)
    
    # Nos aseguramos de que el valor generado no sea negativo
    return max(-transaction_value, transaction_value)

def simulate_day_transactions(day, is_weekend=False):
    transactions_per_hour = transactions_per_hour_weekend if is_weekend else transactions_per_hour_laboral_days
    day_transactions_map = {}
    
    for hour in range(hours):
        num_transactions = transactions_per_hour[hour]
        hourly_transactions = [round(generate_transaction_value(), 2) for _ in range(num_transactions)]
        # print(f"->: {num_transactions} transactions simulated for Hour {hour}.")
        # print(f"     Hour {hour}: {hourly_transactions} transactions received.")
        
        # Crear la clave como 'Day_X_Hour_Y'
        key = f"Day_{day}_Hour_{hour}"
        day_transactions_map[key] = hourly_transactions
    
    return day_transactions_map

def calculate_average(transactions):
    if not transactions:
        return 0
    return sum(transactions) / len(transactions)

def recollect_information(day_transactions_map):
    # Unir todas las transacciones del día 0
    day_0_transactions = []
    for hour in range(hours):
        key = f"Day_0_Hour_{hour}"
        if key in day_transactions_map:
            day_0_transactions.extend(day_transactions_map[key])  # Agregar las transacciones de cada hora
    
    # Calcular el promedio de las transacciones del día 0
    average_value = calculate_average(day_0_transactions)
    print(f"\nDay 0: Average transaction value: {round(average_value, 2)} euros\n")
    return round(average_value, 2)


def simulate_month():
    if os.path.exists("anomalous_transactions.txt"):
                            os.remove("anomalous_transactions.txt")
    all_transactions_map = {}
    
    for day in range(days):
        # Solicitar al usuario que escriba "pass next day" para avanzar al siguiente día
        user_input = input("Type 'enter' to continue to the next day: ").strip()

       
        
        # Comprobar que el usuario haya escrito la cadena correcta
        while user_input != "":
            print("Invalid input. Please type 'enter' to proceed.")
            user_input = input("Type 'pass next day' to continue to the next day: ").strip()
        
        is_weekend = (day % 7 == 5 or day % 7 == 6)  # Sábado y domingo
        daily_transactions = simulate_day_transactions(day, is_weekend)
        all_transactions_map.update(daily_transactions)  # Agregar al mapa general

        if day == 0:
            average_value = recollect_information(all_transactions_map)
        else:
            # Comprobamos si para cada transacción el valor 200% mayor o menor que el promedio, y si es así, imprimimos por consola que hay una transacción anomala
            for key in daily_transactions:
                for transaction in daily_transactions[key]:
                    if transaction >= 4 * average_value or transaction <= 0.05 * average_value:
                        print(f"Anomalous transaction detected on {key}: {transaction} euros")
                        # almacenamos las transacciones sospechosas en un archivo                        
                        with open("anomalous_transactions.txt", "a") as file:
                            file.write(f"{key}: {transaction}\n")
    
    return all_transactions_map, average_value

def main():
    print("Starting the simulation...")
    all_transactions_map, average_value = simulate_month()

    # print(all_transactions_map)
    print("Simulation finished.")
    
    # Ejemplo de cómo acceder a las transacciones de un día y hora específicos
    example_key = "Day_1_Hour_2"
    if example_key in all_transactions_map:
        print(f"Transactions for {example_key}: {all_transactions_map[example_key]}")

if __name__ == "__main__":
    main()
