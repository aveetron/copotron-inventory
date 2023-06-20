# Welcome to Copotron Inventory!

Copotron Inventory Management System is a comprehensive and efficient software solution designed to streamline and optimize the process of managing inventory in various industries. With its user-friendly interface and powerful features, Copotron enables businesses to effectively track, monitor, and control their inventory levels, ensuring smooth operations and minimizing stock-related challenges.


## Run project
- Download the zip file and unzip
- In the project directory, create a virtual environment
    > python3 -m venv venv
- Now Activate this environment
	> source venv/bin/activate
- After activating the virtual environment, install the requirements
	> pip install -r requirements.txt
- Now run database migration commands
	> python manage.py makemigrations
	> python manage.py migrate
-  Finally run this project
	> python manage.py runserver 

## Run project using Docker
- Download the zip file and unzip
- In the project directory and run
    > docker-compose build
	> docker-compose up
- For running the project in detach mood run this command (optional)
	> docker-compose up -d




#### need any help, feel free to knock 'copotronlab@gmail.com'