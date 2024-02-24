# First you have to create a .env file inside the project folder then place the following variables

SECRET_KEY=flask-app-secret
SQLALCHEMY_DATABASE_URI=sqlite:///sqlite.db

CLOUDINARY_URL=your cloudinary url
CLOUDINARY_CLOUD_NAME=your cloudinary cloud name
CLOUDINARY_API_KEY=your cloudinary api key
CLOUDINARY_API_SECRET=your cloudinary api secret

## I have also included a sample file .env.sample

# Then you have to install the "requirements.txt" file by creating a virtual environment

# You have to run two server one is for the TailwindCSS and the other is for flask

# In order to run the server for enabling TailwindCSS for the flask application you have to run the following command from the root of the project

### npm run watch

# In order to run the flask application you should navigate to the src folder then run either one of the following commands

### flask run

## or

### python app.py (for Windows OS)

### python3 app.py (for Mac OS)
