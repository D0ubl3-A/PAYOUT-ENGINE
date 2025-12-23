from dataclasses import dataclass
from uuid import uuid4

from psycopg.rows import dict_row

from db.connection import get_conn


@dataclass(frozen=True)
class ExtractionRecord:
    extraction_id: str
    upload_id: str
    status: str
    model_primary: str
    model_secondary: str | None
    raw_verbatim: str | None
    payload_json: dict | None
    normalized_json: dict | None
    diff_json: dict | None
    validation_errors: dict | None


def new_extraction_record(
    upload_id: str,
    status: str,
    model_primary: str,
    model_secondary: str | None = None,
    raw_verbatim: str | None = None,
    payload_json: dict | None = None,
    normalized_json: dict | None = None,
    diff_json: dict | None = None,
    validation_errors: dict | None = None,
) -> ExtractionRecord:
    return ExtractionRecord(
        extraction_id=uuid4().hex,
        upload_id=upload_id,
        status=status,
        model_primary=model_primary,
        model_secondary=model_secondary,
        raw_verbatim=raw_verbatim,
        payload_json=payload_json,
        normalized_json=normalized_json,
        diff_json=diff_json,
        validation_errors=validation_errors,
    )


def create_extraction(record: ExtractionRecord) -> ExtractionRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO extractions (
                  extraction_id,
                  upload_id,
                  status,
                  model_primary,
                  model_secondary,
                  raw_verbatim,
                  payload_json,
                  normalized_json,
                  diff_json,
                  validation_errors
                )
                VALUES (
                  %(extraction_id)s,
                  %(upload_id)s,
                  %(status)s,
                  %(model_primary)s,
                  %(model_secondary)s,
                  %(raw_verbatim)s,
                  %(payload_json)s,
                  %(normalized_json)s,
                  %(diff_json)s,
                  %(validation_errors)s
                )
                RETURNING extraction_id, upload_id, status, model_primary, model_secondary,
                          raw_verbatim, payload_json, normalized_json, diff_json, validation_errors
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return ExtractionRecord(**row)


def update_extraction(record: ExtractionRecord) -> ExtractionRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE extractions
                SET status = %(status)s,
                    model_primary = %(model_primary)s,
                    model_secondary = %(model_secondary)s,
                    raw_verbatim = %(raw_verbatim)s,
                    payload_json = %(payload_json)s,
                    normalized_json = %(normalized_json)s,
                    diff_json = %(diff_json)s,
                    validation_errors = %(validation_errors)s,
                    updated_at = now()
                WHERE extraction_id = %(extraction_id)s
                RETURNING extraction_id, upload_id, status, model_primary, model_secondary,
                          raw_verbatim, payload_json, normalized_json, diff_json, validation_errors
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return ExtractionRecord(**row)


def get_extraction(extraction_id: str) -> ExtractionRecord | None:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT extraction_id, upload_id, status, model_primary, model_secondary,
                       raw_verbatim, payload_json, normalized_json, diff_json, validation_errors
                FROM extractions
                WHERE extraction_id = %(extraction_id)s
                """,
                {"extraction_id": extraction_id},
            )
            row = cur.fetchone()
            return ExtractionRecord(**row) if row else None


def list_extractions(limit: int = 50) -> list[ExtractionRecord]:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT extraction_id, upload_id, status, model_primary, model_secondary,
                       raw_verbatim, payload_json, normalized_json, diff_json, validation_errors
                FROM extractions
                ORDER BY created_at DESC
                LIMIT %(limit)s
                """,
                {"limit": limit},
            )
            rows = cur.fetchall()
            return [ExtractionRecord(**row) for row in rows]
