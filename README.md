
# Fast Mock






![GitHub release (latest by date)](https://img.shields.io/github/v/release/Jahn16/fast-mock)
![Swagger Validator](https://img.shields.io/swagger/valid/3.0?specUrl=http%3A%2F%2Ffastmock.jahn.host%2Fopenapi.json)
![GitHub](https://img.shields.io/github/license/Jahn16/fast-mock?label=license)



Fast Mock is a very simple HTTP server mock, built using Fast API.

![screencapture-localhost-8000-docs-2023-11-22-08_46_57](https://github.com/Jahn16/fast-mock/assets/40438992/f16758e7-2c8d-459c-b321-7c59ff9aaaee)


## Usage/Examples

Create a mock request

```
curl --location 'fastmock.your-domain.com:8000/requests/create' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <your-token>' \
--data '{
  "method": "GET",
  "url": "https://example.com/path?param1=foo&param2=bar",
  "status_code": 200,
  "response": "{\"test\": 1}"
}'
```
Response Body
```json
{
    "method": "GET",
    "status_code": 200,
    "id": 1,
    "endpoint": "/path",
    "parameters": "param1=foo&param2=bar",
    "owner_id": 1,
    "url_id": "8f5350fb-f63e-4795-889b-9060916eca75",
    "response": {
        "test": 1
    }
}
```

Retrieve the mocked response
```
curl --location '<url-id-from-previous-step>.your-domain.com:8000/path?param1=foo&param2=bar' \
--header 'Content-Type: application/json'
```
Response Body
```json
{
    "test": 1
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
