from dataclasses import dataclass
from uuid import uuid4

from psycopg.rows import dict_row

from db.connection import get_conn


@dataclass(frozen=True)
class PayoutRunRecord:
    run_id: str
    month: str
    extraction_id: str | None
    status: str
    inputs_json: dict
    outputs_json: dict | None
    audit_json: dict | None


def new_payout_run(
    month: str,
    status: str,
    inputs_json: dict,
    outputs_json: dict | None = None,
    audit_json: dict | None = None,
    extraction_id: str | None = None,
) -> PayoutRunRecord:
    return PayoutRunRecord(
        run_id=uuid4().hex,
        month=month,
        extraction_id=extraction_id,
        status=status,
        inputs_json=inputs_json,
        outputs_json=outputs_json,
        audit_json=audit_json,
    )


def create_payout_run(record: PayoutRunRecord) -> PayoutRunRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO payout_runs (
                  run_id,
                  month,
                  extraction_id,
                  status,
                  inputs_json,
                  outputs_json,
                  audit_json
                )
                VALUES (
                  %(run_id)s,
                  %(month)s,
                  %(extraction_id)s,
                  %(status)s,
                  %(inputs_json)s,
                  %(outputs_json)s,
                  %(audit_json)s
                )
                RETURNING run_id, month, extraction_id, status, inputs_json, outputs_json, audit_json
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return PayoutRunRecord(**row)


def update_payout_run(record: PayoutRunRecord) -> PayoutRunRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                UPDATE payout_runs
                SET status = %(status)s,
                    inputs_json = %(inputs_json)s,
                    outputs_json = %(outputs_json)s,
                    audit_json = %(audit_json)s
                WHERE run_id = %(run_id)s
                RETURNING run_id, month, extraction_id, status, inputs_json, outputs_json, audit_json
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return PayoutRunRecord(**row)


def get_payout_run(run_id: str) -> PayoutRunRecord | None:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT run_id, month, extraction_id, status, inputs_json, outputs_json, audit_json
                FROM payout_runs
                WHERE run_id = %(run_id)s
                """,
                {"run_id": run_id},
            )
            row = cur.fetchone()
            return PayoutRunRecord(**row) if row else None


def list_payout_runs(limit: int = 50) -> list[PayoutRunRecord]:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT run_id, month, extraction_id, status, inputs_json, outputs_json, audit_json
                FROM payout_runs
                ORDER BY created_at DESC
                LIMIT %(limit)s
                """,
                {"limit": limit},
            )
            rows = cur.fetchall()
            return [PayoutRunRecord(**row) for row in rows]
