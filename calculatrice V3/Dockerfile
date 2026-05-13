FROM python:3.12-slim

WORKDIR /app

RUN pip install flask pytest

COPY calculatrice.py .
COPY test_calculatrice.py .
COPY templates/ templates/

EXPOSE 3000
CMD ["python", "calculatrice.py"]
