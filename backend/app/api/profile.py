from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from app.dependencies.database import get_db
from app.models.user import User
from app.models.daily_stats import DailyStats
from sqlalchemy import func

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me")
def get_my_profile(request: Request, db: Session = Depends(get_db)):
    # auth_middleware ne request.state.user_id set kiya tha — wahi use karo
    user_id = request.state.user_id

    # User dhundo DB mein by ID
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Total solved problems count karo daily_stats se
    # func.sum() SQL ka SUM() function hai
    total_solved = db.query(func.sum(DailyStats.correct))\
        .filter_by(user_id=user_id).scalar() or 0

    # Total attempts count karo
    total_attempted = db.query(func.sum(DailyStats.solved))\
        .filter_by(user_id=user_id).scalar() or 0

    # Overall accuracy calculate karo
    accuracy = round(total_solved / total_attempted * 100, 1) if total_attempted else 0

    # Active days count karo (kitne alag-alag dates pe kaam kiya)
    active_days = db.query(func.count(DailyStats.date))\
        .filter_by(user_id=user_id).scalar() or 0

    return {
        "user_id": user.id,
        "username": user.username,
        "rating": user.rating,       
        "total_solved": total_solved,
        "total_attempted": total_attempted,
        "accuracy": accuracy,
        "active_days": active_days,
    }


@router.put("/cf-handle")
def update_cf_handle(request: Request, body: dict, db: Session = Depends(get_db)):
    # User apna Codeforces handle update kar sake
    user_id = request.state.user_id
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # body mein {"cf_handle": "tourist"} hoga
    new_handle = body.get("cf_handle", "").strip()
    if not new_handle:
        raise HTTPException(status_code=400, detail="Handle cannot be empty")

    user.cf_handle = new_handle  # DB mein save
    db.commit()
    return {"message": "Handle updated", "cf_handle": new_handle}