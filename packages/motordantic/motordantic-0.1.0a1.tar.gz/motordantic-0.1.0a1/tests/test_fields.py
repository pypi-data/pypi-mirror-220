import pytest_asyncio
import pytest

from bson import ObjectId

from motordantic.document import Document
from motordantic.fields import ExtraDBField
from motordantic.exceptions import NotDeclaredField


class FieldDoc(Document):
    doc_id: str = ExtraDBField(db_field_name='documentId')
    name: str = ExtraDBField(db_field_name='documentName')


class AggDoc(Document):
    doc_id: str = ExtraDBField(db_field_name='documentId')
    cost: float = ExtraDBField(db_field_name='price')


@pytest_asyncio.fixture(scope='session', autouse=True)
async def drop_field_doc(event_loop, connection):
    yield
    await FieldDoc.Q.drop_collection(force=True)
    await AggDoc.Q.drop_collection(force=True)


@pytest.mark.asyncio
async def test_save(connection):
    doc = FieldDoc(doc_id='123', name='first document')
    await doc.save()
    assert doc._id is not None

    native_result = await FieldDoc.manager.collection.find_one({'_id': doc._id})
    assert native_result.get('documentId') == doc.doc_id
    assert native_result.get('documentName') == doc.name


@pytest.mark.asyncio
async def test_find_one(connection):
    doc = await FieldDoc.Q.find_one(doc_id='123')
    assert doc is not None
    assert doc.doc_id == '123'
    assert doc.name == 'first document'

    with pytest.raises(NotDeclaredField):
        doc = await FieldDoc.Q.find_one(documentId='123')
        assert doc == 1


@pytest.mark.asyncio
async def test_insert_one(connection):
    data = {'doc_id': '2222', 'name': 'second'}
    object_id = await FieldDoc.Q.insert_one(**data)
    assert isinstance(object_id, ObjectId)


@pytest.mark.asyncio
async def test_update_in_save(connection):
    doc = await FieldDoc.Q.find_one(doc_id__regex='2222')
    assert doc is not None
    doc.name = 'second document'
    await doc.save()
    native_result = await FieldDoc.manager.collection.find_one({'_id': doc._id})
    assert native_result.get('documentName') == 'second document'


@pytest.mark.asyncio
async def test_simple_aggregate(connection):

    data = [{'doc_id': '1', 'cost': 5000}, {'doc_id': '2', 'cost': 6000}]
    c = await AggDoc.Q.insert_many(data)
    assert c == 2
    sum_ = await AggDoc.Q.aggregate_sum('cost')
    assert sum_ == 11000

    max_ = await AggDoc.Q.aggregate_max('cost')
    assert max_ == 6000
    min_ = await AggDoc.Q.aggregate_min('cost')
    assert min_ == 5000
    avg_ = await AggDoc.Q.aggregate_avg('cost')
    assert avg_ == 5500.0
