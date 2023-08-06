import pytest
import pytest_asyncio

from motordantic.document import Document
from motordantic.fields import computed_field
from motordantic.exceptions import MotordanticValidationError
from pydantic import BaseModel


class Config(BaseModel):
    path: str = '/home/'
    env: str = 'test'


class Application(Document):
    name: str
    config: Config
    lang: str

    @computed_field
    def lang_upper(self) -> str:
        return self.lang.upper()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def application_data(connection):
    application = await Application(name='test', config=Config(), lang='python').save()
    yield
    await Application.Q.drop_collection(force=True)


def test_schema(connection):
    application = Application(name='test', config=Config(), lang='python')
    assert application.serialize(['lang_upper']) == {'lang_upper': 'PYTHON'}
    assert application.serialize_json(['lang_upper']) == '{"lang_upper": "PYTHON"}'
    assert application.data == {
        'name': 'test',
        'config': {'path': '/home/', 'env': 'test'},
        'lang': 'python',
        'lang_upper': 'PYTHON',
    }
    assert (
        application.json()
        == '{"name": "test", "config": {"path": "/home/", "env": "test"}, "lang": "python", "lang_upper": "PYTHON"}'
    )
    assert application.schema() == {
        'title': 'Application',
        'type': 'object',
        'properties': {
            'name': {'title': 'Name', 'type': 'string'},
            'config': {'$ref': '#/definitions/Config'},
            'lang': {'title': 'Lang', 'type': 'string'},
            'lang_upper': {'title': 'Lang Upper', 'read_only': True, 'type': 'string'},
        },
        'required': ['name', 'config', 'lang'],
        'definitions': {
            'Config': {
                'title': 'Config',
                'type': 'object',
                'properties': {
                    'path': {'title': 'Path', 'default': '/home/', 'type': 'string'},
                    'env': {'title': 'Env', 'default': 'test', 'type': 'string'},
                },
            }
        },
    }


@pytest.mark.asyncio
async def test_application_data(connection):
    application = await Application.Q.find_one(name='test')
    data = application.data
    assert isinstance(data['config'], dict)
    assert data['config']['env'] == 'test'

    data = await Application.Q.find_one(config__env='test')
    assert data.name == 'test'
    data = await Application.Q.find_one(config__env='invalid')
    assert data is None


@pytest.mark.asyncio
async def test_raise_with_field_mongo_model(connection):
    class Default(Document):
        name: str
        app: Application

    with pytest.raises(MotordanticValidationError):
        await Default(name='default', app=await Application.Q.find_one()).save()
