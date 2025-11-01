import requests
          
collection_id = 2          
url = "https://api-production.data.gov.sg/v2/public/api/collections/{}/metadata".format(collection_id)
        
response = requests.get(url)
print(response.json())