# Flatten Nested  API Data/Dataframe with kpt_flatten_json Package

The kpt_flatten_json package simplifies the process of converting complex JSON API/dataframe data into a structured and easy-to-analyze flat dataframe. It offers a user-friendly function that transforms the complex JSON data into a tabular format, where each row represents a record and each column contains a specific attribute or value. This package is designed to make data analysis and processing tasks more accessible, even for users with limited programming experience. It allows you to extract relevant information from deep within the nested structure, enabling efficient data analysis and visualization. 


# kpt_flatten_json Package consists of two functions: 

     1. kpt_flatten_api(to flatten API data)

     2. kpt_flatten_json(to flatten dataframe)


# 1. kpt_flatten_api(to flatten API data)

Consider an API , which consists a list of nested dictionaries containing details about batters and toppings. We can use the kpt_flatten_api function to flatten this API data structure into a flat table as shown:

## API Information:

url='https://bxray-dev.kockpit.in:6789/userauthentication'

method='post'

uid = "xyz"

pwd = "12345"

body = {
     "userId": uid,
     "password": pwd
     }


## API Data
 
{
    "id": "0001",
    "type": "donut",
    "name": "Cake",
    "ppu": 0.55,
    "batters":
        {
            "batter":
                [
                    { "id": "1001", "type": "Regular" },
                    { "id": "1002", "type": "Chocolate" },
                    { "id": "1003", "type": "Blueberry" },
                    { "id": "1004", "type": "Devil's Choclate" }
                ]
        },
    "topping":
        [
            { "id": "5001", "type": "None" },
            { "id": "5002", "type": "Glazed" },
            { "id": "5005", "type": "Sugar" },
            { "id": "5007", "type": "Powdered Sugar" },
            { "id": "5006", "type": "Chocolate" },
            { "id": "5003", "type": "Chocolate" },
            { "id": "5004", "type": "Maple" }
        ]}


## Installation

$ [sudo] pip install kpt_flatten_json

## Function

kpt_flatten_api: Returns a flattened data from API

## Usage

To use the kpt_flatten_api function, import the function and pass the required API parameters:
```python

from kpt_flatten_json import *

flatdf= kpt_flatten_api(spark=spark,url=url,method=method,body=body,username=uid,password=pwd,sep="_")
```

## Flattened Data from API

| id| name| ppu | type | topping_id | topping_type               | batters_batter_id | batters_batter_type               |
| :-------- | :------- | :------------------------- |:-------- | :------- | :------------------------- |:-------- | :------- |
|0001|Cake|0.55|donut| 5001| None| 1001| Regular|
|0001|Cake|0.55|donut| 5001| None| 1002| Chocolate|
|0001|Cake|0.55|donut| 5001| None| 1003| Blueberry|
|0001|Cake|0.55|donut| 5001| None| 1004| Devil's Food|
|0001|Cake|0.55|donut| 5002| Glazed| 1001| Regular|
|0001|Cake|0.55|donut| 5002| Glazed| 1002| Chocolate|
|0001|Cake|0.55|donut| 5002| Glazed| 1003| Blueberry|

# Note:  

1. User need to pass spark session as variable in kpt_flatten_api function.

2. Function arguments must be same as specified below.

| Parameters| Type| 
| :-------- | :------- | 
| spark | SparkSession |
| url | String |
| method | Post or Get (String) |
| body | Dictionary |
| username | String |
| password | String |
| sep="_" | (fixed no other separator will be acceptable) |

# Methods To Fetch Data From API:
## 1. Basic Authentication (Using username , password or API Key):

url='https://bxray-dev.kockpit.in:6789/userauthentication'

method='post'

uid = "xyz"

pwd = "12345"

body = {
     "userId": uid,
     "password": pwd
     }

flatdf= kpt_flatten_api(spark=spark,url=url,method=method,body=body,username=uid,password=pwd,sep="_")


## 2. With OAuthToken Authentication/Bearer Token (Using authToken):

authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJEb21haW4iOiJUQTAxMzAiLCJpYXQiOjE2NzU2NzM2NTksImV4cCI6MTY3ODI2NTY1OX0.t8A8vYWiIinyCWNOlk6q2IA-C2KajvUUTB8uD_4dQOM'

url = 'https://bxray-dev.kockpit.in:6789/test/tokenauth'

body = {}

method="post" or "get"

flatdf= kpt_flatten_api(spark=spark,url=url,method=method,body=body,authToken=authToken,sep="_")

## 3. Without  Authentication (Using url only):

url='https://bxray-dev.kockpit.in:6789/test/withoutParameter'

method="post" or "get"

flatdf= kpt_flatten_api(spark=spark,url=url,method=method,sep="_")


## Example Code:

import requests

from pyspark.sql import SparkSession, Row

import json

from pyspark.sql.functions import *

from pyspark.sql.types import *

from FlattenApi_func import flatten_api

spark = SparkSession.builder.appName("ReadDarwinAPIWithAuth").getOrCreate()

username = "example"

password = "examplepassword"

api_key='ExampleAPIKEY'

processed_from='04-01-2023 00:00:00'

processed_to='04-01-2023 23:55:00'

url="https://example"

method="post"

body = {
    "api_key": api_key,
    "processed_from": processed_from,
    "processed_to": processed_to
    }

flatdf= flatten_api(spark=spark,url=url,method=method,body=body,username=username,password=password,sep="_")

flatdf.show(2)

# 2. kpt_flatten_json(to flatten dataframe):

## Example
Consider a list of nested dictionaries containing details about batters and toppings. We can use the kpt_flatten_json function to flatten this JSON data structure into a flat table as shown:

data = 
[  
     
    {
    "id": "0001",
    "type": "donut",
    "name": "Cake",
    "ppu": 0.55,
    "batters":
        {
            "batter":
                [
                    { "id": "1001", "type": "Regular" },
                    { "id": "1002", "type": "Chocolate" },
                    { "id": "1003", "type": "Blueberry" },
                    { "id": "1004", "type": "Devil's Choclate" }
                ]
        },
    "topping":
        [
            { "id": "5001", "type": "None" },
            { "id": "5002", "type": "Glazed" },
            { "id": "5005", "type": "Sugar" },
            { "id": "5007", "type": "Powdered Sugar" },
            { "id": "5006", "type": "Chocolate" },
            { "id": "5003", "type": "Chocolate" },
            { "id": "5004", "type": "Maple" }
        ]}

]

# Convert the data to a complex DataFrame

complexdf = spark.createDataFrame(data=data)

## Complex Dataframe


| batters| id| name | ppu | topping| type               |
| :-------- | :------- | :------------------------- |:-------- | :------- | :------------------------- |
| {[{1001, Regular}... | 0001 | Cake|0.55 | [{5001, None}, {5... | donut|

## Installation

$ [sudo] pip install kpt_flatten_json

## Function

kpt_flatten_json: Returns a flattened dataframe


# Flatten the DataFrame
## Usage
To use the kpt_flatten_json function, import the function and pass in your complex DataFrame as a parameter:
```python
from kpt_flatten_json import *

flatdf= kpt_flatten_json(complexdf)
```


## Flattened Dataframe
| id| name| ppu | type | topping_id | topping_type               | batters_batter_id | batters_batter_type               |
| :-------- | :------- | :------------------------- |:-------- | :------- | :------------------------- |:-------- | :------- |
|0001|Cake|0.55|donut| 5001| None| 1001| Regular|
|0001|Cake|0.55|donut| 5001| None| 1002| Chocolate|
|0001|Cake|0.55|donut| 5001| None| 1003| Blueberry|
|0001|Cake|0.55|donut| 5001| None| 1004| Devil's Food|
|0001|Cake|0.55|donut| 5002| Glazed| 1001| Regular|
|0001|Cake|0.55|donut| 5002| Glazed| 1002| Chocolate|
|0001|Cake|0.55|donut| 5002| Glazed| 1003| Blueberry|