# EcommerceApplication
Django Ecommerce application project setup with Ubuntu(Linux distribution):

1) -Clone the project from Github:

    git clone -b develop https://github.com/DamodarVishwakarma/EcommerceApp.git

2) -Create virtual environment and activate it, to do this follow these commands:

    a)  sudo pip3 install virtualenv
    b)  sudo apt install python3.8-venv
    c)  python3 -m venv env_name
    d)  source env_name/bin/activate

3) -Change the directory:

    cd ecomUser

4) -Install dependencies:

    pip install -r requirements.txt

5) -Apply database migrations:
    
    a)  python manage.py makemigrations 
    b)  python manage.py migrate

6) -Start local development server:

    python manage.py runserver

