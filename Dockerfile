FROM python:3.12

RUN mkdir /xTuchan05

WORKDIR /xTuchan05

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /xTuchan05/docker/*.sh

CMD sleep 10 && (alembic revision --autogenerate -m "auto" || true) && alembic upgrade head && alembic revision --autogenerate -m "auto" || true && alembic upgrade head && gunicorn app.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000