import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)
s3_client = boto3.client('s3')

BUCKET_NAME = 'liminal-s3-browser-prototype'
URL_EXPIRATION_SECONDS = 3600  # Set the expiration time for the signed URLs (1 hour in this example)


@app.route('/list_objects', methods=['GET'])
def list_objects():
    prefix = request.args.get('prefix', '')  # For filtering based on folder or filename
    max_items = int(request.args.get('max_items', 1000))  # Number of items per page
    continuation_token = request.args.get('continuation_token', None)  # Token for pagination

    s3_params = {
        'Bucket': BUCKET_NAME,
        'Prefix': prefix,
        'MaxKeys': max_items,
        'Delimiter': '/',
    }
    if continuation_token:
        s3_params['ContinuationToken'] = continuation_token

    response = s3_client.list_objects_v2(**s3_params)

    return_data = {
        'Items': [],
        'NextContinuationToken': response.get('NextContinuationToken', None)  # Token for next set of results
    }

    if 'CommonPrefixes' in response:
        for item in response['CommonPrefixes']:
            return_data['Items'].append({
                'Name': item['Prefix'],
                'Size': 0,
                'DateUpdated': None
            })

    if 'Contents' in response:
        for item in response['Contents']:
            return_data['Items'].append({
                'Name': item['Key'],
                'Size': item['Size'],
                'DateUpdated': item['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
            })

    return jsonify(return_data)

@app.route('/list_all_objects', methods=['GET'])
def list_all_objects():
    prefix = request.args.get('prefix', '')  # For filtering based on folder or filename

    s3_params = {
        'Bucket': BUCKET_NAME,
    }

    all_items = []

    while True:
        response = s3_client.list_objects_v2(**s3_params)

        if 'Contents' in response:
            for item in response['Contents']:
                all_items.append({
                    'Name': item['Key'],
                    'Size': item['Size'],
                    'DateUpdated': item['LastModified'].strftime('%Y-%m-%d %H:%M:%S')
                })

        # Check if there are more items to fetch
        continuation_token = response.get('NextContinuationToken', None)
        if not continuation_token:
            break

        s3_params['ContinuationToken'] = continuation_token

    return jsonify({
        'Items': all_items,
        'TotalCount': len(all_items),
        'NextContinuationToken': None
    })

if __name__ == '__main__':
    app.run(debug=True)
