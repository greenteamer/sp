

import json
i = 0
list = []
for image in images:
    list.append(image.url())
    i += 1

response_data = json.dumps(list)

# return an HttpResponse with the JSON and the correct MIME type
return HttpResponse(response_data, mimetype='application/json')
return HttpResponse('{"0":"%s"}' % images.url() )








