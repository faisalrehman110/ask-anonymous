import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("data.db")


def read_database(db_path=DB_PATH):
    """Read all tables in the SQLite database and print them in a clean format."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        ).fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        for table in tables:
            table_name = table["name"]
            columns = [
                row["name"] for row in conn.execute(f"PRAGMA table_info('{table_name}')").fetchall()
            ]
            rows = conn.execute(f"SELECT * FROM '{table_name}'").fetchall()

            print(f"\nTable: {table_name}")

            if not rows:
                print("  (No rows found)")
                continue

            headers = [str(col) for col in columns]
            formatted_rows = []
            for row in rows:
                values = ["" if value is None else str(value) for value in row]
                formatted_rows.append(values)

            widths = [len(header) for header in headers]
            for row in formatted_rows:
                for i, value in enumerate(row):
                    widths[i] = max(widths[i], len(value))

            header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
            separator = "-+-".join("-" * width for width in widths)
            print(header_line)
            print(separator)

            for row in formatted_rows:
                print(" | ".join(value.ljust(widths[i]) for i, value in enumerate(row)))
    finally:
        conn.close()


if __name__ == "__main__":
    read_database()
