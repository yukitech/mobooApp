from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy import desc

def get_all(db: Session):
  return db.query(models.PredictResult).all()

def get_predict_result(db: Session):
  result = db.query( models.PredictResult.id, models.PredictResult.pred_result, models.PredictResult.pred_result_simp).order_by(desc(models.PredictResult.created_at)).first()
  res = dict(id=result.id, pred_result=result.pred_result, pred_result_simp=result.pred_result_simp)
  return res

def get_prob_result(id: int, db: Session):
  result = db.query(models.PredictResult.id, models.PredictResult.prob_result, models.PredictResult.prob_result_simp).filter(models.PredictResult.id == id).first()
  res = dict(id=result.id, pred_result=result.prob_result, pred_result_simp=result.prob_result_simp)
  return res

def save_predict_result(db: Session, result: schemas.PredictResultCreate):
  new_result = models.PredictResult(**result.dict())
  db.add(new_result)
  db.commit()
  db.refresh(new_result)