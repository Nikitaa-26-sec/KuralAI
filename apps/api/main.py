from fastapi import FastAPI

app = FastAPI(title="KuralAI API")

@app.get("/health")
def health():
    return {"status": "ok"}
@app.get("/")
def root():
    return {"message": "KuralAI API is running"}