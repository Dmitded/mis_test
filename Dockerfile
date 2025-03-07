FROM python:3.12-slim
ENV IS_RUNNING_BY_GUNICORN yes

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]