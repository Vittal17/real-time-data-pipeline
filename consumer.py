import boto3
import json
import time

# Connect to Kinesis and S3 (update region if not us-east-1)
kinesis_client = boto3.client('kinesis', region_name='us-east-1')
s3_client = boto3.client('s3', region_name='us-east-1')

# Get shard ID dynamically
try:
    stream_desc = kinesis_client.describe_stream(StreamName='StreamTweet')
    shard_id = stream_desc['StreamDescription']['Shards'][0]['ShardId']
    print(f"Using shard ID: {shard_id}")
except Exception as e:
    print(f"Error describing stream: {e}")
    exit()

# Get shard iterator
try:
    response = kinesis_client.get_shard_iterator(
        StreamName='StreamTweet',  # Fixed to match producer
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )
    shard_iterator = response['ShardIterator']
except Exception as e:
    print(f"Error getting shard iterator: {e}")
    exit()

# Process the stream
while True:
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,
        Limit=10
    )
    shard_iterator = response['NextShardIterator']

    for record in response['Records']:
        tweet = json.loads(record['Data'])
        print(f"Processed tweet: {tweet}")

        filename = f"threat_{tweet['user']}_{int(tweet['timestamp'])}.json"
        try:
            s3_client.put_object(
                Bucket='farzitweet',
                Key=filename,
                Body=json.dumps(tweet)
            )
            print(f"Saved to S3: {filename}")
        except Exception as e:
            print(f"Error saving to S3: {e}")

    time.sleep(1)