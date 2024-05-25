# Leads Data 

## Steps:

```
python3 -m venv env   
source env/bin/activate 
pip install fastapi uvicorn sqlalchemy pymysql
```

For the sender email: 
```
1. Make sure you have followed the steps outlined in https://support.google.com/accounts/answer/185833 for creating an 'App password' for your email.

2. In /LeadsProject/leads_package/constants.py replace the values for ATTORNEY_EMAIL, SERVER_LOGIN_EMAIL, SERVER_LOGIN_PASSWORD

Note: currently attorney email is a constant email, we can modify it into an array or can make use of database and API to add/ remove more attorneys in future
```

To start the service: 
```
uvicorn leads_package.main:app --reload       
```

All the APIs can be tried at: http://127.0.0.1:8000/docs


## API examples:


1. POST /users/
Usage: This can be used by prospects to submit their data to the system , Once a prospect submits this, they will receive a success email and the attorney will get an email with the new lead's email address details . By default the state of lead is set to PENDING.
```
input body: 
{
  "firstname": "string",
  "lastname": "string",
  "email": "string",
  "resume": "string"
}
```

2. GET /users/{email}

Usage: This API can be used to get a user's detail based on email address. This is to be used by attorney to get the details of users. 
```
input : email string
```

3. PUT/users/{email}/reach_out
Usage: Attorney can use this to mark the state as REACHED_OUT once they contact the lead 
```
input : email string 
```

4. GET /leads/

Usage: This can be used by attorney to get all the leads 

```
No inputs 
```

5. /users/{email}/change_state

Usage: This can be used by attorney to change state of any users manually where 0 stands for PENDING and 1 stands for REACHED_OUT

```
input : email string and state string 
```
