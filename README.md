# Dev<img src="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/link.svg" style="color:red" width="32">Connect developed by Avishek Das

DevConnect, the best place for finding skilled Developers. Users can register with their preferred role. Add your skills and experiences to get stand out in the talent hunt. Developers can search for jobs and directly apply on the listed jobs or can bookmark them for later. Direct messaging also available. Hiring Managers can post job and search for developers with their required skillsets. They also can direct message developers. 
***

## Technologies Used
+ [Flask (backend)](https://flask.palletsprojects.com/en/2.2.x/)
+ [HarperDB (database)](https://harperdb.io/)
+ [Bootstrap 4 (frontend)](https://getbootstrap.com/docs/4.6/getting-started/introduction/)

## Running locally

* Clone the Github repository

      git clone https://github.com/davishek7/dev-connect

* Create and activate virtual environment

      cd dev-connect
      python3 -m venv env
      source env/bin/activate

* Install dependencies using pip

      pip install requirements.txt

* Copy the .env.example file to .env and change the values

      cp .env.example .env

* Running the dev server

      python runserver.py


## Folders and File structure

+ app/ - folder holds the main application
    - app/auth/ - holds the logic related to authentication and search
    - app/user/ - all user related stuff
    - app/jobs/ - all the logics for job feature
    - app/contact/ - for contact
    - app/templates/ - frontend HTML files
    - app/static/ - holds all the static files
    - app/\_\_init__.py - it contains the flask application factory
    - app/database.py - holds the harperDB connection
    - app/context_processor.py - custom context for jinja2 templates
    - app/extensions.py - flask extensions used on the project
+ config.py - app configurations i.e. secret key etc.
+ runserver.py - file for running the application
---
## Live Url

+ [DevConnect](https://dev-connect.up.railway.app/) on Railway
+ [DevConnect](https://dev-connect-flask.herokuapp.com/) on Heroku 😒

### Accounts for testing the app

+ Developer
    - email - davishek7@gmail.com
    - password - 1234

+ Hiring Manager
    - email - canavi048@gmail.com
    - password - 1234
---

## Images for preview

### Homepage
![Homepage](/assets/images/home_screen.png)

### Developer Search
![Developer Search](/assets/images/dev_search.png)

### Search Developers by Multiple Skills
![Multi Skill Dev Search](/assets/images/multi_dev_search.png)

### Login Page
![Login](/assets/images/login.png)

### Register Page
![Register](/assets/images/register.png)

### User Profile
![User Profile](/assets/images/user_profile.png)

### User Chat with others
![User Chat](/assets/images/user_chat.png)

### Job Search
![Job Search](/assets/images/job_search.png)

### Job Search with Multiple Skills
![Job Search with Multi Skills](/assets/images/multi_job_search.png)

### Job Details
![Job Details](/assets/images/job_details.png)

### Job Create
![Job Create](/assets/images/adding_job.png)

### Job List
![Job List](/assets/images/job_list.png)

### Job Apply
![Job Apply](/assets/images/job_apply.png)

### Job Bookmark
![Job Bookmark](/assets/images/job_bookmark.png)

***

### For more on Flask Application Factory pattern

[Video](https://youtu.be/EdPutNyIHRw) | [Github](https://github.com/davishek7/flask-application-factory)
