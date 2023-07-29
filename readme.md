# Flask-Bloglite-v1

## Description:
Blog-Lite is a multi-user app where users can post blog-entries with appropriate images to spread their ideas in the form of text. The app has features to follow and search other users, and also voice their opinions through comments and likes on their posts.

## Technologies Used:
* Python: Develop the controllers and serve as the host programming language for the app
* Flask: Serves as the web-framework for the app
* Flask-Restful: Used to develop the RESTful API for the app to process CRUD
* Flask-SQLAlchemy: Used to access and modify the app's SQLite database
* HTML: Develop the required web-pages.
* Jinja2: Template engine
* CSS: Style the web-pages
* Bootstrap: To make the frontend appealing and easy to navigate. (Used CDN link)
* SQLite: Serves as the database for the app
  


## Architecture and Features:
The application follows the standard MVC architecture. The View of the application is created using HTML, CSS, and Bootstrap. The Controller is created using Python and Flask. The Model is created using Flask-SQLAlchemy.

The features of the application are as follows:

* Signup and Login for users
* Ability to view user’s posts, followers, and follows
* Navigate and view other’s posts, followers, and follows
* Ability to search, follow, and unfollow other users
* User specific feed according to the follows of the user
* Create, View, Edit, and Delete posts
* Create, View, Edit, and Delete user accounts
* Comment to express user’s opinions on posts
* Like other posts

  
## Required Modules
* Flask
* flask_sqlalchemy
* flask_restful

## To Create Virtual Environment
Run the following commands in terminal
* `python -m venv env` 
* `cd env\scripts`
* `.\activate` --------- To activate the env
* `pip install -r requirements.txt` to install the modules

To deactivate the env, use `deactivate` 

## Instructions to Run the App

* create the database by opening the terminal
*  type `python` and click enter, write the below code
* ` from models import db` `db.create_all()`
Your database is created.
* cd into the directory of the project
Run python app.py

## Folder Structure

* `database.sqlite3` is the sqlite database. It can be anywhere on the machine just the adjustment in path in app.py is required.
* `static` a folder in which we have the photos, profile and css files used in the app.
** `photos` is the folder where blog upload imgs are stored.
** `profile` is the folder where profile pics are stored.
* `templates` is the default folder where templates are stored.
* `requirements.txt` is the txt file containing the modules required.

```
blog-lite1-mad1/

├── app.py
├── api.py
├── modals.py
├── database.sqlite3
├── static
    ├──index.css
    ├──mains.css
    ├──blog.jpg
    └──profile
       └── profile-pic
    └──photos
       └── blog-images
├── readme.md
└── templates
    └── html-files
├── Report.pdf
└── requirements.txt
```

   
