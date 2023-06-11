FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5001
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]