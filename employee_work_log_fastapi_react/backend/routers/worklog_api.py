from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from backend.database import get_db
from backend.dependencies import get_current_user, require_admin
from backend.models import User, WorkLog
from backend.schemas import WorkLogCreate, WorkLogOut, WorkLogUpdate

router = APIRouter(prefix="/api/worklogs", tags=["Work Logs"])
VALID_STATUSES = {"Pending", "In Progress", "Completed"}


def validate_status(status_value: str):
    if status_value not in VALID_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be Pending, In Progress or Completed",
        )


def to_worklog_out(log: WorkLog) -> WorkLogOut:
    return WorkLogOut(
        id=log.id,
        user_id=log.user_id,
        user_full_name=log.user.full_name if log.user else None,
        date=log.date,
        task=log.task,
        hours=log.hours,
        status=log.status,
        project=log.project,
        comments=log.comments,
    )


@router.get("", response_model=list[WorkLogOut])
def get_work_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    logs = db.query(WorkLog).options(joinedload(WorkLog.user)).order_by(WorkLog.date.desc()).all()
    return [to_worklog_out(log) for log in logs]


@router.post("", response_model=WorkLogOut, status_code=status.HTTP_201_CREATED)
def create_work_log(
    log_data: WorkLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_status(log_data.status)

    log = WorkLog(
        user_id=current_user.id,
        date=log_data.date,
        task=log_data.task.strip(),
        hours=log_data.hours,
        status=log_data.status,
        project=log_data.project.strip(),
        comments=(log_data.comments or "").strip(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    log = db.query(WorkLog).options(joinedload(WorkLog.user)).filter(WorkLog.id == log.id).first()
    return to_worklog_out(log)


@router.put("/{log_id}", response_model=WorkLogOut)
def update_work_log(
    log_id: int,
    log_data: WorkLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_status(log_data.status)

    log = db.query(WorkLog).filter(WorkLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work log not found")

    log.date = log_data.date
    log.task = log_data.task.strip()
    log.hours = log_data.hours
    log.status = log_data.status
    log.project = log_data.project.strip()
    log.comments = (log_data.comments or "").strip()
    db.commit()
    db.refresh(log)
    log = db.query(WorkLog).options(joinedload(WorkLog.user)).filter(WorkLog.id == log.id).first()
    return to_worklog_out(log)


@router.delete("/{log_id}")
def delete_work_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    log = db.query(WorkLog).filter(WorkLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Work log not found")

    db.delete(log)
    db.commit()
    return {"message": "Work log deleted successfully"}
