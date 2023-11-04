from fastapi import FastAPI

app = FastAPI(title="Finlearn")


@app.get("/")
def healthcheck():
    return {"status": True}
