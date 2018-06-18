# contest_of_champions
Management system for the gladiatorial event organised by Grandmaster on :new_moon:

# Running the application

- Checkout code on /opt/contest_of_champions_v2 on local computer
- Build the containers: `docker-compose -f docker-compose-prod.yml build`
- Start the app: `docker-compose -f docker-compose-prod.yml up -d`
- API is available on http://localhost:80

# Running the tests
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

    
# Examples

