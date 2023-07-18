# AWS Lambda Version
from datetime import datetime, timedelta
req_list = {}

def lambda_handler(event, context):
    res_msg = {}
    client = event['pathParameters']['client']
    if event['queryStringParameters']:        
        rate = event['queryStringParameters'].get('rate')
        rate = int(rate)
    else:
        rate = 1
    grant = throttling (client, rate)
    if grant:
        status = 200
    else:
        status = 429        

    res_msg['statusCode'] = int(status)

    #res_msg['body']= json.dumps(body_res, ensure_ascii=False)
    return (res_msg)


def throttling (client, rate):  
    global req_list
    reqs = req_list.get(client)
    if not reqs:
        reqs = []
        req_list[client] = reqs
    counter = 0
    now = datetime.now()
    delta = timedelta(seconds = 60)
    threashold = timedelta(minutes = 10)
    for timestamp in reqs:
        if now - timestamp < delta :
            counter += 1
        # Clean timestamps older then threashold
        if now - timestamp > threashold:
            del reqs[reqs.index(timestamp):]
            break
    # Add timestamp always at the beginning
    if counter >= rate:
        return False
    else:
        reqs.insert(0,datetime.now())
        return True
