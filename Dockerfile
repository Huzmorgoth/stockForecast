FROM python:3.6
WORKDIR /app
COPY . .
RUN apt-get --yes --no-install-recommends install python3 python3-dev
RUN pip install --use-feature=2020-resolver -r requirements.txt
ENTRYPOINT [ "streamlit" ]
CMD [ "run", "Main.py" ]