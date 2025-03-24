import boto3
import json
import time
import random

# Connect to Kinesis
kinesis_client = boto3.client('kinesis', region_name='us-east-1')

# Fake user names and messages
users = ['Alice', 'Bob', 'Charlie', 'Dia']
messages = ['Loving this weather!', 'Just coded something cool.', 'Python rocks!', 'AWS is fun.']

def generate_tweet():
    tweet = {
        'user': random.choice(users),
        'message': random.choice(messages),
        'timestamp': time.time()
    }
    return tweet

# Send data to Kinesis
while True:
    tweet = generate_tweet()
    tweet_json = json.dumps(tweet)  # Convert to JSON string
    print(f"Sending: {tweet_json}")

    kinesis_client.put_record(
        StreamName='StreamTweet',
        Data=tweet_json,
        PartitionKey='partitionkey'  # Simple key to group data
    )
    time.sleep(1)  # Wait 1 second before sending the next