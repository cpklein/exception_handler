# AWS Lambda Version
import time

def lambda_handler(event, context):
    res_msg = {}
    status = event['pathParameters']['status']
    if event['queryStringParameters']:
        delay = event['queryStringParameters'].get('delay')
        time.sleep(int(delay))
    res_msg['statusCode'] = int(status)

    #res_msg['body']= json.dumps(body_res, ensure_ascii=False)
    return (res_msg)


