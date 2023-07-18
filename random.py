# AWS Lambda Version
from random import choices

def lambda_handler(event, context):
    res_msg = {}
    status = event['pathParameters']['status']
    population = [status, '200']
    status = event['pathParameters']['status']
    if event['queryStringParameters']:   
        rate = event['queryStringParameters'].get('rate')
        rate = (int(rate))/100
        weights = [rate, 1-rate]
    else:
        weights = [.5, .5]
    
    status = choices(population, weights)[0]

    res_msg['statusCode'] = int(status)

    #res_msg['body']= json.dumps(body_res, ensure_ascii=False)
    return (res_msg)

