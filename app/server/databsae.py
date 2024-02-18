from beanie import init_beanie
import motor.motor_asyncio
from server.schema.models import InvoiceReport

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        "mongodb+srv://sympoly:sympoly@sympoly-client.sbznudx.mongodb.net/"
    )
    await init_beanie(database=client.db_invoice_reports, document_models=[InvoiceReport])
