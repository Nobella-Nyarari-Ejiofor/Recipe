# Recipe
Recipe API Project

This is a Backend Restapi application that has been developed on Django and deployed on AWS using Docker containers. 

## A Description of the WebApplication.

## Table of Content

+ [Description](#description)
+ [Behaviour Driven Development](#behaviour-driven-development)
+ [Installation Requirement](#Installation)
+ [Technology Used](#technology-used)
+ [Reference](#reference)
+ [Licence](#licence)
+ [Authors Info](#authors-info)
+ [Live Link](#live-link)

## Description

<p>An application where users can access the backend restapis on Swaager documentation . The api's use token authentication . To access the api's : The user has to . 
<p>

* </p>Click on the project <a href = "http://ec2-3-8-89-101.eu-west-2.compute.amazonaws.com/api/docs"> Link</a> </p>.
* Create a user under the api/user/me restapi .
* Generate a user token under the restapi /api/user/token/ .
* Copy the token and paste it under the authorize tab at the top of the page in the section Token . For example Token jghghjj25143563778 .
* Now the user has access to all the endpoints and documentation .



## Behaviour Driven Development

<p>

* A user can upload / delete / edit and create a recipe .
* A user can upload / delete / edit and create an ingredient for a recipe .
* A user can create their own accounts .
* A user can view recipes uploaded by others .
* A user can upload photos of recipes.

</p>

***
## Installation

* Open Terminal `ctrl+Alt+T`

* Git clone https://github.com/Nobella-Nyarari-Ejiofor/Recipe

or

* Git fork - Enter into your own repository and search-https://github.com/Nobella-Nyarari-Ejiofor/SnapPark then click on fork to add
it on your own repository.

 Navigate into the cloned project. 
`cd Recipe`


* Create and activate the vitual Environment and install the from requirements.txt
`$ python3.6 -m virtualenv virtual`
`$ source virtual/bin/activate`
`$ pip install -r requirements.txt`

* Setting up environment variables

Create an `.env` and add the following.
```
SECRET_KEY='<Secret_key>'
DBNAME='tribune'
USER='<Username>'
PASSWORD='<password>'
DEBUG=True

EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='<your-email>'
EMAIL_HOST_PASSWORD='<your-password>'

```

requirements from 
---
`requirements.txt`


* Start the Server to run the app
* `$ python3.6 manage.py runserver`

* Open [localhost:8000](#)
***


### Requirements

* Either a computer,phone,tablet or an Ipad

* An access to the Internet

* Python3

* Postgres

* virtualenv

*Pip

[Go Back to the top](#SnapPark)

## Technology Used

* Python/Django - Which was used to build the web-applications.

* Swagger - For the api documentation .

* Postgresql - For the database

* Heroku - For deployment

* Flake8 - For liniting .

* Github Workflows-  Create a CI/CD pipeline.

* Docker - For placing application in containers .

* Postgresql - For the database

* AWS - The cloud platform where the container runs.


## Reference

* LMS
