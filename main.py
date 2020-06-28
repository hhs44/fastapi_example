from fastapi import FastAPI, Depends
from pydantic.schema import date
from sqlalchemy.orm import Session
# from starlette.requests import Request
# from starlette.responses import FileResponse
# from starlette.staticfiles import StaticFiles

import crud
import schemas
from database import SessionLocal


def get_db():
    """
    获取事务
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"))
#
#
# @app.get("/")
# async def index(request: Request):
#     """
#
#     :param request:
#     :return:
#     """
#     return FileResponse('./static/index.html')


@app.get("/api/car", name="获取车辆信息", description="获取所有车辆信息")
async def get_car(db: Session = Depends(get_db)):
    """

    :param db:
    :return:
    """
    car = crud.read_car(db)
    return car


@app.get("/api/record/", name="获取所有违章记录", description="获取所有违章记录", response_model=schemas.Latest)
async def get_all_record(page: int = 1, carno: str = None, start: date = None, end: date = None,
                         db: Session = Depends(get_db)):
    """
    :param page:
    :param carno:
    :param start:
    :param end:
    :param db:
    :return:
    """
    latest = crud.read_all_record(carno=carno, start=start, end=end, page=page, db=db)
    return latest


@app.patch("/api/record/{record_id}", name="update car record", description="处理违章记录", response_model=schemas.Dealt)
async def dealt_record(record_id: int, db: Session = Depends(get_db)):
    """
    :param record_id:
    :param db:
    :return:
    """
    dealt = crud.update_dealt(db=db, record_id=record_id)
    return dealt


@app.delete("/api/record/{record_id}", name="del car record", description="删除违章记录", response_model=schemas.Dealt)
async def dealt_record(record_id: int, db: Session = Depends(get_db)):
    """
    :param record_id:
    :param db:
    :return:
    """
    dealt = crud.del_record(db=db, record_id=record_id)
    return dealt


if __name__ == '__main__':
    import uvicorn

    # uvicorn main: app --reload
    uvicorn.run(app, host='127.0.0.1', port=8000)
