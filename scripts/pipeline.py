
import subprocess
import sys
from pathlib import Path
from datetime import datetime

from scripts.db import get_conn

ROOT = Path(__file__).resolve().parent.parent

COMMANDS = [
    # Load existing CSV files only. Do not generate new data.
    [sys.executable, "-m", "scripts.load"],

    # Execute all SQL transformations.
    [sys.executable, "-m", "scripts.run_sql"],
]


def create_audit_run(started_at):
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO audit.pipeline_runs (
                    pipeline_name,
                    run_status,
                    started_at,
                    records_loaded
                )
                VALUES (%s, %s, %s, %s)
                RETURNING run_id;
            """, (
                "KSA Banking Data Pipeline",
                "RUNNING",
                started_at,
                0
            ))

            run_id = cursor.fetchone()[0]

        conn.commit()
        return run_id

    finally:
        conn.close()


def update_audit_run(
    run_id,
    status,
    completed_at,
    records_loaded=0,
    error_message=None
):
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE audit.pipeline_runs
                SET
                    run_status = %s,
                    completed_at = %s,
                    records_loaded = %s,
                    error_message = %s
                WHERE run_id = %s;
            """, (
                status,
                completed_at,
                records_loaded,
                error_message,
                run_id
            ))

        conn.commit()

    finally:
        conn.close()


def get_fact_count():
    conn = get_conn()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM core.fact_transactions;
            """)

            return cursor.fetchone()[0]

    finally:
        conn.close()


def main():
    started_at = datetime.now()
    run_id = None

    try:
        run_id = create_audit_run(started_at)

        for command in COMMANDS:
            print("\nRunning:", " ".join(command))

            subprocess.run(
                command,
                cwd=ROOT,
                check=True
            )

        records_loaded = get_fact_count()

        update_audit_run(
            run_id,
            "SUCCESS",
            datetime.now(),
            records_loaded
        )

        print("\nPIPELINE COMPLETED SUCCESSFULLY")
        print("Fact table records:", records_loaded)

    except Exception as error:
        print("\nPIPELINE FAILED:", error)

        if run_id is not None:
            try:
                update_audit_run(
                    run_id,
                    "FAILED",
                    datetime.now(),
                    0,
                    str(error)
                )
            except Exception as audit_error:
                print("Could not update audit log:", audit_error)

        raise


if __name__ == "__main__":
    main()
