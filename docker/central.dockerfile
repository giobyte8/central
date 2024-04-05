FROM python:3.10-alpine
WORKDIR /opt/central


# For ADD/COPY instructions, let's assume that context
# will be app's root folder

ADD central /opt/central/central
ADD requirements.txt /opt/central/requirements.txt


# Install dependencies and run app
RUN apk add --no-cache tzdata && pip install -r requirements.txt
ENTRYPOINT ["python", "central/main.py"]
