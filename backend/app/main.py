from fastapi import FastAPI

app = FastAPI(title="Koopilot API")


@app.get("/")
def root():
    return {"message": "Koopilot backend is running"}