import json
json.loads(urllib.request.urlopen(urllib.request.Request('https://shapeshift.io/rate')).read().decode('utf-8'))