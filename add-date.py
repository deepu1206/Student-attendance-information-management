import json
import boto3

TableName = "student_info"
dynamodb_resource = boto3.resource('dynamodb')
table = dynamodb_resource.Table(TableName)

def lambda_handler(event, context):
    
    id = event['id']
    a_date = event['date']
    try:
        response = table.get_item(TableName=TableName, Key={'id': id})
    except Exception as e:
        raise Exception (f"Exception occurred while calling 'db_get_item' function for Table name {TableName} - {e}")
    
    if 'Item' not in response.keys():
        return {
            'statusCode': 404,
            'body': f'Student Id {id} not found in our Records.....'
        }
    
    pull_data = response['Item']
    print (pull_data)
    if 'attended_date' not in pull_data.keys():
        pull_data['attended_date'] = a_date.split()
        return db_put_item(pull_data )
    else:
        return update_db(id, a_date)


def db_put_item(Item_dict):
    try:
        response = table.put_item(Item=Item_dict)
        return {
        'statusCode': 200,
        'body': json.dumps('Added date to db')
        }
    except Exception as e:
        raise Exception(f"Exception occurred while calling 'db_put_item' function for Table name {TableName} - {e}")


def update_db(id, n_date):
    try:
        response = table.update_item(
            Key={
                'id': id,
            },
            UpdateExpression="SET #ri = list_append(#ri, :vals)",
            ExpressionAttributeNames={
                    '#ri': 'attended_date',
            },
            ExpressionAttributeValues = {
                ':vals': [n_date],
            },
            ReturnValues="UPDATED_NEW"
        )
        return {
        'statusCode': 200,
        'body': json.dumps('Updated DB!')
        }
    except Exception as e:
        raise Exception(f"Exception occurred while calling 'db_update_item' function for Table name {TableName} - {e}")