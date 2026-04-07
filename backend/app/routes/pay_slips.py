from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.models import PaySlip, User
from app.schemas.schemas import PaySlipCreate, PaySlipResponse

router = APIRouter()

@router.post("/pay-slips", response_model=PaySlipResponse)
def generate_pay_slip(payload: PaySlipCreate, db: Session = Depends(get_db)):
    # Verify employee exists
    emp = db.query(User).filter(User.employee_id == payload.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
        
    new_slip = PaySlip(
        employee_id=payload.employee_id,
        month=payload.month,
        amount=payload.amount,
        status=payload.status,
        project_id=payload.project_id
    )
    db.add(new_slip)
    db.commit()
    db.refresh(new_slip)
    
    # Attach name for response
    new_slip.employee_name = emp.name
    return new_slip

@router.get("/pay-slips", response_model=List[PaySlipResponse])
def get_all_pay_slips(project_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(PaySlip).order_by(PaySlip.created_at.desc())
    if project_id and project_id != 'null':
        query = query.filter(PaySlip.project_id == project_id)
    
    results = query.all()
    
    # Attach employee names
    for slip in results:
        emp = db.query(User).filter(User.employee_id == slip.employee_id).first()
        slip.employee_name = emp.name if emp else "Unknown"
        
    return results

@router.get("/pay-slips/my/{employee_id}", response_model=List[PaySlipResponse])
def get_my_pay_slips(employee_id: str, db: Session = Depends(get_db)):
    results = db.query(PaySlip).filter(PaySlip.employee_id == employee_id).order_by(PaySlip.created_at.desc()).all()
    for slip in results:
        emp = db.query(User).filter(User.employee_id == slip.employee_id).first()
        slip.employee_name = emp.name if emp else "Unknown"
    return results
