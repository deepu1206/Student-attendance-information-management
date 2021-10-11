import json
import boto3
 
def lambda_handler(event, context):
    
    TableName = "student_info"
    id = event['id']
    
    dynamodb_resource = boto3.resource('dynamodb')
    table = dynamodb_resource.Table(TableName)
    try:
        response = table.get_item(TableName=TableName, Key={'id': id})
    except Exception as e:
        raise Exception (f"Exception occurred while calling 'db_get_item' function for Table name {TableName} - {e}")
    
    if 'Item' in response.keys():
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    
    return {
        'statusCode': 404,
        'body': f'Student Id {id} not found in our Records.....'
    }

#def check_avg():