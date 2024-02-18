from fastapi import APIRouter, status, File, UploadFile, HTTPException
from server.schema.models import InvoiceReport
from server.schema.exrf_parser import EXRFParser
from server.utils.invoice_utils import to_invoice_report, list_reports

router = APIRouter()

@router.get("/", response_description="reports records retrieved")
async def get_reports() -> list[InvoiceReport]:
    reports = await InvoiceReport.find_all().to_list()
    reports = list_reports(reports)
    return reports

@router.get("/{id}", response_description="singel report record retrieved")
async def get_report_record(id: str) -> InvoiceReport:
    review = await InvoiceReport.get(id)
    return review

@router.post("/upload/", status_code=status.HTTP_201_CREATED, response_model=InvoiceReport)
async def add_report(file: UploadFile = File(...)):
    contents = await file.read()
    file_data = contents.decode("utf-8")
    await save_to_mongodb(file_data)

    return {"filename": file.filename}
    
async def save_to_mongodb(file_data):
    lines = file_data.split("\n")
    parsed_data_raw = EXRFParser.parse_file(lines)
    parsed_data_object = to_invoice_report(parsed_data_raw["Report"])

    await parsed_data_object.insert()

@router.delete("/{id}", response_description="report record deleted from the database")
async def delete_report(id: str) -> dict:
    record = await InvoiceReport.get(id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Review record not found!"
        )

    await record.delete()
    return {
        "message": "Record deleted successfully"
    }