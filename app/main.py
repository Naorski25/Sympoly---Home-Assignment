from fastapi import FastAPI
from server.databsae import init_db
from server.routes.invoice import router as Router


app = FastAPI()
app.include_router(Router, tags=["InvoiceReport"], prefix="/reports")

@app.on_event("startup")
async def start_db():
    await init_db()



