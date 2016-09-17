from os import path


def handler(event, context):
    if 'requested_file' not in event:
        raise Exception("Bad Request: no 'requested_file' submitted")

    requested_file = event['requested_file']
    request_path = path.join("static", requested_file)

    if not path.exists(request_path):
        raise Exception("Bad Request: The requested file does not exist")

    with open(request_path) as f:
        return "".join([line for line in f])
