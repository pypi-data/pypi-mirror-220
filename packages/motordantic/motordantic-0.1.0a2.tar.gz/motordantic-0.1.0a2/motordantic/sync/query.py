from typing import Type

from ..query.query import QueryBuilder, BaseQuery

__all__ = ('SyncQuery', 'SyncQueryBuilder')


class SyncQuery(BaseQuery):
    def __getattr__(self, method_name: str) -> 'SyncQuery':
        return SyncQuery(self._builder, method_name)

    def __call__(self, *args, **kwargs):
        method = getattr(self._builder, self.method_name)
        return self._builder.odm_manager._io_loop.run_until_complete(
            method(*args, **kwargs)
        )


class SyncQueryBuilder(QueryBuilder):
    query_class: Type[BaseQuery] = SyncQuery
