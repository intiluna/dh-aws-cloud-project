import csv
import boto3
import os

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

# Define the name of your DynamoDB table
# USERS_TABLE = os.environ['USERS_TABLE']

def upload_records_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            userId = row['userId']
            upload_record_to_dynamodb(name, userId)

def upload_record_to_dynamodb(name, userId):
    try:
        response = dynamodb.put_item(
            TableName=USERS_TABLE,
            Item={
                'userId': {'S': userId},
                'name': {'S': name}
            }
        )
        print(f"Uploaded record: {name}, {userId}")
    except Exception as e:
        print(f"Failed to upload record: {name}, {userId}. Error: {e}")

if __name__ == "__main__":
    csv_file = "records_to_populate_db.csv"  # Path to your CSV file
    upload_records_from_csv(csv_file)
