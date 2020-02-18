# Aviasales anagrams web server

Run all containers in daemon mode:
```
docker-compose up -d
```  

## Unit tests
```
docker-compose exec web python -m unittest app/tests.py
```

## API methods

### List anagrams:
```
curl 'localhost:8080/get?word=foobar' 
```
* Returns `null` or an array of anagrams in json.
* Word from query params is not case-sensitive

### Create anagram:
```
curl localhost:8080/load -d '["foobar", "aabb", "baba", "boofar", "test"]'
```
* Accept json array in request body
* Return 201 and empty array if request successful
* Return 400 if request body does not contains array of strings in json format 
