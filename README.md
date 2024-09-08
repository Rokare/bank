# Bank project


### 1-  Build project

##### Require : 
 - python 3.11 or upper
 - docker


Install project dependancies
```
pip install -e .[dev] 
```

Launch Database container
```
docker compose up -d
```

Launch FastApi server (if in root project folder):
```
fastapi dev .\src\bank\api\main.py
```

### 2 - Testing and documentation


To test api features no need to uses a third party API testing like Insomnia or Postman.
FastApi already include a generated documentation with Swagger.
You can test directly back-end api features.

![alt text](/img/image-1.png)

To test an api route click on "Try it out"
![alt text](/img/image-2.png)

Then "Execute"
![alt text](/img/image-3.png)

#### Fast Api Docs : 
##### [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

### 3 -  Available features

#### Client
- Get All Clients
- Create Client
- Get Client
- Modify Client
- Delete Client

#### Account

- Get All Accounts
- Create Account
- Get Account
- Modify Account
- Delete Account
- Get Accounts From Id Client


#### Transaction

 - Get All Transactions
 - Create Transaction
 - Get Transaction 
 - Get Transaction by Account


