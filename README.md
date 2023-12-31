# Canto API Documentation

Welcome to the API documentation for the Blog Application! This document provides information on how to interact with canto APIs.

# Table of Contents

1. [About](#about)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Authentication](#authentication)
5. [API Endpoints](#api-endpoints)
   - [Admin Enpoints](#admin-endpoints)
   - [Business Type Endpoints](#business-type-endpoints)
   - [Business Enpoints](#business-endpoints)
   - [Business Image Endpoints](#business-image-endpoints)
   - [Business Item Endpoints](#business-item-endpoints)

## About

Canto API allows businesses in a specific location, area or gated community to be added to a directory of businesses that can be seached based on keywords.

## Features

- Authentication
- Multipe image upload
- Search with keywords
- View details of the Business

## Technologies

- Python
- Docker
- Sqlalchemy
- PostgreSQL
- Pytest
- [Swagger API Spec](https://canto-api.onrender.com/docs#/)
- Uvicorn server

## Authentication

Before using the API endpoints, you must authenticate yourself. We use JSON Web Tokens (JWT) for authentication. To authenticate, include an `Authorization` header with a valid token in your request.

Example:

```

Authorization: Bearer YOUR_ACCESS_TOKEN

```

## API Endpoints

## Admin Endpoints

This enpoints are for those that can add a business to the application.

| Endpoint                   | Method   | Description                                    |
| -------------------------- | -------- | ---------------------------------------------- |
| `/admins`                  | `GET`    | Retrieve a list of all admins.                 |
| `/admins/{admin_id}`       | `GET`    | Retrieve a specific detail of admin by its ID. |
| `/admin`                   | `POST`   | Create an admin account.                       |
| `/admins/{admin_id}`       | `PUT`    | Update an existing admin by its ID.            |
| `/admins/{admin_id}`       | `DELETE` | Delete an admin account by its ID.             |
| `/admins/login`            | `POST`   | Admin can login to account.                    |
| `/admins/{admin_id}/image` | `POST`   | Add display image for admin.                   |

## Business Type Endpoints

These endpoints are just to categorize the business into various types and categories are based on the Admins intuition.

| Endpoint                   | Method   | Description                                         |
| -------------------------- | -------- | --------------------------------------------------- |
| `/business/type`           | `GET`    | Retrieve a list of all businesses.                  |
| `/business/type/{type_id}` | `GET`    | Retrieve a specific detail of a business by its ID. |
| `/business/type`           | `POST`   | Add a business.                                     |
| `/business/type/{type_id}` | `PUT`    | Update an existing business by its ID.              |
| `/business/type/{type_id}` | `DELETE` | Delete an admin account by its ID.                  |

## Business Endpoints

These are endpoints for businesses to be added.

| Endpoint                                          | Method   | Description                                         |
| ------------------------------------------------- | -------- | --------------------------------------------------- |
| `/business`                                       | `GET`    | Retrieve a list of all businesses.                  |
| `/business/{business_id}`                         | `GET`    | Retrieve a specific detail of a business by its ID. |
| `/business`                                       | `POST`   | Add a business.                                     |
| `/business/search?limit=10&offset=0&keyword=rice` | `POST`   | Search for/about a business by keyword.             |
| `/business/{business_id}`                         | `PUT`    | Update an existing business by its ID.              |
| `/business/{business_id}`                         | `DELETE` | Delete an admin account by its ID.                  |

## Business Image Endpoints

These are endpoints to add images to the business for people to view more details on them.

| Endpoint                     | Method   | Description                             |
| ---------------------------- | -------- | --------------------------------------- |
| `/business/image/display`    | `POST`   | Add business display image.             |
| `/business/image/display`    | `DELETE` | Delete business display image.          |
| `/business/image/{image_id}` | `DELETE` | Delete an image from a business.        |
| `/business/image/`           | `POST`   | Add multiple/one image(s) to business.  |
| `/business/image/`           | `DELETE` | Delete multiple images from a business. |

## Business Item Endpoints

| Endpoint                        | Method   | Description                                              |
| ------------------------------- | -------- | -------------------------------------------------------- |
| `/business/item/`               | `GET`    | Retrieve a list of all businesses items.                 |
| `/business/item/`               | `POST`   | Create a business item.                                  |
| `/business/items/`              | `POST`   | Add multiple business items to business.                 |
| `/business/{business_id}/item/` | `GET`    | Retrieve a list of all items that belongs to a business. |
| `/business/item/{id}`           | `GET`    | Retrieve a single item.                                  |
| `/business/item/{id}`           | `PUT`    | Update a business item.                                  |
| `/business/item/{id}`           | `DELETE` | Delete a business item.                                  |

### Connect with me 🗣️

<a href="https://twitter.com/oyekolatoheeb"><img src="https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white"/></a>
<a href="https://www.linkedin.com/in/toheeb-oyekola-937b59201/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="https://toheeb19.hashnode.dev/"><img src="https://img.shields.io/badge/Hashnode-2962FF?style=for-the-badge&logo=hashnode&logoColor=white"/></a>
