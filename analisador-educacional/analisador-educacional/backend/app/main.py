from fastapi import FastAPI

app = FastAPI(title="Analisador Educacional - Backend")


@app.get("/api/health")
def health():
    """Usado pelo Docker Compose para saber se o backend está pronto."""
    return {"status": "ok"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello, World!"}
