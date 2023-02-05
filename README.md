
# Fast Mock






![GitHub release (latest by date)](https://img.shields.io/github/v/release/Jahn16/fast-mock)
![Swagger Validator](https://img.shields.io/swagger/valid/3.0?specUrl=http%3A%2F%2Ffastmock.jahn.host%2Fopenapi.json)
![GitHub](https://img.shields.io/github/license/Jahn16/fast-mock?label=license)



Fast Mock is a very simple HTTP server mock, built using Fast API.
## Documentation

[Fast Mock - Swagger UI](http://fastmock.jahn.host/docs)


## Usage/Examples

Curl
```
curl -X 'GET' \
  'http://fastmock.jahn.host/endpoint%2Fyou%2Fwant%2Fmocked' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzU2MDY0MjQsInN1YiI6IjEifQ.qhx1Ul3gfyby2pdLKUZj0S-9g8_Rsuq50ILksvs_FMc'
```
Response Body
```json
{
  "response": {
    "youWantMocked": "valueYouWant"
  }
}
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/Jahn16/fast-mock.git
```

Go to the project directory

```bash
  cd fast-mock
```

Install dependencies

```bash
  pip install -r requirements
```

Start the server

```bash
  uvicorn app.main:app
```
