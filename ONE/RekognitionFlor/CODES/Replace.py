from __future__ import print_function
import json
import base64

print('Loading function')


def lambda_handler(event, context):
    output = []
    for record in event['records']:
        payload = base64.b64decode(record['data'])
        payload = json.loads(payload)
        s = payload['StatusTime']
        s = s.replace(' ', 'T')
        s = s[:-4]
        data = {
            'Name': payload['Name'],
            'StatusTime': s,
            'Distance': payload['Distance'],
            'MinMagicPoints': payload['MinMagicPoints'],
            'MaxMagicPoints': payload['MaxMagicPoints'],
            'MinHealthPoints': payload['MinHealthPoints'],
            'MaxHealthPoints': payload['MaxHealthPoints'],
        }
        data = json.dumps(data)
        b_data=data.encode()
        b64encoded=base64.b64encode(b_data)
        b64encoded = b64encoded.decode()
        print(b64encoded)
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': b64encoded,
            'approximateArrivalTimestamp': record['approximateArrivalTimestamp']
        }
        output.append(output_record)

    print('Successfully processed {} records.'.format(output))

    return {'records': output}


