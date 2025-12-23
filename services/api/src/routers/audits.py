from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.repositories import get_payout_run

router = APIRouter()


class AuditResponse(BaseModel):
    run_id: str
    month: str
    audit: dict | None


@router.get("/audits/{run_id}", response_model=AuditResponse)
def get_audit(run_id: str) -> AuditResponse:
    run = get_payout_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Payout run not found")
    return AuditResponse(run_id=run.run_id, month=run.month, audit=run.audit_json)
