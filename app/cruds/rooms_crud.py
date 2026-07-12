from database.database import get_db

def get_room_by_id(room_id: str):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM rooms WHERE id = ?", 
            (room_id,)).fetchone()
        if row:
            return dict(row, equipment=eval(row["equipment"]))
        return '404'

def room_exists(name: str):
    with get_db() as conn:
        query = "SELECT id FROM rooms WHERE name = ?"
        params = [name]
        if conn.execute(query, params).fetchone() is not None:
            return '409'

def create_room_in_db(room_id: str, name: str, capacity: int, equipment: list):
    with get_db() as conn:
        conn.execute("INSERT INTO rooms (id, name, capacity, equipment) VALUES (?, ?, ?, ?)",
            (room_id, name, capacity, str(equipment)))
        conn.commit()

def update_room_in_db(room_id: str, name: str, capacity: int, equipment: list):
    with get_db() as conn:
        conn.execute("UPDATE rooms SET name = ?, capacity = ?, equipment = ? WHERE id = ?",
            (name, capacity, str(equipment), room_id))
        conn.commit()

def delete_room_in_db(room_id: str):
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM rooms WHERE id = ?", 
            (room_id,))
        conn.commit()
        return cursor.rowcount

def get_all_rooms_with_filters(min_cap=None, max_cap=None):
    with get_db() as conn:
        query = "SELECT * FROM rooms WHERE 1=1"
        params = []

        if min_cap is not None:
            query += " AND capacity >= ?"
            params.append(min_cap)
        if max_cap is not None:
            query += " AND capacity <= ?"
            params.append(max_cap)
        
        rows = conn.execute(query, params).fetchall()
        result = []
        for row in rows:
            room = dict(row, equipment=eval(row["equipment"]))
            result.append(room)
        return result