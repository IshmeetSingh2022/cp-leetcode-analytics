

import sys

from app.models.problems import Problem
from app.core.database import SessionLocal
from app.services.codeforces_service import fetch_problemset


def seed_problems() -> int:
    """Fetch all Codeforces problems and insert missing ones. Returns count inserted."""
    db = SessionLocal()
    inserted = 0

    try:
        problems = fetch_problemset()

        for p in problems:
            contest_id = p.get("contestId")
            index = p.get("index")

            if not contest_id or not index:
                continue

            exists = (
                db.query(Problem)
                .filter_by(contest_id=contest_id, index=index)
                .first()
            )

            if exists:
                continue

            problem = Problem(
                contest_id=contest_id,
                index=index,
                name=p.get("name", ""),
                rating=p.get("rating") or 0,
                tags=",".join(p.get("tags", [])),
            )
            db.add(problem)
            inserted += 1

        db.commit()

    except Exception as exc:
        db.rollback()
        print(f"Error: {exc}", file=sys.stderr)
        raise

    finally:
        db.close()

    return inserted


if __name__ == "__main__":
    count = seed_problems()
    print(f"Inserted {count} new problems.")
