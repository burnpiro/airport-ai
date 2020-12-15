FROM python:3.8

WORKDIR /simulator
COPY ./ .
RUN pip install -rrequirements.txt

ENV FPS=30

CMD ["python", "simulation_server.py"]