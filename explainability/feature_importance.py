import pandas as pd

def explain():
    return {
        "time_of_day": "Peak hour rides increase demand",
        "zone_density": "Urban zones drive higher demand",
        "weekday": "Office days raise bookings"
    }

if __name__ == "__main__":
    print(explain())
