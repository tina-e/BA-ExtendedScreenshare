import http.client as client

connection = client.HTTPConnection('192.168.178.136', 5000)
connection.connect()

while True:
    connection.request('GET', 'http://192.168.178.136:8000/mouseevent')
    response = connection.getresponse()
    print(response.read())
#connection.endheaders()
