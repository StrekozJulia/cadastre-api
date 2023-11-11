import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from cadastre.models import Base, QueryModel
from cadastre.database import SessionLocal, engine


class TestQuery:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = SessionLocal()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()
        Base.metadata.drop_all(engine)

    def test_add_valid_data(self):
        self.session.add(QueryModel(
            cadastre_num="47:14:1203001:814",
            latitude="+18.65",
            longitude="-56.658",
            created_at=datetime(2019, 12, 4, 0, 0, 0),
            answer=True
        ))
        self.session.commit()
        query = self.session.query(QueryModel).filter_by(
            cadastre_num="47:14:1203001:814"
        ).first()
        assert query.cadastre_num == "47:14:1203001:814"
        assert query.latitude == "+18.65"
        assert query.longitude == "-56.658"
        assert query.created_at == datetime(2019, 12, 4, 0, 0, 0)
        assert query.answer is True

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_cadastre_num(self):
        query = QueryModel(
            cadastre_num="5",
            latitude="+18.65",
            longitude="-56.658",
            created_at=datetime(2019, 12, 4, 0, 0, 0),
            answer=True
        )
        self.session.add(query)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_latitude(self):
        query = QueryModel(
            cadastre_num="47:14:1203001:814",
            latitude="+180.65",
            longitude="-56.658",
            created_at=datetime(2019, 12, 4, 0, 0, 0),
            answer=True
        )
        self.session.add(query)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_longitude(self):
        query = QueryModel(
            cadastre_num="47:14:1203001:814",
            latitude="+18.65",
            longitude="-560.658",
            created_at=datetime(2019, 12, 4, 0, 0, 0),
            answer=True
        )
        self.session.add(query)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    @pytest.mark.xfail(raises=IntegrityError)
    def test_add_invalid_answer(self):
        query = QueryModel(
            cadastre_num="47:14:1203001:814",
            latitude="+18.65",
            longitude="-560.658",
            created_at=datetime(2019, 12, 4, 0, 0, 0),
            answer=None
        )
        self.session.add(query)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
