FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_URI=mongodb://mongo:27017/file_share
ENV PORT=5000

EXPOSE $PORT

CMD ["gunicorn", "run:app", "-b", "0.0.0.0:${PORT}"]