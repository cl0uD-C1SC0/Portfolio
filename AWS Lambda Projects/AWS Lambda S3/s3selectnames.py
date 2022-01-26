import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    r = s3.select_object_content(
        Bucket='wildguru-select',
        Key='NationalNames2000-2014.csv.gz',
        ExpressionType='SQL',
        Expression="select * from s3object n where n.\"Name\" like 'Stephen' and n.\"Sex\" like '%M%'",
        InputSerialization = {
            'CompressionType': 'GZIP',
            'CSV': {
                "FileHeaderInfo": "Use"
            }
            
        },
        OutputSerialization = {'CSV': {}},
    )

    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")
            print(statsDetails['BytesScanned'])
            print("Stats details bytesProcessed: ")
            print(statsDetails['BytesProcessed'])

