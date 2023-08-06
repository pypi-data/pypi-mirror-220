import pytest
import pytest_asyncio

from motordantic.exceptions import MotordanticValidationError
from motordantic.document import Document


class TestField(str):
    type_ = str
    required = False
    default = None
    validate_always = False
    alias = ''

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not value or value == 'no':
            raise ValueError('invalid value')
        return value


class Validate(Document):
    name: str
    position: int
    config: dict
    sign: int = 1
    type_: str = 'ga'
    test: TestField = TestField('test value')
    array: list = [1, 2]


@pytest_asyncio.fixture(scope='session', autouse=True)
async def drop_ticket_collection(event_loop):
    yield
    await Validate.Q.drop_collection(force=True)


@pytest.mark.asyncio
async def test_validate(connection):
    with pytest.raises(MotordanticValidationError):
        await Validate.Q.find_one(array='invalid')

    with pytest.raises(MotordanticValidationError):
        await Validate.Q.find_one(_id='invalid')

    with pytest.raises(MotordanticValidationError):
        await Validate.Q.find_one(position='invalid')
        await Validate.Q.find_one(config='invalid')

    with pytest.raises(MotordanticValidationError):
        Validate(
            array={'invalid': 'true'},
            name='123',
            position='invalid postion',
            config={},
        )

    with pytest.raises(MotordanticValidationError):
        Validate(array=[], name='123', position=1, config={}, test='no')
