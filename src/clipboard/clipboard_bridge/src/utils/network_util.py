from requests import get

def get_public_ipv4(port=None):
    ip = get('https://api.ipify.org').text
    if port is None:
        return get_complete_http_path(ip)
    else:
        return get_complete_http_path(ip, port)

def get_complete_http_path(str_in, port=None):
    if port is not None:
        return 'http://' + str_in + ':' + str(port) + '/'
    else:
        return 'http://' + str_in + '/'
