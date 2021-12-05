# url-short
## Description
 a flask project for generating short url from long url with functionality to check stats and keyword search on the Url.
## Installation
create a virtualenv and activate the virtualenv 
  ```bash
  pip install -r requirements.txt
  ```
## Configuration
**.env** file is used to manage the database uri for sql databases.
By default it uses **sqlite** database if **DB_URI** is not set

set the **DB_URI** to your database uri 

## Running
```bash
python main.py
```
## API Endpoints
1. POST   / 
   content-type : json/application
   data_format = {"url": url_to_short }
   
2. GET  short_url/stats  
   get all the stats about the url
   
3. GET  /search?q=keyword
   get all the urls having a keyword specified in the q
