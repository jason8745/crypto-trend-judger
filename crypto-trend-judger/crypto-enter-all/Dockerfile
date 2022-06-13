# step1
FROM python:3.9-slim as build 
COPY . /app
WORKDIR /app
# install pip package
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# step2
FROM gcr.io/distroless/python3
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/lib/python3.9/site-packages
COPY --from=build /app /app
ENV PYTHONPATH=/usr/lib/python3.9/site-packages

WORKDIR /app
CMD ["main.py"]   