# eclasses
1. Clone this repo:
  git clone https://github.com/nechtobolshee/eclasses


2. Add .env file with following parameters:
#Parameters for connect db to django
HOST=<your_host>
POSTGRES_DB=<your_db_name>
POSTGRES_USER=<your_postgres_user>
POSTGRES_PASSWORD=<your_postgres_password>

#Parameters for django superuser
DJANGO_SUPERUSER_USERNAME=<your_username>
DJANGO_SUPERUSER_EMAIL=<your_email>
DJANGO_SUPERUSER_PASSWORD=<your_password>

3. Run project (using docker-compose):
  sudo docker-compose up --build
