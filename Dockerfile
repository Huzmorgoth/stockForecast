FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install --use-feature=2020-resolver -r requirements.txt
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]