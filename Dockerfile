FROM python:3.11

WORKDIR /flask-app

COPY .. /flask-app

RUN pip install -r requirements.txt

EXPOSE 4000

ENV FLASK_APP=/flask-app/api/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]