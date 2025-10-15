# --------------------------------------------------------------
# Importar librerías necesarias
# --------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------------------------------------------------
# Crear las carpetas necesarias si no existen
# --------------------------------------------------------------
os.makedirs("files/output", exist_ok=True)
os.makedirs("files/plots", exist_ok=True)

# --------------------------------------------------------------
# Cargar los archivos CSV de entrada
# --------------------------------------------------------------
drivers = pd.read_csv("files/input/drivers.csv")
timesheet = pd.read_csv("files/input/timesheet.csv")

# --------------------------------------------------------------
# Crear tabla timesheet_with_means (promedio de horas por driver)
# --------------------------------------------------------------
timesheet_with_means = timesheet.copy()
mean_hours = timesheet.groupby("driverId")["hours-logged"].mean().reset_index()
mean_hours.rename(columns={"hours-logged": "mean_hours-logged"}, inplace=True)
timesheet_with_means = pd.merge(timesheet_with_means, mean_hours, on="driverId", how="left")

# --------------------------------------------------------------
# Crear tabla timesheet_below: registros con menos horas que el promedio
# --------------------------------------------------------------
timesheet_below = timesheet_with_means[timesheet_with_means["hours-logged"] < timesheet_with_means["mean_hours-logged"]]

# --------------------------------------------------------------
# Crear sum_timesheet: suma de horas y millas por driver
# --------------------------------------------------------------
sum_timesheet = timesheet.groupby("driverId")[["hours-logged", "miles-logged"]].sum().reset_index()

# --------------------------------------------------------------
# Crear min_max_timesheet: min y max de horas por driver
# --------------------------------------------------------------
min_max_timesheet = timesheet.groupby("driverId")["hours-logged"].agg(["min", "max"]).reset_index()

# --------------------------------------------------------------
# Crear summary: unir sum_timesheet con drivers
# --------------------------------------------------------------
summary = pd.merge(sum_timesheet, drivers[["driverId", "name"]], on="driverId", how="left")

# --------------------------------------------------------------
# Guardar summary.csv
# --------------------------------------------------------------
summary.to_csv("files/output/summary.csv", index=False)

# --------------------------------------------------------------
# Crear tabla top10 con los conductores con más millas registradas
# --------------------------------------------------------------
top10 = summary.sort_values(by="miles-logged", ascending=False).head(10)

# --------------------------------------------------------------
# Crear gráfico de barras horizontales
# --------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.barh(top10["name"], top10["miles-logged"], color="lightblue")
plt.xlabel("Millas registradas")
plt.ylabel("Conductor")
plt.title("Top 10 conductores por millas registradas")
plt.gca().invert_yaxis()  # El conductor con más millas arriba
plt.tight_layout()

# Guardar gráfico
plt.savefig("files/plots/top10_drivers.png")
plt.close()

print("Archivos generados correctamente:")
print(" - files/output/summary.csv")
print(" - files/plots/top10_drivers.png")