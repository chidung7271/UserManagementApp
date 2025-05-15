from database.db_connector import DatabaseConnector


class Pet:
    def __init__(self, db=None, id=None,user_id= None, name=None, breed=None, age=None, gender=None, adoption_date=None, health_status=None, note=None, image_path=None):
        self.db = db
        self.id = id
        self.user_id = user_id
        self.name = name
        self.breed = breed
        self.age = age
        self.gender = gender
        self.adoption_date = adoption_date
        self.health_status = health_status
        self.note = note
        self.image_path = image_path

    def create(self):
        query = "INSERT INTO pets (user_id, name, breed, age, gender, adoption_date, health_status, note, image_path) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.user_id,self.name, self.breed, self.age, self.gender, self.adoption_date, self.health_status, self.note, self.image_path)
        self.db.execute_query(query, values)
    
    def read_all(self):
        query = "SELECT * FROM pets WHERE user_id = %s"
        values = (self.user_id,)
        result = self.db.fetch_all(query,values)
        pets = []
        if not result:
            return pets
        for pet_data in result:
            pet = Pet(
                self.db,
                id=pet_data[0],
                user_id=pet_data[1],
                name=pet_data[2],
                breed=pet_data[3],
                age=pet_data[4],
                gender=pet_data[5],
                image_path=pet_data[6],
                adoption_date=pet_data[7],
                health_status=pet_data[8],
                note=pet_data[9],
                )
            pets.append(pet)
        return pets
    

    def read(self, id):
        query = "SELECT * FROM pets WHERE pet_id = %s"
        values = (id,)
        result = self.db.fetch_all(query, values)
        if result:
            pet_data = result[0]
            return Pet(
                self.db,
                id=pet_data[0],
                user_id=pet_data[1],
                name=pet_data[2],
                breed=pet_data[3],
                age=pet_data[4],
                gender=pet_data[5],
                image_path=pet_data[6],
                adoption_date=pet_data[7],
                health_status=pet_data[8],
                note=pet_data[9],
                )
        else:
            return None

    def update(self):
        query = "UPDATE pets SET user_id = %s, name = %s, breed = %s, age = %s, gender = %s, adoption_date = %s, health_status = %s, note = %s, image_path = %s WHERE pet_id = %s"
        values = (self.user_id, self.name, self.breed, self.age, self.gender, self.adoption_date, self.health_status, self.note, self.image_path, self.id)
        self.db.execute_query(query, values)

    def delete(self, id):
        query = "DELETE FROM pets WHERE pet_id = %s"
        values = (id,)
        self.db.execute_query(query, values)
    
    def get_pet_id(self):
        query = "SELECT pet_id FROM pets WHERE name = %s AND user_id = %s"
        values = (self.name,self.user_id)
        result = self.db.fetch_one(query, values)
        if result:
            self.id = result[0]
            return result[0]
        return None
