FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PREFECT_API_URL=http://prefect-server:4200/api

CMD ["python", "run_pipeline.py"]
