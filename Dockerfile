FROM python:3.8-alpine
WORKDIR /app
COPY . /app
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app/app.py"]