FROM python:3.10-slim as build

WORKDIR /usr/app
RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.10-slim@sha256:134b8763131e8a6800c1393108ec60efc3ed6d793243787bddd1b972ed10b722

RUN groupadd -g 999 user && useradd -r -u 999 -g user user

RUN mkdir /usr/app && chown user:user /usr/app
WORKDIR /usr/app

COPY --chown=user:user --from=build /usr/app/venv ./venv
COPY --chown=user:user . .
USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 5000


ENTRYPOINT ["./boot.sh"]
