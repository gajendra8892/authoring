import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Generate fake data
fake = Faker()

# Touch Point probabilities
touch_points = ["CAF", "AAF", "DAF", "CAL"]
touch_point_weights = [75.0, 20.0, 2.5, 2.5]

# Language options
languages = [
    "Romanian", "English", "Spanish", "Italian", "Greek", "Dutch", "German", 
    "Norwegian", "Luxembourgish", "Portuguese", "Thai", "French", "Dutch", 
    "French", "Hungarian", "Vietnamese", "Danish", "Polish", "Slovenian", 
    "English", "Swedish", "Czech", "Turkish", "Finnish", "Russian", "Arabic"
]

def generate_touch_point():
    return random.choices(touch_points, weights=touch_point_weights)[0]

def generate_language():
    return random.choice(languages)

def generate_task_topic():
    # Generate random task topic
    return fake.sentence()

def generate_fake_data():
    return {
        "Topic ID": fake.uuid4(),
        "Version": random.randint(1, 10),
        "Touch Point": generate_touch_point(),
        "Language": generate_language(),
        "Status": fake.random_element(elements=("Pending", "Completed", "In Progress")),
        "Task ID": fake.uuid4(),
        "Task Action": fake.random_element(elements=("Create", "Update", "Delete")),
        "Task Topic": generate_task_topic(),
        "Task Assignee": fake.name(),
        "Task Status": fake.random_element(elements=("Pending", "Completed", "In Progress")),
        "Task Creator": fake.name(),
        "Create Date": fake.date_this_decade(),
        "Finish Date": fake.date_between(start_date='today', end_date='+30d'),
        "Task Comments": fake.text(max_nb_chars=200),
        "Task User": fake.name(),
        "Date/Time": fake.date_time_this_year(),
        "Task Due Date": fake.date_between(start_date='today', end_date='+30d'),
        "Author Name": fake.name(),
        "Original Date Published": fake.date_this_decade(),
        "Category Code": fake.random_element(elements=("A", "B", "C", "D")),
        "Last Action Performed": fake.random_element(elements=("Create", "Update", "Delete")),
        "Last Updated By": fake.name(),
        "Last Updated Date": fake.date_time_this_year(),
    }

# Generate 10,000 records
data = [generate_fake_data() for _ in range(10000)]

# Convert data to DataFrame
df = pd.DataFrame(data)

# Export DataFrame to Excel file
excel_file = "C:\\Users\\Gajendra\\Desktop\\Ford_authoring\\Dummy\\authoring_dummy.xlsx"
df.to_excel(excel_file, index=False)

print(f"Generated {len(data)} records. Data exported to '{excel_file}'")
