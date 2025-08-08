from fastapi import FastAPI
from app.core.responses import ApiResponse
from app.core.http_client import api_client
from app.models.example import ResponseModel, BaseObject

app = FastAPI()
api_response = ApiResponse()


@app.get("/")
def read_root():
    return api_response.success(data={"test": "stes"}, message="Welcome")


@app.get("/error")
def error_root():
    return api_response.error(
        message="my custom error", error_code="NOt Fund", status_code=404
    )


payload = BaseObject(
    name="Apple MacBook Pro 16",
    data={
        "year": 2019,
        "price": 1849.99,
        "CPU model": "Intel Core i9",
        "Hard disk size": "1 TB",
    },
)


@app.get("/post")
async def test_post():
    response = await api_client.post(
        endpoint="objects", response_model=ResponseModel, data=payload
    )
    if response.success:
        return api_response.success(
            data=response.data.model_dump() if response.data else None,
            message=response.message,
            status_code=response.status_code
        )
    else:
        return api_response.error(
            message=response.error,
            error_code=response.error_code,
            status_code=response.status_code,
            details=response.details
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
