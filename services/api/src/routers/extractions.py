from dataclasses import asdict
from pathlib import Path

from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel

from db.repositories import (
    create_extraction,
    ExtractionRecord,
    get_upload,
    list_extractions,
    new_extraction_record,
    update_extraction,
)
from services.vision import run_dual_model_extraction

router = APIRouter()


class ExtractionRequest(BaseModel):
    upload_id: str


class ExtractionResponse(BaseModel):
    extraction_id: str
    upload_id: str
    status: str
    model_primary: str
    model_secondary: str | None
    raw_verbatim: str | None
    payload_json: dict | None
    normalized_json: dict | None
    diff_json: list[dict] | None
    validation_errors: list[str] | None


class ExtractionListResponse(BaseModel):
    extractions: list[ExtractionResponse]


@router.post("/extractions", response_model=ExtractionResponse)
def run_extraction(payload: ExtractionRequest) -> ExtractionResponse:
    upload = get_upload(payload.upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    image_bytes = _load_image_bytes(upload.storage_path)
    if image_bytes is None:
        raise HTTPException(status_code=404, detail="Stored file not found")

    record = new_extraction_record(
        upload_id=upload.upload_id,
        status="PENDING",
        model_primary="primary",
        model_secondary="secondary",
    )
    saved = create_extraction(record)

    images = [image_bytes]
    result = run_dual_model_extraction(images)
    updated = update_extraction(
        ExtractionRecord(
            extraction_id=saved.extraction_id,
            upload_id=saved.upload_id,
            status=result.status,
            model_primary="maverick",
            model_secondary="scout",
            raw_verbatim=result.verbatim,
            payload_json=result.payload,
            normalized_json=result.normalized,
            diff_json=[asdict(diff) for diff in result.diffs],
            validation_errors=result.errors,
        )
    )

    return ExtractionResponse(
        extraction_id=updated.extraction_id,
        upload_id=updated.upload_id,
        status=updated.status,
        model_primary=updated.model_primary,
        model_secondary=updated.model_secondary,
        raw_verbatim=updated.raw_verbatim,
        payload_json=updated.payload_json,
        normalized_json=updated.normalized_json,
        diff_json=updated.diff_json,
        validation_errors=updated.validation_errors,
    )


@router.get("/extractions", response_model=ExtractionListResponse)
def list_extractions_endpoint() -> ExtractionListResponse:
    items = []
    for extraction in list_extractions():
        items.append(
            ExtractionResponse(
                extraction_id=extraction.extraction_id,
                upload_id=extraction.upload_id,
                status=extraction.status,
                model_primary=extraction.model_primary,
                model_secondary=extraction.model_secondary,
                raw_verbatim=extraction.raw_verbatim,
                payload_json=extraction.payload_json,
                normalized_json=extraction.normalized_json,
                diff_json=extraction.diff_json,
                validation_errors=extraction.validation_errors,
            )
        )
    return ExtractionListResponse(extractions=items)


def _load_image_bytes(storage_path: str) -> bytes | None:
    path = Path(storage_path)
    if path.exists():
        return path.read_bytes()
    if storage_path.startswith("http://") or storage_path.startswith("https://"):
        with httpx.Client(timeout=30) as client:
            response = client.get(storage_path)
            if response.status_code != 200:
                return None
            return response.content
    return None
