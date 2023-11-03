import requests
def fun():
    url ="https://reqres.in/api/users?page=2"
    response=requests.get(url)
    print(response.json())
fun()       
