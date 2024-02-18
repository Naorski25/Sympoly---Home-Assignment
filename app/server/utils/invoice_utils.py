from server.schema.models import InvoiceReport , Details, Person, Transaction


def to_invoice_report(data: dict) -> InvoiceReport:
    """
    Convert the parsed data to an InvoiceReport object.
    """
    details = Details.parse_details(data["Details"])
    reporter = Person.parse_person(data["Reporter"])
    approvers = [Person.parse_person(approver) for approver in data["Approvers"]]
    transactions = [Transaction.parse_transaction(transaction) for transaction in data["Transactions"]]
    return InvoiceReport(
        id=data["ID"],
        details=details,
        reporter=reporter,
        approvers=approvers,
        transactions=transactions,
    )
    
def report_to_dict(report: InvoiceReport) -> dict:
    """
    Convert the InvoiceReport object to a dictionary.
    """
    transactions = []
    for transaction in report.transactions:
        transaction_data = dict(transaction)
        transaction_data["data"] = dict(transaction.data)
        transactions.append(transaction_data)
    return {
        "id": report.id,
        "details": dict(report.details),
        "reporter": dict(report.reporter),
        "approvers": [dict(approver) for approver in report.approvers],
        "transactions": transactions,
    }


def list_reports(reports: list[InvoiceReport]) -> list[dict]:
    """
    Convert a list of InvoiceReport objects to a list of dictionaries.
    """
    return [report_to_dict(report) for report in reports]