FROM python:3.8

WORKDIR /simulator
COPY ./ .
RUN pip install -rrequirements.txt

ENV FPS=30
ENV WS_PORT=8081

CMD ["python", "simulation_server.py"]