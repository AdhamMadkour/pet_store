

# Pet Store API

[![pyton](https://img.shields.io/badge/python-latest-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![django](https://img.shields.io/badge/django-latest-blue.svg)](https://www.djangoproject.com/)
[![djangorestframework](https://img.shields.io/badge/djangorestframework-3.10.3-blue.svg)](https://www.django-rest-framework.org/)
[![pytest](https://img.shields.io/badge/pytest-latest-blue.svg)](https://docs.pytest.org/en/latest/)
[![docker](https://img.shields.io/badge/docker-latest-blue.svg)](https://www.docker.com/)
[![docker-compose](https://img.shields.io/badge/docker--compose-latest-blue.svg)](https://docs.docker.com/compose/)
[![swagger](https://img.shields.io/badge/swagger-2.0-blue.svg)](https://swagger.io/)

## Table of Contents

- [Introduction](#introduction)
- [prerequisites](#prerequisites)
- [Features](#features)
- [schema](#schema)
- [API Endpoints](#api-endpoints)
- [Setup](#setup)
- [Run](#run)
- [Test](#test)
- [How to use](#how-to-use)

## Introduction

Pet Store API is a simple RESTful API that allows you to manage a pet store. It is built using Django and Django Rest Framework.

## prerequisites

- docker-compose
- A platform for testing APIs like [Postman](https://www.postman.com/downloads/)

## Features

- CRUD operations for pets
- CRUD for auction on pets
- CRUD for bids
- Swagger documentation

## schema

![schema](/documentation/database_schema.png)

## API Endpoints

### Swagger

`http://localhost:8000/swagger/`
![swagger](/documentation/swagger_screenshot.png)

### Postman Collection

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://god.gw.postman.com/run-collection/18601695-2e022495-e940-467c-8679-6998f055ca06?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D18601695-2e022495-e940-467c-8679-6998f055ca06%26entityType%3Dcollection%26workspaceId%3Da7bf3bf5-053c-4fc7-af81-3acef1db61f8)

## Setup

1. Clone the repository

```bash
git clone
```

2. Remove .example from .env.example file

```bash
mv .env.example .env
```

## Run

1. Start the docker container

```bash
docker-compose -f docker-compose.dev.yml up
```

2. Sqlite database already created and migrated. You can use the default data for testing.

## Tests

1. Run command

```bash
docker exec -it <container_name> poetry run pytest -rP -vv
```

#### example:

```bash
docker exec -it pet_store-api-1 poetry run pytest -rP -vv
```

## How to use

### In order to test Auction and Bids, you need to create a pet first. And to create a pet you need to be authenticated or you can use the default data or create a user using the following from `auth/users/` endpoint.

### to get the token use the following endpoint `auth/jwt/create/`

### Example:

```json
{
  "username": "admin",
  "password": "admin"
}
```

### To create a collection you login to admin panel and create a category and tags and then create a pet using the collection id.

login to admin panel using the following credentials:

```
username: admin
password: admin
```

### To login to admin panel use the following endpoint

`localhost:8000/admin/`
![admin](/documentation/django_admin_screenshot.png)

### Or you can use the default data to test the API endpoints tags with id `1` and category with id `1`.

### To create a pet use the following endpoint `pets/` you should be authenticated to visit this endpoint.

### Example:

```json
{
    "name": "Test",
    "age": 3,
    "status": True,
    "price": "1200.00",
    "category": 1,
    "tags": [1],
}
```

### To create an auction use the following endpoint `auction/` you should be :

1. Authenticated
2. The pet should be created
3. The Pet should only have one auction at a time.
4. The auction should only be created by the pet owner.

### Example:

```json
{
  "pet": 1,
  "start_price": "1000.00",
  "start_date": "2021-09-01T00:00:00Z",
  "end_date": "2021-09-30T00:00:00Z"
}
```

### To create a bid use the following endpoint `bid/` you should be :

1. Authenticated
2. The auction should be created
3. The bid should be greater than the start price of the auction.
4. The bid should be created by a different user than the pet owner.
5. The bid should be created before the end date of the auction.

### Example:

```json
{
  "auction": 1,
  "price": "900.00"
}
```

### To view the auction bidders details use the following endpoint `pets/<pet_id>/bids/` to view this endpoint you should be:

1. Authenticated
2. The Owner of the pet.

### Enjoy the API! 🎉

```

```
