# Friends
Supports Sending friend requests, listing friends , Accepting friend requests, and Remove friends.

## Sending a friend request

**Request**:

`POST` `/send_friend_request/`

Parameters:

Name            | Type   | Required | Description
----------------|--------|----------|------------
pk              | int    | Yes      | id of the person whom you want to send friend request.
message         | string | Yes      | Message while sending friend request.

*Note:*

- Authorization Protected

**Response**:

```json
Content-Type application/json
201 Created

{
    "message": "Request sent successfully"
}
```


## See list of friend requests

**Request**:

`GET` `/friend_requests/`


*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "friend_requests": [
        {
            "from_user": "tracc6",
            "from_user_id": 12,
            "message": "Hi! I would like to add you"
        }
    ]
}
```


## Accept a friend

**Request**:

`POST` `/accept_friend/`

Parameters:

Name            | Type   | Description
----------------|--------|---
id              | string | id of the user who sent you friend request 



*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "status": "success",
    "message": "accepted successfully"
}
```


## List all friends

**Request**:

`GET` `/friends/`

Parameters:


*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "friends": [
        {
            "id": 5,
            "username": "tracys",
            "profile_pic": "/media/maxresdefault-2_DCqaCOE.jpg",
            "latitude": 78.2089447859796,
            "longitude": 17.5448069121643,
            "distance": 6465.374721805008
        },
        {
            "id": 4,
            "username": "tracy",
            "profile_pic": "/media/test_rWi6WVN.jpg",
            "latitude": 78.2089447859796,
            "longitude": 17.5448069121643,
            "distance": 6465.374721805008
        }
    ]
}
```

## Remove a friend

**Request**:

`POST` `/remove_friend/`

Parameters:

Name            | Type   | Description
----------------|--------|---
pk              | string | id of the user who sent you friend request 



*Note:*

- **[Authorization Protected](authentication.md)**

**Response**:

```json
Content-Type application/json
200 OK

{
    "status": "success",
    "message": "Removed successfully"
}
```
