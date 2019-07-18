# Users
Supports registering, viewing, and updating user accounts.

## Register a new user account

**Request**:

`POST` `/users/`

Parameters:

Name            | Type   | Required | Description
----------------|--------|----------|------------
username        | string | Yes      | The username for the new user.
password        | string | Yes      | The password for the new user account.
first_name      | string | No       | The user's given name.
last_name       | string | No       | The user's family name.
email           | string | No       | The user's email address.
location        | string | No       | The user's locations in SRID=4326;POINT (78.2089447859796 17.5448069121643) format.
nkey            | string | No       | The user's notification token
profile_picture | image  | No       | The user's profile picture


*Note:*

- Not Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
    "id": 13,
    "username": "tracc7",
    "first_name": "tracc7",
    "last_name": "gibson",
    "email": "tracc7@ghm.io",
    "auth_token": "db455cddf16d70f951de4fd9e12dde8568585d3b",
    "location": "SRID=4326;POINT (78.2089447859796 17.5448069121643)",
    "profile_picture": "http://127.0.0.1:8000/media/maxresdefault-2.jpg"
}
```

The `auth_token` returned with this response should be stored by the client for
authenticating future requests to the API. See [Authentication](authentication.md).


## Get a user's profile information

**Request**:

`GET` `/users/:id`

Parameters:

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "id": 11,
    "username": "tracc5",
    "first_name": "tracc5",
    "last_name": "gibson",
    "location": "SRID=4326;POINT (78.2089447859796 17.5448069121643)",
    "profile_picture": "http://127.0.0.1:8000/media/maxresdefault_lyBe4I3.jpg"
}
```


## Update your profile information

**Request**:

`PUT/PATCH` `/users/:id`

Parameters:

Name            | Type   | Description
----------------|--------|---
first_name      | string | The first_name of the user object.
last_name       | string | The last_name of the user object.
email           | string | The user's email address.
location        | string | The user's locations in SRID=4326;POINT (78.2089447859796 17.5448069121643) format.
nkey            | string | The user's notification token
profile_picture | image  | The user's profile picture




*Note:*

- All parameters are optional
- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "id": 13,
    "username": "tracc7",
    "first_name": "tracc7",
    "last_name": "gibson",
    "location": "SRID=4326;POINT (78.2089447859796 17.5448069121643)",
    "profile_picture": "http://127.0.0.1:8000/media/maxresdefault-2.jpg"
}
```


## Search for user profiles

**Request**:

`GET` `/user_search/`

Parameters:

Name       | Type   | Description
-----------|--------|---
search     | string | Can contain username or email address starts with

*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "vjpranay",
            "first_name": "",
            "last_name": "",
            "location": null
        }
    ]
}
```
