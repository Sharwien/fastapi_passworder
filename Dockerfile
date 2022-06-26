FROM python:3.10
WORKDIR /app
# Caching the requirements layer here!
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ./requirements.txt /tmp
RUN pip install --upgrade -r /tmp/requirements.txt
COPY ./passworder /app
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]
