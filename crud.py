from typing import List, Any

from pydantic.schema import date
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

import pagnation
from models import Car, Record

PAGE_SIZE = 5


def read_car(db: Session):
    """

    :param db:
    :return:
    """
    cars: List[Any] = db.query(Car).all()
    return cars


def read_search_record(db: Session):
    """
    :param db:
    :return:
    """
    return db.query(Record).all()


def read_all_record(db: Session, carno: str = '', start: date = None, end: date = None, page: int = 1):
    """
    :param db:
    :param carno:
    :param start:
    :param end:
    :param page:
    :return:
    """
    url = "/api/record/?"
    records = db.query(Record)
    if carno:
        records = records.join(Car).filter(or_(
            Car.carno.like("%" + carno + "%"),
            Car.owner.like("%" + carno + "%")))
        url += f"carno={carno}&"
    if all([start, end]):
        records = records.filter(and_(Record.makedate <= end, Record.makedate >= start))
        url += f"start={start}&end={end}"
    count = (len(records.all()) + PAGE_SIZE - 1) / PAGE_SIZE
    if page:
        records = records.limit(PAGE_SIZE).offset((page - 1) * PAGE_SIZE)
    records = records.all()
    return pagnation.pagenation(records, url, page, count)


def update_dealt(db: Session, record_id: int):
    """
    :param db:
    :param record_id:
    :return:
    """
    try:
        record = db.query(Record).get(record_id)
        record.dealt = True
        db.add(record)
        db.commit()
        return {'code': 10000, 'msg': "Success update car's record "}
    except Exception as e:
        print(e)
    return {'code': 10001, 'msg': " Fail update car's record "}


def del_record(db: Session, record_id: int):
    """
    :param db:
    :param record_id:
    :return:
    """
    try:
        record = db.query(Record).get(record_id)
        if record.dealt:
            db.delete(record)
            db.commit()
            return {'code': 10000, 'msg': " Success del car's record "}
    except Exception as e:
        print(e)
    return {'code': 10001, 'msg': " Fail del car's record "}
