# contest_of_champions
Management system for the gladiatorial event organised by Grandmaster on Sakaar :new_moon:

# Running the application

- Checkout code on /opt/contest_of_champions_v2 on local computer
- Build the containers: `docker-compose -f docker-compose-prod.yml build`
- Start the app: `docker-compose -f docker-compose-prod.yml up -d`
- API is available on http://localhost:80

# To run tests

- `docker exec -it contest_api_web python3 -m pytest -v`

# API Documentation

- POST **/heroes**

    Register a new hero.<br>
    This request must be authenticated using an authentication token with Grandmaster permissions.<br>
    The body must contain a JSON object that defines `name`, `password` and `group` fields.<br>
    In the case of success a status code 201 is returned.<br>
    The response body contains a JSON object with the newly added user.<br>
    Also `Location` header contains the URI of the new user.<br>
 
- GET **/heroes**

    Return list of users.<br>
    This request must be authenticated using an authentication token with Grandmaster permissions.<br>
    In the case of success a status code 200 is returned.<br>
    On failure status code 400 is returned<br>
    
- GET **/heroes/<public_id>**

    Return a hero.<br>
    This request must be authenticated using an authentication with Grandmaster permissions token.<br>
    In the case of success a status code 200 is returned.<br>
    The response body contains a JSON object with the requested user.
    On failure status code 400 is returned.
    
- PATCH **/heroes/<public_id>**
   
   Kill a hero.<br> 
   This request must be authenticated using an authentication with Grandmaster permissions token.<br>
   Return status code 204. It means that the server has successfully fulfilled the request and there is no additional content to send in the response.
   
   
- DELETE **/heroes/<public_id>**

   Delete a hero from the gladiatorial event.<br>
   This request must be authenticated using an authentication token with Grandmaster permissions.<br>
   Return status code 204. It means that the server has successfully fulfilled the request and there is no additional content to send in the response.
    
- GET **/login**

    Return an authentication token.<br>
    This request must be authenticated using a HTTP Basic Authentication Header.<br>
    In the case of success a JSON object with a field `token` is returned.<br>
    This token is used to get protected resources.<br>
    On failure status code 401 is returned.<br>
    
    
- POST **/fights**

    Register a new fight between two heroes.<br>
    This request must be authenticated using an authentication token with Grandmaster permissions.<br>
    In the case of success a JSON object with result of this fight is returned.<br>
    On failure status code 401 is returned.


- GET **/ranking**

    Return the ranking of living heroes.<br>
    This request must be authenticated using an authentication token with normal permissions<br>
    In the case of success a status code 200 is returned.<br>
    On failure status code 401 is returned.<br>
    

- GET **/deaths**

    Return the sorted list of those lost in battles.<br>
    This request must be authenticated using an authentication token with Grandmaster permissions<br>
    In the case of success a status code 200 is returned.<br>
    On failure status code 401 is returned.<br>

    
# Some examples

`curl` command to log in as a `Grandmaster` with password:<br>
(Credentials of existing users are located in migrations directory)

```
$ curl -u Grandmaster:grandpass -i -X GET http://localhost/login

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 191
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Tue, 19 Jun 2018 03:13:45 GMT

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI0MjJlYTFjMi00NzExLTRjMzYtYmM5MC0zNzRjMjI4OTkyNWEiLCJleHAiOjE1MjkzNzg5MjV9.WObcyClF8dBceUvl93UJMoyswVYUNY269K5LPJuSax8"
}

```
And now we can use the token to get access to protected resources<br>
For example: <br>
`curl` command to register a new hero
```
$ curl -i -X POST http://localhost/heroes -H "Content-Type: application/json" -H "x-access-token:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI0MjJlYTFjMi00NzExLTRjMzYtYmM5MC0zNzRjMjI4OTkyNWEiLCJleHAiOjE1MjkzNzg5MjV9.WObcyClF8dBceUvl93UJMoyswVYUNY269K5LPJuSax8" -d  '{"name": "Presidente", "password": "123", "group": "HUMAN"}' 

HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 125
Location: http://localhost/heroes/1cf62ef4-212e-484c-a766-3ecda8b4a594
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Tue, 19 Jun 2018 03:37:40 GMT

{
  "group": "HUMAN", 
  "health": 100, 
  "name": "Presidente", 
  "public_id": "1cf62ef4-212e-484c-a766-3ecda8b4a594"
}

```

`curl` command to get list of heroes

```
$ curl -i -X GET http://localhost/heroes -H "x-access-token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI0MjJlYTFjMi00NzExLTRjMzYtYmM5MC0zNzRjMjI4OTkyNWEiLCJleHAiOjE1MjkzNzg5MjV9.WObcyClF8dBceUvl93UJMoyswVYUNY269K5LPJuSax8"

HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 551
Server: Werkzeug/0.14.1 Python/3.6.5
Date: Tue, 19 Jun 2018 03:21:52 GMT

[
  {
    "group": "NONE", 
    "health": 100, 
    "name": "Grandmaster", 
    "public_id": "422ea1c2-4711-4c36-bc90-374c2289925a"
  }, 
  {
    "group": "MUTANT", 
    "health": 100, 
    "name": "Hulk", 
    "public_id": "8eead8ef-65c8-45c5-8095-d1c055cc6d19"
  }, 
  {
    "group": "MYSTIC", 
    "health": 100, 
    "name": "Guilotine", 
    "public_id": "79b251d7-a6ad-4784-b417-1c3ee78b348d"
  }, 
  {
    "group": "HUMAN", 
    "health": 100, 
    "name": "Grzesiek", 
    "public_id": "77a9ae20-b5f1-41ba-b40d-f1252c5883d6"
  }
]
```