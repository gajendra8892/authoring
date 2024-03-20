import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker
import uuid

# Initialize Faker to generate fake data
fake = Faker()

# Function to generate random datetime within specified range
def random_datetime(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 24*60*60 - 1)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

# Specify date range
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 1, 1)

# Read existing data from Excel file
existing_data = pd.read_excel('D:\\Data\\New folder\\sample data\\Book1.xlsx')

# Number of records
num_records = 25000

# Generate random data for search_ts_est column
search_ts_est = [random_datetime(start_date, end_date) for _ in range(num_records)]

# Generate random data for search_reference_id column
search_reference_id = [str(uuid.uuid4()) for _ in range(num_records)]

# Define search regions and their percentages
search_regions = {
    "America": {
        "US": 80.0,
        "Canada": 10.0,
        "Brazil": 5.0,
        "Mexico": 2.5,
        "Argentina": 2.5,
    },
    "Europe Big 5": ["English UK", "Germany", "France", "Italy", "Spain"],
    "Rest of Europe": [
        "Austria", "Belgium", "Czech", "Denmark", "Finland", "Greece", "Hungary", "Ireland",
        "Luxembourg", "Netherland", "Norway", "Poland", "Portugal", "Romania", "Slovenia", "Sweden", "Switzerland",
    ],
    "IMG": ["Australia", "New Zealand", "India", "South Africa", "Philippines", "UAE", "Thailand", "Vietnam"]
}

# Language mappings
country_to_language = {
    "US": "English",
    "English UK": "English",
    "Germany": "German",
    "France": "French",
    "Italy": "Italian",
    "Spain": "Spanish",
    "Mexico": "Spanish",
    "Ireland": "English",
    "Australia": "English",
    "Philippines": "English",
    "India": "English",
    "Denmark": "Danish",
    "Poland": "Polish",
    "Czech": "Czech",
    "Finland": "Finnish",
    "Hungary": "Hungarian",
    "Greece": "Greek",
    "Norway": "Norwegian",
    "Slovenia": "Slovenian",
    "Romania": "Romanian",
    "Sweden": "Swedish",
    "Dutch": "Dutch",
    "Austria": "German",
    "Brazil": "Portuguese",
    "Turkey": "Turkish",
    "UAE": "Arabic",
    "Portugal": "Portuguese",
    "Switzerland": "German",
    "Belgium": "Dutch",
    "Canada": "English",
    "Netherland": "Dutch",
    "South Africa": "English",
    "New Zealand": "English",
    "Luxembourg": "Luxembourgish",
    "Vietnam": "Vietnamese",
    "Thailand": "Thai",
    "Europe": "Russian",
    "Argentina": "Spanish",
}

# Define touchpoint codes and their percentages
touchpoint_codes = {
    "CAF": 75.0,
    "AAF": 20.0,
    "DAF": 2.5,
    "CAL": 2.5,
}

# Define search initiated by mappings
search_initiated_by_map = {
    "CAF": "Consumers",
    "AAF": "Agents",
    "CAL": "Consumers",
    "DAF": "Dealers"
}

# Function to generate random touchpoint code based on specified percentages
def generate_touchpoint_code():
    codes = list(touchpoint_codes.keys())
    weights = list(touchpoint_codes.values())
    return random.choices(codes, weights=weights)[0]

# Function to generate random search country based on specified region
def generate_search_country(region):
    if region == "America":
        countries = list(search_regions[region].keys())
        weights = list(search_regions[region].values())
        return random.choices(countries, weights=weights)[0]
    else:
        return random.choice(search_regions[region])

# Function to generate language based on country
def generate_language(country):
    return country_to_language.get(country, "English")

# Generate random data for search_region, search_country, language, and touchpoint_code columns
search_region = [random.choices(list(search_regions.keys()))[0] for _ in range(num_records)]
search_country = [generate_search_country(region) for region in search_region]
language = [generate_language(country) for country in search_country]
touchpoint_code = [generate_touchpoint_code() for _ in range(num_records)]

# Generate random data for search_initiated_by column based on touchpoint codes
search_initiated_by = [search_initiated_by_map[code] for code in touchpoint_code]

# Duplicate existing data for columns where existing data exists
existing_data_length = len(existing_data)
existing_data_repeated = existing_data.iloc[:num_records % existing_data_length]._append(
    existing_data.sample(n=num_records - num_records % existing_data_length, replace=True),
    ignore_index=True
)

# Create DataFrame from repeated existing data
existing_data_repeated = existing_data_repeated.loc[:num_records - 1]

# Generate random data for other columns
topics_viewed_per_user_session = [random.randint(1, 20) for _ in range(num_records)]
keyword_search_per_user_session = [random.randint(1, 10) for _ in range(num_records)]

# Generate topic_review_yes_cnt and topic_review_no_cnt columns based on survey_rating
topic_review_yes_cnt = [1 if rating == 5 else 0 for rating in existing_data_repeated['Survey Rating']]
topic_review_no_cnt = [1 if rating == 1 else 0 for rating in existing_data_repeated['Survey Rating']]

# Generate date_key column with the format DDMMYYYY from search_ts_est
date_key = [date.strftime("%d%m%Y") for date in search_ts_est]

# Combine all the data into a DataFrame
random_data = {
    'search_ts_est': search_ts_est,
    'Search_Reference_ID': search_reference_id,
    'topic_id': existing_data_repeated['Topic ID'].tolist(),
    'topic_name': existing_data_repeated['Topic Name'].tolist(),
    'topic_label': existing_data_repeated['Topic Label'].tolist(),
    'short_description': existing_data_repeated['Short description'].tolist(),
    'language': language,
    'search_initiated_by': search_initiated_by,
    'touchpoint_code': touchpoint_code,
    'user_utterance': existing_data_repeated['User Utterance'].tolist(),
    'feedback': existing_data_repeated['Feedback'].tolist(),
    'survey_rating': existing_data_repeated['Survey Rating'].tolist(),
    'search_region': search_region,
    'search_country': search_country,
    'search_status': [random.choice(['Completed', 'Failed', 'Pending']) for _ in range(num_records)],
    'analytics_tag': ['' for _ in range(num_records)],  # Blank analytics tag
    'consumer_device': [random.choice(['Mobile', 'Desktop', 'Tablet']) for _ in range(num_records)],
    'keyword_search_per_user_session': keyword_search_per_user_session,
    'topics_viewed_per_user_session': topics_viewed_per_user_session,
    'error_description': ['' for _ in range(num_records)],  # Blank error description
    'source_name': ['RTE' for _ in range(num_records)],
    'load_date_est': [datetime.now().strftime("%Y-%m-%d %H:%M:%S") for _ in range(num_records)],
    'sp_agent_id': [fake.random_number(digits=4) for _ in range(num_records)],
    'topic_review_yes_cnt': topic_review_yes_cnt,
    'topic_review_no_cnt': topic_review_no_cnt,
    'date_key': date_key
}

# Create DataFrame from random data
random_data_df = pd.DataFrame(random_data)

# Save to Excel
random_data_df.to_excel('C:\\Users\\Gajendra\\Desktop\\Ford_authoring\\Dummy\\topic_dummy.xlsx', index=False)
