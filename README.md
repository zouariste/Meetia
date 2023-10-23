# Meetia

chmod 777 init.sh
python3 manage.py createsuperuser
python3 manage.py runserver

Admin Dirigeant
mzouari@outlook.com
Collaborateur
collaborateur@outlook.com
Rapporteur
rapporteur@outlook.com

docker build -t meetia-app .
docker run -it meetia-app
docker-compose up
docker exec -it meetiaappserver /bin/bash -c "source myenv/bin/activate && python3 manage.py createsuperuser"