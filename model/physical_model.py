class Physical:
    def __init__(self, db, user_id = None, pet_name = None, physical_id = None, pet_id = None, weight = None, height = None, date = None, note = None):
        self.db = db
        self.user_id = user_id
        self.pet_name = pet_name
        self.physical_id = physical_id
        self.pet_id = pet_id
        self.weight = weight
        self.height = height
        self.date = date
        self.note = note
    
    def create(self):
        query = "INSERT INTO physical (pet_id, weight, height, date, note) VALUES (%s, %s, %s, %s, %s)"
        values = (self.pet_id, self.weight, self.height, self.date, self.note)
        self.db.execute_query(query, values)

    def read_all(self):
        query = """
        SELECT p.physical_id, p.pet_id, pet.name AS pet_name, p.weight, p.height, p.date, p.note
        FROM physical p
        JOIN pets pet ON p.pet_id = pet.pet_id
        WHERE pet.user_id = %s
        """
        values = (self.user_id,)
        result = self.db.fetch_all(query, values)
        physicals = []
        if not result:
            return physicals
        for physical_data in result:
            physical = Physical(
                self.db,
                self.user_id,
                pet_name=physical_data[2],
                physical_id=physical_data[0],
                pet_id=physical_data[1],
                weight=physical_data[3],
                height=physical_data[4],
                date=physical_data[5],
                note=physical_data[6],
            )
            physicals.append(physical)
        return physicals

    def delete(self):
        query = "DELETE FROM physical WHERE physical_id = %s"
        values = (self.physical_id,)
        self.db.execute_query(query, values)

    def update(self):
        query = "UPDATE physical SET pet_id = %s, weight = %s, height = %s, date = %s, note = %s WHERE physical_id = %s"
        values = (self.pet_id, self.weight, self.height, self.date, self.note, self.physical_id)
        self.db.execute_query(query, values)

    def get_physical_id(self):
        query = "SELECT physical_id FROM physical WHERE pet_id = %s AND weight = %s AND height = %s AND date = %s AND note = %s"
        values = (self.pet_id, self.weight, self.height, self.date, self.note)
        result = self.db.fetch_one(query, values)
        if result:
            self.physical_id = result[0]
            return result[0]
        return None
        
