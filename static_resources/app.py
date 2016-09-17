from os import path


def handler(event, context):
    if 'requested_file' not in event:
        raise Exception("Bad Request: no 'requested_file' submitted")
    if 'request_type' not in event:
        raise Exception("Bad Request: no 'request_type' submitted")

    request_type = event['request_type']
    if request_type not in {'js', 'html'}:
        raise Exception("Bad Request: request type '%s' is not valid" % (request_type, ))

    requested_file = event['requested_file']
    request_path = path.join("static", request_type, requested_file)

    if not path.exists(request_path):
        raise Exception("Bad Request: The requested file does not exist")

    with open(request_path) as f:
        return "".join([line for line in f])
