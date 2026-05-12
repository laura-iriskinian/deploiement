FROM python:3.12-slim

WORKDIR /app

RUN pip install flask psycopg2-binary

COPY calculatrice.py .
COPY templates/ templates/

EXPOSE 3000
CMD ["python", "calculatrice.py"]
