# Maintenance-Tracker [![Build Status](https://travis-ci.org/davenmathews/Maintenance-Tracker.svg?branch=api)](https://travis-ci.org/davenmathews/Maintenance-Tracker) [![Coverage Status](https://coveralls.io/repos/github/davenmathews/Maintenance-Tracker/badge.svg?branch=api)](https://coveralls.io/github/davenmathews/Maintenance-Tracker?branch=api) [![Maintainability](https://api.codeclimate.com/v1/badges/b457b83d3a9f810225e0/maintainability)](https://codeclimate.com/github/davenmathews/Maintenance-Tracker/maintainability)

This is an application that provides users with the ability to reach out to operations or repairs department regarding repair or maintenance requests and monitor the status of their request.

## User Interface Features
- Users can [register](https://davenmathews.github.io/Maintenance-Tracker/UI/html/user-register.html) for a free account.
- Users can [log into their accounts](https://davenmathews.github.io/Maintenance-Tracker/UI/html/index.html).
- Users can [make requests](https://davenmathews.github.io/Maintenance-Tracker/UI/html/make-request.html) to the app.
- Users can [see all their requests.](https://davenmathews.github.io/Maintenance-Tracker/UI/html/index-user.html)
- Users can [view all details on a particular request](https://davenmathews.github.io/Maintenance-Tracker/UI/html/user-view-request.html) and perform actions such as editing and deleting.
- Users can [view and edit their profile.](https://davenmathews.github.io/Maintenance-Tracker/UI/html/my-profile.html)
- Admin can [log in.](https://davenmathews.github.io/Maintenance-Tracker/UI/html/index.html)
- Admin can [view all requests made to this app and respond accordingly.](https://davenmathews.github.io/Maintenance-Tracker/UI/html/index-admin.html)

### Technology Used
- HTML
- CSS

### Deployment
Github pages: https://davenmathews.github.io/Maintenance-Tracker/UI/html/index.html

## API
### Built with:
- Python 3.6
- Flask

### Prerequisites:
- Should have [git](https://git-scm.com/) installed
- Should have [Python](https://www.python.org/) 3.6 installed
- Should have [pip](https://pypi.org/) installed
- Should have [PostgreSQL](https://www.postgresql.org) installed.
- Should have decent knowledge on working with the above.
### Features:
- `POST api/v1/auth/signup` User registration
- `POST api/v1/auth/login` User login
- `POST api/v1/auth/logout` User logout
- `GET api/v1/requests` Admin views all requests made in the application
- `GET api/v1/requests/<int:request_id>` Admin views one request as per the id in the URL
- `PUT api/v1/requests/<int:request_id>/<string:action>` Admin responds to requests
- `GET api/v1/users/` Admin views all users in the app
- `GET api/v1/users/<int:user_id>` Admin views one user as per the id in the URL
- `PUT api/v1/users/<int:user_id>/<string:action>` Admin promotes/demotes user
- `GET api/v1/users/request/` Users view their requests
- `POST api/v1/users/requests/<int:request_id>` User views one request as per the id in the URL
- `PATCH api/v1/users/requests/<int:request_id>` User edits request as per the id in the URL

### How to install the project:
- Clone this repository:
  `https://github.com/davenmathews/Maintenance-Tracker.git`
- `cd` into the directory where this repository was cloned.
- create a virtual environment using the code below:

    `pip install virtualenv`

    `virtualenv venv`
- install the requirements needed

    `pip install -r requirements.txt`
- run the code below to set the environment variables.

   **Windows**

    `setx APP_CONFIG_NAME development`\
    `setx DB_NAME testdb`\
    `setx DB_USER <your postgresql user>`\
    `setx DB_PASSWORD <your postgresql user's password>`\
     **_Ensure your user has read and write privileges_**

    `setx ADMIN_EMAIL <your preferred email>`\
    `setx ADMIN_PASSWORD <your preferred password>`\- should follow guidelines given in the
    signup route in the documentation

    `setx ADMIN_QUESTION <your preferred security question>`\
    `setx ADMIN_ANSWER<your preferred security answer>`\
     **_You can use the above credentials in the login route, to log in as an administrator_**

   **Mac/Linux**

    `export APP_CONFIG_NAME=development`\
    `export DB_NAME=testdb`\
    `export DB_USER=<your postgresql user>`\
    `export DB_PASSWORD=<your postgresql user's password>`\
     **_Ensure your user has read and write privileges_**

    `export ADMIN_EMAIL <your preferred email>`\
    `export ADMIN_PASSWORD <your preferred password>`\- should follow guidelines given in the
    signup route in the documentation

    `export ADMIN_QUESTION <your preferred security question>`\
    `export ADMIN_ANSWER<your preferred security answer>`\
     **_You can use the above credentials in the login route, to log in as an administrator_**

- run the code below to start the server:
  `python maintenanceTracker.py`

- Test the above endpoints using Postman. To promote another user to admin, use the endpoint above and append 'promote' to the URL. To demote use 'demote'.
- The endpoints documentation can be found on the path
  `api/v1` inside the browser. You can also test the endpoints [here](https://fathomless-bayou-53469.herokuapp.com/api/v1)
- To run tests:
    `nosetests -v ./MaintenanceTrackerAPI/_tests`

### Deployment
[Heroku](https://fathomless-bayou-53469.herokuapp.com/api/v1)
