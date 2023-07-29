This Project needs to following modules to be installed
* Flask
* flask_sqlalchemy
* flask_restful

Create a requirements.txt with all the modules in it.
* flask
* flask-SQLAlchemy==2.5.1
* flask-restful

To create virtual environment
Run the following commands in terminal
* `python -m venv env` 
* `cd env\scripts`
* `.\activate` --------- To activate the env
* `pip install -r requirements.txt`

To deactivate the env, use `deactivate` 

(OR)

Install the modules by following these commands
`pip install Flask`
`pip install flask-sqlalchemy`
`pip install flask-restful` 

After installing the modules follow the procedure given below.

- Go to root directory of the application and find "app.py"

- Now to create the database
`>>> from models import db`
`>>>  db.create_all()` 

- Run the app.py file using the terminal according to the respective operating system.


```
├── iitmproject
    ├── static
    ├── templates
    ├── app.py
    ├── models.py
    ├── api.py
    ├── database.sqlite3
    ├── readme.txt
    |── Report.pdf 
    |── requirements.txt 


```# Flask-BlogLite
# Flask-BlogLite
