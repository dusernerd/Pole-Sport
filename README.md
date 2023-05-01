# Pole Sport

### Introduction

Universities tend to provide different outdoor activities for their students, and sport is one of them. It is nice to have a platform that would allow students to make an online inscription for their favourite sports. This web application is made to facilitate that process.

#### Description
#### General Structure of a program

The program is built using **FLASK** Python Library for Back-End, and **HTML**, **CSS** for Front-End. It consists of **app.py** main python file, where the whole logic is written for Back-End, **helpers.py** supplementary file, HTML and CSS files (HTML files are in *templates* folder, whereas CSS file is in *static* folder), *session* folder, where FLASK stores users' sessions, and *users.db* database.

#### Imported modules

In **app.py** are imported the following modules:
*os* - to ask a user for a API_KEY.
*flask* - for handling requests, rendering templates, and storing session's information.
*cs50* - for data manipulation.
*flask_session* - to deal with FLASK's sessions.
*helpers* - for rendering apology.html and using login_required decorator.

#### Detailed information

In **app.py** there are also different functions implemented., *def after_request()* to ensure responses aren't cached. *def login()* with GET and POST methods, which is render the login page and verifying the credentials entered and clearing session function. *def index()* to get the homepage of the user Subscribe and Unsubscribe for a discipline, also *@login_required* decorator is implemented, so that if the user is not logged in he/she can't access that page. *def signup()* for creating an account and entering that information to the database. *def logout()* to log out by clearing the session.
Generally, there are two types of request's methods: GET and POST. GET is made to show up the pages and provide information about existing data, however via GET it is also possible to get and pass argument to a database. POST is made to transfer the information more securely.
In the application there are four different urls that can be reached: */*, */login*, */signup* and */logout*.
*/* - for the main page
*/login* - before the main page to Log In
*/signup* - if not registered yet to Sign Up
*/logout* - once entered the user can be Logged Out
A user can create an account, then log in into his/her homepage and register for an interested sport discipline, and afer that the user can delete that registration from a list.
In *users.db* database there are three tables: users, sports and enrollment (joined table). Users' table is made to save the user information by name and hashed value of the password provided, Sports' table is served for storing all sports available at that moment, and enrollment table is made to join that two tables together (many to many relationship).
