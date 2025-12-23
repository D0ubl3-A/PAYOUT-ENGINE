from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4

from psycopg.rows import dict_row

from db.connection import get_conn


@dataclass(frozen=True)
class InvoiceRecord:
    invoice_id: str
    run_id: str
    month: str
    recipient_type: str
    recipient_id: str
    invoice_number: str
    status: str
    file_format: str
    filename: str
    content_type: str
    storage_path: str
    size_bytes: int
    sha256: str
    total_usd: Decimal


def new_invoice_record(
    *,
    run_id: str,
    month: str,
    recipient_type: str,
    recipient_id: str,
    invoice_number: str,
    status: str,
    file_format: str,
    filename: str,
    content_type: str,
    storage_path: str,
    size_bytes: int,
    sha256: str,
    total_usd: Decimal,
) -> InvoiceRecord:
    return InvoiceRecord(
        invoice_id=uuid4().hex,
        run_id=run_id,
        month=month,
        recipient_type=recipient_type,
        recipient_id=recipient_id,
        invoice_number=invoice_number,
        status=status,
        file_format=file_format,
        filename=filename,
        content_type=content_type,
        storage_path=storage_path,
        size_bytes=size_bytes,
        sha256=sha256,
        total_usd=total_usd,
    )


def create_invoice(record: InvoiceRecord) -> InvoiceRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO invoices (
                  invoice_id,
                  run_id,
                  month,
                  recipient_type,
                  recipient_id,
                  invoice_number,
                  status,
                  file_format,
                  filename,
                  content_type,
                  storage_path,
                  size_bytes,
                  sha256,
                  total_usd
                )
                VALUES (
                  %(invoice_id)s,
                  %(run_id)s,
                  %(month)s,
                  %(recipient_type)s,
                  %(recipient_id)s,
                  %(invoice_number)s,
                  %(status)s,
                  %(file_format)s,
                  %(filename)s,
                  %(content_type)s,
                  %(storage_path)s,
                  %(size_bytes)s,
                  %(sha256)s,
                  %(total_usd)s
                )
                RETURNING invoice_id, run_id, month, recipient_type, recipient_id,
                          invoice_number, status, file_format, filename, content_type,
                          storage_path, size_bytes, sha256, total_usd
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return InvoiceRecord(**row)


def get_invoice(invoice_id: str) -> InvoiceRecord | None:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT invoice_id, run_id, month, recipient_type, recipient_id,
                       invoice_number, status, file_format, filename, content_type,
                       storage_path, size_bytes, sha256, total_usd
                FROM invoices
                WHERE invoice_id = %(invoice_id)s
                """,
                {"invoice_id": invoice_id},
            )
            row = cur.fetchone()
            return InvoiceRecord(**row) if row else None


def list_invoices(run_id: str | None = None, limit: int = 200) -> list[InvoiceRecord]:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            if run_id:
                cur.execute(
                    """
                    SELECT invoice_id, run_id, month, recipient_type, recipient_id,
                           invoice_number, status, file_format, filename, content_type,
                           storage_path, size_bytes, sha256, total_usd
                    FROM invoices
                    WHERE run_id = %(run_id)s
                    ORDER BY created_at DESC
                    LIMIT %(limit)s
                    """,
                    {"run_id": run_id, "limit": limit},
                )
            else:
                cur.execute(
                    """
                    SELECT invoice_id, run_id, month, recipient_type, recipient_id,
                           invoice_number, status, file_format, filename, content_type,
                           storage_path, size_bytes, sha256, total_usd
                    FROM invoices
                    ORDER BY created_at DESC
                    LIMIT %(limit)s
                    """,
                    {"limit": limit},
                )
            rows = cur.fetchall()
            return [InvoiceRecord(**row) for row in rows]
