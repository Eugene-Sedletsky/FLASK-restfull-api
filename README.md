# Scaffolding for RestFULL api service in FLASK

This is JSON based RESTfull API service, designed to be in trusted network, where you don't need to validate access levels of requestor (think microservice and Ambassador/Proxy)

With microservice in mind, this project implement basic CRUD functionality to manage user related data.

    - All received data are validated against JSONSchema
    - User can be added to database as long as consent been provided.
    - In case of revoking consent, user will be deleted from database.


![test-coverage.png](doc%2Ftest-coverage.png)
Figure: Test coverage report

![test-coverage.png](doc%2Fpylint-code-quality.png)
Figure: PyLint code quality report


## Motivation

After discovering another Flask-based API that lacked structure and testability. Determined to improve the development experience, I created this project as a scaffold for my private endeavors.
My goal is to inspire others to explore better practices for building Flask apps. Let's journey together towards excellence in API development.


### Unit Tests and Functional Tests

I believe in the importance of testing to ensure the reliability and robustness of our code. That's why I have incorporated both unit tests and functional tests in this project.
Unit tests help us validate the individual components of our code, while functional tests ensure the smooth functioning of the application as a whole.
With thorough testing, we can confidently deliver a more stable and bug-free experience to our users.


### Automatic API Request Handler Binding

To make experience as a developer smoother and more efficient, I've implemented automatic API request handler binding. This means you won't have to manually map each API endpoint to its corresponding handler.
Instead, our system will take care of this binding for you, saving you time and effort, just create a new controller and app will bind it automatically for you.

### Flask App Configuration Management

Deploying and testing applications often require different configurations, especially when it comes to databases. This application easily switch databases for test instances during testing.
This flexibility allows for a more seamless testing process and helps ensure that your tests run smoothly without interfering with your production database.


## Instructions 
    

### 1. Create a new virtual environment:

```sh
python3 -m venv venv
```

### 2. Activate the virtual environment:

```sh
$ source venv/bin/activate
```


### 2. Install dependencies

Install the python packages specified in requirements.txt:

```sh
(venv) $ pip install -r requirements.txt
```

### 3 Database Initialization

This Flask application needs a SQLite database to store data. The database could be be initialized using:

```
(venv) $ flask init_db
```


### 4 Running the Flask Application

Run development server to serve the Flask application:

```sh
(venv) $ flask --app app --debug run
```

Navigate to 'http://127.0.0.1:5000' in your favorite web browser to view the website!


## Testing

### To run all the tests:

```sh
(venv) $ python -m pytest -v
```

### To check test coverage

To check the code coverage of the tests:

```sh
(venv) $ python -m pytest --cov-report term-missing --cov=project
```


## Key Python Modules Used

* **Flask**: micro-framework for web application development which includes the following dependencies:
  * click: package for creating command-line interfaces (CLI)
  * itsdangerous: cryptographically sign data 
  * Jinja2: templating engine
  * MarkupSafe: escapes characters so text is safe to use in HTML and XML
  * Werkzeug: set of utilities for creating a Python application that can talk to a WSGI server
* **pytest**: framework for testing Python projects
* **Flask-SQLAlchemy** - ORM (Object Relational Mapper) for Flask
* **Flask-WTF** - simplifies forms in Flask
* **flake8** - static analysis tool
* **isort** - sorts Python package imports
* **safety** - checks Python dependencies for known security vulnerabilities
* **bandit** - tool designed to find common security issues in Python code
* **jsonschema** - library for validating data against JSON schema

@ToDo: consider using .env and libraries such

* **python-dotenv** - .env. for test environment
* **dotenv** - loading .env for production environment
* **Flask** - 




This application is written using Python 3.11.