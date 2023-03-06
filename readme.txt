Commands - for docker

alembic init alembic
docker-compose build (build docker)

docker-compose run api
docker-compose run api alembic revision --autogenerate -m "first migrate"
docker-compose run api alembic upgrade head
docker-compose up



--------- for running docker production and development image ------------
dev --> docker-compose -f docker-compose-dev.yml up -d
prod --> docker-compose -f docker-compose-prod.yml up -d