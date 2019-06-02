# Django REST API Project with Insurance data

A simple analytics platform for an Insurance company using the Kaggle dataset Agency Performance Model.

# Description

The Insurance REST API is a platform that allows anybody to search and query about the insurance dataset.

## API Endpoints:

Django Token based authentication has been implemented here. The token to access the API is:
d110c55abdfe0cdc88359b0d718288cb06513903

Please take a note of this token which will be needed to request data from this API.

### Token request endpoint:

* [Api type] - POST
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/login
* [Parameters] -                                                                                                                         
                     username : demo                                                                                                     
                     password: demo1234                                                                                                   
               
* Sample code to call the API 

```sh
import requests
url = "http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/login"
payload = "username=demo&password=demo1234"
headers = {'Content-Type': "application/x-www-form-urlencoded",'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```

### Detail data endpoint

* [Api type] - POST
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/detaildata
* [Parameters] -                                                                                                                       
                     agencyid: 5748                                                                                                  
                         year: 2012                                                                                                   
                        month: 12                                                                                                       
                        state: PA
              
* Sample code to call the API 
```sh
import requests
url = "http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/detaildata"
payload = "agencyid=5748&year=2012&month=12&state=PA"
headers = {'Authorization': "Token d110c55abdfe0cdc88359b0d718288cb06513903",'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```

### Detail agency data endpoint: 

* [Api type] - POST
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/detailagencydata
* [Parameters] - 
               agencyid: 5748 
               
* Sample code to call the API 
```sh
import requests
url = "http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/detailagencydata"
payload = "agencyid=5748"
headers = {
    'Authorization': "Token d110c55abdfe0cdc88359b0d718288cb06513903",
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```
### vendor premium endpoint

* [Api type] - POST
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/vendorpremium
* [Parameters] - 
               agencyid: 5748
      
* Sample code to call the API 
```sh
import requests
url = "http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/vendorpremium"
payload = "vendor=A"
headers = {'Authorization': "Token d110c55abdfe0cdc88359b0d718288cb06513903",'cache-control': "no-cache"}
response = requests.request("POST", url, data=payload, headers=headers)
print(response.text)
```

### Provides an aggregated report based on production line and state

* [Api type] - GET
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/stateproductionlinepremium
* [Parameters] - 
                 No
* Sample code to call the API 
```sh
import requests
url = "http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/stateproductionlinepremium"
payload = ""
headers = {'cache-control': "no-cache"}
response = requests.request("GET", url, data=payload, headers=headers)
print(response.text)
```

### CSV eeport export

* [Api type] - GET
* [End Point to call] - endpoint: http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/csvreportexport?startdate=2014-01-01&enddate=2014-12-01
* [Parameters] - 
              ```sh
               startdate: 2014-01-01
               enddate: 2014-12-01
              ```

## Swagger Api Implementaion For Insurance Django Rest Api
[Swagger for Insurance Django Rest Api](http://ec2-54-159-5-43.compute-1.amazonaws.com:8000/insurance/api/v0/swagger-docs/)
Swagger url for insurance Dejango rest Api has been developed. It's basically used for api development. By Clicking the above url anyone can able to see apis which are exposed without a token.

## Deployment
The whole system has deployed into Amazon EC2 (Amazon web Service).
