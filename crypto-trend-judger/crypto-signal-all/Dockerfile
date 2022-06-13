FROM rezaq/ta-lib-python-3.8.10-slim
WORKDIR /app
ADD .  /app
RUN pip install --upgrade pip              
RUN pip install -r requirements.txt
CMD ["python3","main.py"]     