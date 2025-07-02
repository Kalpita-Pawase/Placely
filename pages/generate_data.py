import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine


class StudentData:
    def __init__(self, num_students=777, seed=57):
        self.num_students = num_students
        self.fake = Faker()
        Faker.seed(seed)
        self.students = []

    def generate_students(self):
        for i in range(self.num_students):
            student = {
                "Student ID": i + 1,
                "Name": self.fake.name(),
                "Email": self.fake.email(),
                "Contact": self.fake.msisdn()[:10],  # restrict to 10 digits
                "Batch": random.choice(["2023", "2024", "2025"]),
                "CGPA": round(random.uniform(6.0, 10.0), 2),
                "Soft Skills": ", ".join(random.sample(["Python", "Java", "C++", "JavaScript", "SQL"], 3)),
                "Soft Skills Score": random.randint(0, 50),
                "Programming Score": random.randint(0, 100),
                "Placement Ready": random.choice(["Yes", "NO"])
            }
            self.students.append(student)

    def to_dataframe(self):
        df = pd.DataFrame(self.students)
        df.reset_index(drop=True, inplace=True)  # ignore index
        return df

# Use the class
generator = StudentData()
generator.generate_students()
df = generator.to_dataframe()

# Save to MySQL database
engine = create_engine("mysql+mysqlconnector://root:KK1923@localhost/placely")
df.to_sql(name="students", con=engine, if_exists="replace", index=False)

print("Data successfully saved to MySQL!")

    
