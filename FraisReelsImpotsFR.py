import requests
import tkinter as tk
from tkinter import messagebox

# Clé API OpenRouteService (remplace par ta propre clé)
ORS_API_KEY = "TON_API_KEY"

# Fonction pour obtenir la distance via OpenRouteService
def get_distance(home, work):
    url = f"https://api.openrouteservice.org/v2/directions/driving-car"
    params = {
        "api_key": ORS_API_KEY,
        "start": home,
        "end": work
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "routes" in data:
        return data["routes"][0]["summary"]["distance"] / 1000  # Convertir en km
    return None

# Fonction de calcul des frais réels
def calculate_real_expenses():
    home = home_entry.get()
    work = work_entry.get()
    weeks_off = int(vacation_entry.get())
    working_days = int(work_days_entry.get())
    power = int(power_entry.get())

    distance = get_distance(home, work)
    if distance is None:
        messagebox.showerror("Erreur", "Impossible d'obtenir la distance")
        return

    trips_per_year = (52 - weeks_off) * working_days * 2
    total_distance = distance * trips_per_year

    # Barème kilométrique fictif (mettre à jour avec données officielles)
    rate_per_km = {4: 0.30, 5: 0.35, 6: 0.40}
    cost_per_km = rate_per_km.get(power, 0.30)
    real_expenses = total_distance * cost_per_km

    messagebox.showinfo("Résultats", f"Distance totale : {total_distance:.2f} km\nMontant des frais réels : {real_expenses:.2f} €")

# Interface utilisateur
root = tk.Tk()
root.title("Calcul des Frais Réels")

tk.Label(root, text="Lieu d'habitation (coordonnées GPS)").pack()
home_entry = tk.Entry(root)
home_entry.pack()

tk.Label(root, text="Lieu de travail (coordonnées GPS)").pack()
work_entry = tk.Entry(root)
work_entry.pack()

tk.Label(root, text="Nombre de semaines de vacances").pack()
vacation_entry = tk.Entry(root)
vacation_entry.pack()

tk.Label(root, text="Nombre de jours travaillés par semaine").pack()
work_days_entry = tk.Entry(root)
work_days_entry.pack()

tk.Label(root, text="Puissance fiscale de la voiture").pack()
power_entry = tk.Entry(root)
power_entry.pack()

tk.Button(root, text="Calculer", command=calculate_real_expenses).pack()

root.mainloop()
