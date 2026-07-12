from datetime import datetime as dt

try:
    dt.strptime('2026-03-05_13:45:33', "%Y-%m-%d_%H:%M:%S")
            
except ValueError:
    print(123123)