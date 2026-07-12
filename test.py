import requests
import json

# Правильный запрос с UTF-8
url = "http://localhost:8000/"
data = {
    "name": "Конференц-зал №2",
    "capacity": 20,
    "equipment": ["проектор", "звуковая система", "микрофоны"]
}

data_book = {"room_id": "909c9610-6baa-4218-b87f-1eca23af71ab", 
             "date_start": "2026-03-05 12:45:33", 
             "date_end": "2026-03-05 14:45:33",
             "username": "dorbli"} 

data_book2 = {"room_id": "97520c6e-72a9-41b8-917c-df85865e4796", 
             "date_start": "2026-03-05 13:45:33", 
             "date_end": "2026-03-05 14:30:33",
             "username": "dorbli"}

response = requests.post(
    url + 'rooms',
    json=data,
    headers={"Content-Type": "application/json; charset=utf-8"}
)
requests.post(url + 'bookings', json=data_book, headers={"Content-Type": "application/json; charset=utf-8"})

print(requests.post(url + 'bookings', json=data_book2, headers={"Content-Type": "application/json; charset=utf-8"}).json())


# requests.delete(uel + 'bookings/')
print(requests.get(url + 'rooms/97520c6e-72a9-41b8-917c-df85865e4796/bookings?date=2026-03-05').json())

# requests.delete(url + 'rooms/97520c6e-72a9-41b8-917c-df85865e4796')

input()