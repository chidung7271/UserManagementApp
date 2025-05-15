class Calendar:
    def __init__(self, db,  user_id = None, pet_name = None, id=None, pet_id=None, event_type=None, event=None, note=None, date=None):
        self.db = db
        self.user_id = user_id
        self.pet_name =  pet_name
        self.calendar_id = id
        self.pet_id = pet_id
        self.event_type = event_type
        self.event = event
        self.note = note
        self.date = date
    
    def create(self):
        query = "INSERT INTO calendar ( pet_id, event_type, event, note, date) VALUES ( %s, %s, %s, %s, %s)"
        values = ( self.pet_id, self.event_type, self.event, self.note, self.date)
        self.db.execute_query(query, values)

    def read_all(self):
        query = """
        SELECT c.calendar_id, c.pet_id, p.name AS pet_name,c.event_type, c.event, c.note, c.date
        FROM calendar c
        JOIN pets p ON c.pet_id = p.pet_id
        WHERE p.user_id = %s
        """
        values = (self.user_id,)
        result = self.db.fetch_all(query, values)
        calendars = []
        if not result:
            return calendars
        for calendar_data in result:
            calendar = Calendar(
                self.db,
                self.user_id,
                id=calendar_data[0],
                pet_id=calendar_data[1],
                pet_name=calendar_data[2],
                event_type=calendar_data[3],
                event=calendar_data[4],
                note=calendar_data[5],
                date=calendar_data[6],
            )
            
            calendars.append(calendar)
        return calendars
    def delete(self):
        query ="DELETE FROM calendar WHERE calendar_id = %s"
        values = (self.calendar_id,)
        self.db.execute_query(query, values)
        
    def update(self):
        query = "UPDATE calendar SET pet_id = %s, event_type = %s, event = %s, note = %s, date = %s WHERE calendar_id = %s"
        values = ( self.pet_id, self.event_type, self.event, self.note, self.date, self.calendar_id)
        self.db.execute_query(query, values)
    
    def get_calendar_id(self):
        query = "SELECT calendar_id FROM calendar WHERE pet_id = %s AND event_type = %s AND event = %s AND note = %s AND date = %s"
        values = (self.pet_id, self.event_type, self.event, self.note, self.date)
        result = self.db.fetch_one(query, values)
        if result:
            self.calendar_id = result[0]
            return result[0]
        return None