# eclasses
1. Clone this repo:
  git clone https://github.com/nechtobolshee/eclasses


2. Add .env file with following parameters:\
#Parameters for connect db to django\
POSTGRES_HOST=<your_host>\
POSTGRES_DB=<your_db_name>\
POSTGRES_USER=<your_postgres_user>\
POSTGRES_PASSWORD=<your_postgres_password>\
POSTGRES_PORT=<your_postgres_port>


3. If you need your own db_dump use following command to make him:\
docker exec project_postgres_1 pg_dump -U <your_postgres_user> <your_db_name> > db_dump.sql


4. Run project (using docker-compose):\
  sudo docker-compose up --build