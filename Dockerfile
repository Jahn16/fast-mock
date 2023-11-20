FROM python:3.10-slim as build

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim@sha256:134b8763131e8a6800c1393108ec60efc3ed6d793243787bddd1b972ed10b722

RUN groupadd -g 999 fastmock && useradd -r -u 999 -g fastmock fastmock

RUN mkdir /usr/app && chown fastmock:fastmock /usr/app
WORKDIR /usr/app

COPY --chown=fastmock:fastmock --from=build /usr/app/venv ./venv
COPY --chown=fastmock:fastmock . .
USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 8000


ENTRYPOINT ["./boot.sh"]
