import time
import os
import random
import numpy as np
import matplotlib.pyplot as plt

days = 30 # Number of days, perform a month
hours = 24 # Number of hours, perform a day


def generate_transaction_number(is_weekend, std):
    transactions_per_hour_laboral_days = [ 
    max(0, random.randint(3, 15) + abs(int(random.gauss(0, std)))),  # 00:00
    max(0, random.randint(0, 10) + abs(int(random.gauss(0, std)))),  # 01:00
    max(0, random.randint(1, 10) + abs(int(random.gauss(0, std)))),  # 02:00
    max(0, random.randint(1, 10) + abs(int(random.gauss(0, std)))),  # 03:00
    max(0, random.randint(2, 10) + abs(int(random.gauss(0, std)))),  # 04:00
    max(0, random.randint(4, 10) + abs(int(random.gauss(0, std)))),  # 05:00
    max(0, random.randint(10, 20) + abs(int(random.gauss(0, std)))), # 06:00
    max(0, random.randint(10, 30) + abs(int(random.gauss(0, std)))), # 07:00
    max(0, random.randint(20, 60) + abs(int(random.gauss(0, std)))), # 08:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 09:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 10:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 11:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 12:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 13:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 14:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 15:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 16:00
    max(0, random.randint(30, 100) + abs(int(random.gauss(0, std)))), # 17:00
    max(0, random.randint(20, 80) + abs(int(random.gauss(0, std)))),  # 18:00
    max(0, random.randint(20, 60) + abs(int(random.gauss(0, std)))),  # 19:00
    max(0, random.randint(20, 60) + abs(int(random.gauss(0, std)))),  # 20:00
    max(0, random.randint(10, 40) + abs(int(random.gauss(0, std)))),  # 21:00
    max(0, random.randint(10, 30) + abs(int(random.gauss(0, std)))),  # 22:00
    max(0, random.randint(5, 20) + abs(int(random.gauss(0, std))))    # 23:00
]

    if is_weekend:
        # The number of transactions per hour in weekend days (24h) is 1/3 of the number of transactions in laboral days
        transactions_per_hour_weekend = [transactions_per_hour_laboral_days[i] // 1 for i in range(hours)]
        return transactions_per_hour_weekend
    
    return transactions_per_hour_laboral_days
  


def generate_transaction_value():
    mean_value = 20000  # Valor promedio de las transacciones
    std_deviation = 50000  # Desviación estándar, ajusta para controlar la dispersión
    transaction_value = np.random.normal(mean_value, std_deviation)
    
    # Nos aseguramos de que el valor generado no sea negativo
    return max(-transaction_value, transaction_value)


def simulate_day_transactions(day, is_weekend=False, std=2):
    transactions_per_hour = generate_transaction_number(is_weekend, std)
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



def recollect_information(day_transactions_map, current_day, hourly_transactions_count=None):
    hours = 24  # Definimos el número de horas
    hourly_transactions_count = [0] * hours
    hourly_transactions_count_current_day = [0] * hours  # Crear una lista con 24 posiciones inicializadas en 0
    
    # Unir todas las transacciones de los días hasta el current_day
    total_transactions = []
    
    for day in range(current_day + 1):  # Iterar sobre los días desde el día 0 hasta current_day

        for hour in range(hours):
            key = f"Day_{day}_Hour_{hour}"
            if key in day_transactions_map:
                total_transactions.extend(day_transactions_map[key])  # Agregar las transacciones de cada hora
                # Sumar las transacciones de esa hora a la lista acumulada
                # hourly_transactions_count[hour] += len(day_transactions_map[key])
                hourly_transactions_count[hour] += len(day_transactions_map[key])

                if day == current_day:
                    hourly_transactions_count_current_day[hour] = len(day_transactions_map[key])
    
    # Calcular el promedio de todas las transacciones acumuladas
    average_value = calculate_average(total_transactions)
    print(f"\nDay {current_day}: Average transaction value: {round(average_value, 2)} euros\n")
    
    # Devolver el promedio y la lista de conteos acumulados por hora
    return round(average_value, 2), hourly_transactions_count, hourly_transactions_count_current_day


def simulate_month():
    if os.path.exists("anomalous_transactions.txt"):
        os.remove("anomalous_transactions.txt")
    
    all_transactions_map = {}
    hourly_transactions_count = None  # Inicializamos para mantener el conteo de las transacciones por hora
    average_value = 0  # Variable para mantener el promedio actualizado
    anomaly_threshold_upper = 2.5  # Umbral superior para anomalías en número de transacciones (200% del promedio)
    anomaly_threshold_lower = 0.25  # Umbral inferior para anomalías (50% del promedio)

    # Activamos el modo interactivo de matplotlib
    plt.ion()  # Interactive mode ON

    # Crear la figura y los ejes solo una vez, fuera del bucle
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    for day in range(days):
        time.sleep(1)
        
        is_weekend = (day % 7 == 5 or day % 7 == 6)  # Sábado y domingo
        daily_transactions = simulate_day_transactions(day, is_weekend, std=10)
        all_transactions_map.update(daily_transactions)  # Agregar al mapa general

        # Recolectar información y actualizar el promedio y el conteo de transacciones por hora
        average_value, hourly_transactions_count, hourly_transactions_count_current_day = recollect_information(
            all_transactions_map, 
            current_day=day, 
            hourly_transactions_count=hourly_transactions_count
        )
        print(f"    Hourly transactions count: {hourly_transactions_count}\n")
        print(f"    Hourly transactions count for current day: {hourly_transactions_count_current_day}\n")

        anomalies_indices = []  # Para almacenar índices de transacciones anómalas

        # Verificamos si el número de transacciones es anómalo para cada hora
        for hour in range(24):
            accumulated_transactions = hourly_transactions_count[hour]
            current_day_transactions = hourly_transactions_count_current_day[hour]
            accumulated_transactions = accumulated_transactions - current_day_transactions  # Restar las transacciones del día actual
            
            if accumulated_transactions > 0 and day > 6:  # Evitar división por cero
                average_transactions_per_hour = accumulated_transactions / day
                
                # Comprobamos si las transacciones del día actual para esa hora son anómalas
                if current_day_transactions >= anomaly_threshold_upper * average_transactions_per_hour:
                    print(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Upper threshold) {average_transactions_per_hour}" )
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Upper threshold)\n")
                
                elif current_day_transactions <= anomaly_threshold_lower * average_transactions_per_hour:
                    print(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Lower threshold) {average_transactions_per_hour}")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Lower threshold)\n")

        # Comprobamos si alguna transacción tiene un valor anómalo
        daily_transactions_by_hour = {}  # Agrupamos las transacciones por hora
        for key in daily_transactions:
            hour = int(key.split('_')[-1])  # Extraer la hora de la clave
            if hour not in daily_transactions_by_hour:
                daily_transactions_by_hour[hour] = []
            daily_transactions_by_hour[hour].extend(daily_transactions[key])

        daily_transaction_values = []
        for key in daily_transactions:
            for transaction in daily_transactions[key]:
                daily_transaction_values.append(transaction)
                if transaction >= 4 * average_value:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    print(f"Anomalous transaction detected on {key}: {transaction} euros (Upper threshold) {average_value}")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")
                elif transaction <= 100:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    print(f"Anomalous transaction detected on {key}: {transaction} euros (Lower threshold) {average_value}")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")

        # Actualizar las gráficas de la información del día actual
        hourly_transaction_avg = [count / (day + 1) for count in hourly_transactions_count]
        plot_daily_data(day, hourly_transaction_avg, hourly_transactions_count_current_day, daily_transactions_by_hour, anomalies_indices, fig, ax1, ax2)

    plt.ioff()  # Desactivar el modo interactivo al finalizar
    plt.show()  # Mostrar la gráfica final al terminar

    return all_transactions_map, average_value, hourly_transactions_count

import matplotlib.gridspec as gridspec

def simulate_month():
    if os.path.exists("anomalous_transactions.txt"):
        os.remove("anomalous_transactions.txt")
    
    all_transactions_map = {}
    hourly_transactions_count = None  # Inicializamos para mantener el conteo de las transacciones por hora
    average_value = 0  # Variable para mantener el promedio actualizado
    anomaly_threshold_upper = 2.5  # Umbral superior para anomalías en número de transacciones (200% del promedio)
    anomaly_threshold_lower = 0.25  # Umbral inferior para anomalías (50% del promedio)

    # Activamos el modo interactivo de matplotlib
    plt.ion()  # Interactive mode ON

    # Crear la figura y los ejes usando gridspec
    fig = plt.figure(figsize=(15, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])  # 2 filas, 2 columnas, la fila inferior es para los logs

    # Ejes para los gráficos y el área de logs
    ax1 = fig.add_subplot(gs[0, 0])  # Primera fila, primera columna (gráfico 1)
    ax2 = fig.add_subplot(gs[0, 1])  # Primera fila, segunda columna (gráfico 2)
    ax3 = fig.add_subplot(gs[1, :])  # Segunda fila, ocupa ambas columnas (área de logs)

    for day in range(days):
        time.sleep(1)
        
        is_weekend = (day % 7 == 5 or day % 7 == 6)  # Sábado y domingo
        daily_transactions = simulate_day_transactions(day, is_weekend, std=10)
        all_transactions_map.update(daily_transactions)  # Agregar al mapa general

        # Recolectar información y actualizar el promedio y el conteo de transacciones por hora
        average_value, hourly_transactions_count, hourly_transactions_count_current_day = recollect_information(
            all_transactions_map, 
            current_day=day, 
            hourly_transactions_count=hourly_transactions_count
        )
        log_text = (f"    Hourly transactions count: {hourly_transactions_count}\n"
                    f"    Hourly transactions count for current day: {hourly_transactions_count_current_day}\n")
        
        anomalies_indices = []  # Para almacenar índices de transacciones anómalas

        # Verificamos si el número de transacciones es anómalo para cada hora
        for hour in range(24):
            accumulated_transactions = hourly_transactions_count[hour]
            current_day_transactions = hourly_transactions_count_current_day[hour]
            accumulated_transactions = accumulated_transactions - current_day_transactions  # Restar las transacciones del día actual
            
            if accumulated_transactions > 0 and day > 6:  # Evitar división por cero
                average_transactions_per_hour = accumulated_transactions / day
                
                # Comprobamos si las transacciones del día actual para esa hora son anómalas
                if current_day_transactions >= anomaly_threshold_upper * average_transactions_per_hour:
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Upper threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Upper threshold)\n")
                
                elif current_day_transactions <= anomaly_threshold_lower * average_transactions_per_hour:
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Lower threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Lower threshold)\n")

        # Comprobamos si alguna transacción tiene un valor anómalo
        daily_transactions_by_hour = {}  # Agrupamos las transacciones por hora
        for key in daily_transactions:
            hour = int(key.split('_')[-1])  # Extraer la hora de la clave
            if hour not in daily_transactions_by_hour:
                daily_transactions_by_hour[hour] = []
            daily_transactions_by_hour[hour].extend(daily_transactions[key])

        daily_transaction_values = []
        for key in daily_transactions:
            for transaction in daily_transactions[key]:
                daily_transaction_values.append(transaction)
                if transaction >= 4 * average_value:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Upper threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")
                elif transaction <= 100:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Lower threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")

        # Actualizar las gráficas y los logs de la información del día actual
        hourly_transactions_avg = [count / (day + 1) for count in hourly_transactions_count]
        plot_daily_data(day, hourly_transactions_avg, hourly_transactions_count_current_day, daily_transactions_by_hour, anomalies_indices, fig, ax1, ax2, ax3, log_text)

    plt.ioff()  # Desactivar el modo interactivo al finalizar
    plt.show()  # Mostrar la gráfica final al terminar

    return all_transactions_map, average_value, hourly_transactions_count

def simulate_month():
    if os.path.exists("anomalous_transactions.txt"):
        os.remove("anomalous_transactions.txt")
    
    all_transactions_map = {}
    hourly_transactions_count = None  # Inicializamos para mantener el conteo de las transacciones por hora
    average_value = 0  # Variable para mantener el promedio actualizado
    anomaly_threshold_upper = 2.5  # Umbral superior para anomalías en número de transacciones (200% del promedio)
    anomaly_threshold_lower = 0.25  # Umbral inferior para anomalías (50% del promedio)

    # Activamos el modo interactivo de matplotlib
    plt.ion()  # Interactive mode ON

    # Crear la figura y los ejes usando gridspec
    fig = plt.figure(figsize=(15, 10))
    gs = gridspec.GridSpec(2, 2, height_ratios=[2, 1])  # 2 filas, 2 columnas, la fila inferior es para los logs

    # Ejes para los gráficos y el área de logs
    ax1 = fig.add_subplot(gs[0, 0])  # Primera fila, primera columna (gráfico 1)
    ax2 = fig.add_subplot(gs[0, 1])  # Primera fila, segunda columna (gráfico 2)
    ax3 = fig.add_subplot(gs[1, :])  # Segunda fila, ocupa ambas columnas (área de logs)

    for day in range(days):
        time.sleep(1)
        
        is_weekend = (day % 7 == 5 or day % 7 == 6)  # Sábado y domingo
        daily_transactions = simulate_day_transactions(day, is_weekend, std=10)
        all_transactions_map.update(daily_transactions)  # Agregar al mapa general

        # Recolectar información y actualizar el promedio y el conteo de transacciones por hora
        average_value, hourly_transactions_count, hourly_transactions_count_current_day = recollect_information(
            all_transactions_map, 
            current_day=day, 
            hourly_transactions_count=hourly_transactions_count
        )
        log_text = (f"    Hourly transactions count for current day: {hourly_transactions_count_current_day}\n\n")
        
        anomalies_indices = []  # Para almacenar índices de transacciones anómalas
        anomaly_hours = []  # Almacenar las horas con transacciones anómalas

        # Verificamos si el número de transacciones es anómalo para cada hora
        for hour in range(24):
            accumulated_transactions = hourly_transactions_count[hour]
            current_day_transactions = hourly_transactions_count_current_day[hour]
            accumulated_transactions = accumulated_transactions - current_day_transactions  # Restar las transacciones del día actual
            
            if accumulated_transactions > 0 and day > 6:  # Evitar división por cero
                average_transactions_per_hour = accumulated_transactions / day
                
                # Comprobamos si las transacciones del día actual para esa hora son anómalas
                if current_day_transactions >= anomaly_threshold_upper * average_transactions_per_hour:
                    anomaly_hours.append(hour)  # Registrar la hora con anomalía
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Upper threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Upper threshold)\n")
                
                elif current_day_transactions <= anomaly_threshold_lower * average_transactions_per_hour:
                    anomaly_hours.append(hour)  # Registrar la hora con anomalía
                    log_text += (f"Anomalous number of transactions detected at Day {day}, Hour {hour}: "
                                 f"{current_day_transactions} transactions (Lower threshold) {average_transactions_per_hour}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"Anomalous number of transactions detected at Day {day}, Hour {hour}: {current_day_transactions} transactions (Lower threshold)\n")

        # Comprobamos si alguna transacción tiene un valor anómalo
        daily_transactions_by_hour = {}  # Agrupamos las transacciones por hora
        for key in daily_transactions:
            hour = int(key.split('_')[-1])  # Extraer la hora de la clave
            if hour not in daily_transactions_by_hour:
                daily_transactions_by_hour[hour] = []
            daily_transactions_by_hour[hour].extend(daily_transactions[key])

        daily_transaction_values = []
        for key in daily_transactions:
            for transaction in daily_transactions[key]:
                daily_transaction_values.append(transaction)
                if transaction >= 4 * average_value:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Upper threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")
                elif transaction <= 100:
                    anomalies_indices.append(len(daily_transaction_values) - 1)  # Almacenar el índice de la anomalía
                    log_text += (f"Anomalous transaction detected on {key}: {transaction} euros (Lower threshold) {average_value}\n")
                    with open("anomalous_transactions.txt", "a") as file:
                        file.write(f"{key}: {transaction}\n")

        # Actualizar las gráficas y los logs de la información del día actual
        hourly_transactions_avg = [count / (day + 1) for count in hourly_transactions_count]
        plot_daily_data(day, hourly_transactions_avg, hourly_transactions_count_current_day, daily_transactions_by_hour, anomalies_indices, fig, ax1, ax2, ax3, log_text, anomaly_hours)

    plt.ioff()  # Desactivar el modo interactivo al finalizar
    plt.show()  # Mostrar la gráfica final al terminar

    return all_transactions_map, average_value, hourly_transactions_count


def plot_daily_data(day, hourly_transactions_avg, hourly_transactions_current, daily_transactions_by_hour, anomalies, fig, ax1, ax2):
    hours = list(range(24))

    # Limpiar los ejes antes de volver a dibujar
    ax1.clear()
    ax2.clear()

    # Gráfico 1: Promedio de transacciones por hora (línea) y transacciones actuales (barra)
    ax1.plot(hours, hourly_transactions_avg, label='Average Transactions per Hour', color='blue', marker='o')
    ax1.bar(hours, hourly_transactions_current, label='Current Day Transactions', alpha=0.6, color='orange')

    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Number of Transactions')
    ax1.set_title(f'Day {day}: Transactions per Hour')
    ax1.legend()

    # Gráfico 2: Valores de las transacciones del día actual organizadas por hora
    transaction_values = [daily_transactions_by_hour.get(hour, []) for hour in hours]

    # Aplanamos los valores para graficarlos
    flat_transactions = [val for sublist in transaction_values for val in sublist]
    flat_hours = [hour for hour, sublist in enumerate(transaction_values) for _ in sublist]

    ax2.scatter(flat_hours, flat_transactions, label='Transaction Value', color='green')

    # Marcamos en rojo las transacciones anómalas
    for idx, hour in enumerate(flat_hours):
        if idx in anomalies:
            ax2.scatter(hour, flat_transactions[idx], color='red', label='Anomalous Transaction' if idx == anomalies[0] else "")

    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Transaction Value (Euros)')
    ax2.set_title(f'Day {day}: Transaction Values')
    ax2.legend()

    # Actualizar el título global de la figura
    fig.suptitle(f'Transactions Overview for Day {day}')
    
    # Redibujar la figura
    plt.draw()
    plt.pause(1.5)  # Pausa de 1.5 segundos para visualizar la gráfica antes de actualizar

import matplotlib.pyplot as plt

def plot_daily_data(day, hourly_transactions_avg, hourly_transactions_current, daily_transactions_by_hour, anomalies, fig, ax1, ax2, ax3, log_text):
    hours = list(range(24))

    # Limpiar los ejes antes de volver a dibujar
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Gráfico 1: Promedio de transacciones por hora (línea) y transacciones actuales (barra)
    ax1.plot(hours, hourly_transactions_avg, label='Average Transactions per Hour', color='blue', marker='o')
    ax1.bar(hours, hourly_transactions_current, label='Current Day Transactions', alpha=0.6, color='orange')

    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Number of Transactions')
    ax1.set_title(f'Day {day}: Transactions per Hour')
    ax1.legend()

    # Gráfico 2: Valores de las transacciones del día actual organizadas por hora
    transaction_values = [daily_transactions_by_hour.get(hour, []) for hour in hours]

    # Aplanamos los valores para graficarlos
    flat_transactions = [val for sublist in transaction_values for val in sublist]
    flat_hours = [hour for hour, sublist in enumerate(transaction_values) for _ in sublist]

    ax2.scatter(flat_hours, flat_transactions, label='Transaction Value', color='green')

    # Marcamos en rojo las transacciones anómalas
    for idx, hour in enumerate(flat_hours):
        if idx in anomalies:
            ax2.scatter(hour, flat_transactions[idx], color='red', label='Anomalous Transaction' if idx == anomalies[0] else "")

    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Transaction Value (Euros)')
    ax2.set_title(f'Day {day}: Transaction Values')
    ax2.legend()

    # Mostrar logs en el área de texto
    ax3.text(0.5, 0.5, log_text, ha='center', va='center', wrap=True, fontsize=12)
    ax3.axis('off')  # Ocultar el borde del área de texto

    # Actualizar el título global de la figura
    fig.suptitle(f'Transactions Overview for Day {day}')
    
    # Redibujar la figura
    plt.draw()
    plt.pause(1.5)  # Pausa de 1.5 segundos para visualizar la gráfica antes de actualizar

def plot_daily_data(day, hourly_transactions_avg, hourly_transactions_current, daily_transactions_by_hour, anomalies, fig, ax1, ax2, ax3, log_text, anomaly_hours):
    hours = list(range(24))

    # Limpiar los ejes antes de volver a dibujar
    ax1.clear()
    ax2.clear()
    ax3.clear()

    # Gráfico 1: Promedio de transacciones por hora (línea) y transacciones actuales (barra)
    bar_colors = ['red' if hour in anomaly_hours else 'orange' for hour in hours]  # Cambiar color de las barras

    ax1.plot(hours, hourly_transactions_avg, label='Average Transactions per Hour', color='blue', marker='o')
    ax1.bar(hours, hourly_transactions_current, label='Current Day Transactions', color=bar_colors, alpha=0.6)

    ax1.set_xlabel('Hour of Day')
    ax1.set_ylabel('Number of Transactions')
    ax1.set_title(f'Day {day}: Transactions per Hour')
    ax1.legend()

    # Gráfico 2: Valores de las transacciones del día actual organizadas por hora
    transaction_values = [daily_transactions_by_hour.get(hour, []) for hour in hours]

    # Aplanamos los valores para graficarlos
    flat_transactions = [val for sublist in transaction_values for val in sublist]
    flat_hours = [hour for hour, sublist in enumerate(transaction_values) for _ in sublist]

    ax2.scatter(flat_hours, flat_transactions, label='Transaction Value', color='green')

    # Marcamos en rojo las transacciones anómalas
    for idx, hour in enumerate(flat_hours):
        if idx in anomalies:
            ax2.scatter(hour, flat_transactions[idx], color='red', label='Anomalous Transaction' if idx == anomalies[0] else "")

    ax2.set_xlabel('Hour of Day')
    ax2.set_ylabel('Transaction Value (Euros)')
    ax2.set_title(f'Day {day}: Transaction Values')
    ax2.legend()

    # Mostrar logs en el área de texto
    ax3.text(0.5, 0.5, log_text, ha='center', va='center', wrap=True, fontsize=12)
    ax3.axis('off')  # Ocultar el borde del área de texto

    # Actualizar el título global de la figura
    fig.suptitle(f'Transactions Overview for Day {day}')
    
    # Redibujar la figura
    plt.draw()
    plt.pause(1.5)  # Pausa de 1.5 segundos para visualizar la gráfica antes de actualizar


def main():
    print("Starting the simulation...")
    all_transactions_map = simulate_month()

    # print(all_transactions_map)
    print("Simulation finished.")
    
    # Ejemplo de cómo acceder a las transacciones de un día y hora específicos
    example_key = "Day_1_Hour_2"
    if example_key in all_transactions_map:
        print(f"Transactions for {example_key}: {all_transactions_map[example_key]}")



if __name__ == "__main__":
    main()
