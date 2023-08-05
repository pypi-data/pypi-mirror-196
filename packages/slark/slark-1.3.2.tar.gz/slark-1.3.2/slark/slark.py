from __future__ import annotations
import os.path
import orjson as json


class SlarkException(Exception):
    pass


class SlarkDB:
    db_name: str = 'db.json'
    __content: dict

    def __init__(self, db_name: str | None = None, table_name: str | None = None):
        if db_name:
            self.db_name = db_name
        if not os.path.exists(self.db_name):
            open(self.db_name, 'w').close()
        if table_name:
            self._table_name = table_name

    def __str__(self) -> str:
        self._refresh()
        db = ',\n'.join(f'    {k}: {len(v)} records' for k, v in self.content.items())
        return f'{self.__class__.__name__}(\n{db}\n)'

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def content(self) -> dict:
        return self.__content

    def __write(self) -> None:
        with open(self.db_name, 'bw') as file:
            file.write(json.dumps(self.content))

    def _write_table(self, rows: list) -> None:
        self.content[self._table_name] = rows
        self.__write()

    def _drop_table(self) -> None:
        del self.content[self._table_name]
        self.__write()

    def _refresh(self) -> None:
        # TODO: Find Solution, so won't refresh on every single query
        with open(self.db_name, 'rb') as file:
            data = file.read()
            self.__content = json.loads(data) if data else {}

    def table(self, table_name: str) -> SlarkTable:
        return SlarkTable(db_name=self.db_name, table_name=table_name)


class SlarkTable(SlarkDB):
    _table_name: str | None = None

    def __init__(self, table_name: str, db_name: str, **kwargs):
        super().__init__(db_name=db_name, table_name=table_name)
        self._table_name = table_name

    def __str__(self) -> str:
        self._refresh()
        records = self.content[self.table_name]
        if not records:
            return f'{self.__class__.__name__}(\n    table_name: {self.table_name}\n)'

        result = '\n'.join(f'    {k}: {type(v).__name__}' for k, v in records[0].items())
        return f'{self.__class__.__name__}(\n    table_name: {self.table_name}\n\n{result}\n)'

    def __check_is_slark_obj(self) -> None:
        if not hasattr(self, '_id'):
            raise SlarkException('You should call this method on SlarkObject instance.')

    def __create_object(self, data: dict, /) -> SlarkObject:
        return SlarkObject(table_name=self.table_name, db_name=self.db_name, **data)

    def _get_table(self) -> list[dict]:
        """return records"""
        if self._table_name is None:
            raise SlarkException('You should call table() first.')

        self._refresh()
        return self.content.get(self._table_name, [])

    def create(self, **kwargs) -> SlarkObject:
        rows = self._get_table()
        kwargs['_id'] = len(rows) + 1
        rows.append(kwargs)
        self._write_table(rows)
        return self.__create_object(kwargs)

    def get(self, **kwargs) -> SlarkObject | None:
        found = None
        for r in self._get_table():
            for k, v in kwargs.items():
                if r.get(k) == v:
                    if found:
                        raise SlarkException('Multiple object found for this kwargs')
                    found = self.__create_object(r)
        return found

    def first(self, **kwargs) -> SlarkObject | None:
        rows = self._get_table()
        if not kwargs:
            return self.__create_object(rows[0])

        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                return self.__create_object(r)

    def last(self, **kwargs) -> SlarkObject | None:
        rows = self._get_table()
        rows.reverse()

        if not kwargs:
            return self.__create_object(rows[0])

        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                return self.__create_object(r)

    def filter(self, **kwargs) -> list[SlarkObject]:
        if not kwargs:
            return self.all()

        result = list()
        for r in self._get_table():
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                result.append(self.__create_object(r))
        return result

    def all(self) -> list[SlarkObject]:
        return [self.__create_object(r) for r in self._get_table()]

    def count(self, **kwargs) -> int:
        rows = self._get_table()
        if not kwargs:
            return len(rows)

        result = 0
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                result += 1
        return result

    def delete(self):
        self.__check_is_slark_obj()
        rows = self._get_table()
        for r in rows:
            if r.get('_id') == self._id:
                rows.remove(r)
                self._write_table(rows)
                break

    def delete_one(self, **kwargs) -> bool:
        rows = self._get_table()
        if not kwargs:
            return False

        index = 0
        found = False
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                found = True
                break
            index += 1

        # Didn't find any match
        if not found:
            return False

        # Delete Matched One
        rows.pop(index)
        self._write_table(rows)
        return True

    def delete_many(self, **kwargs) -> int:
        rows = self._get_table()
        if not kwargs:
            return 0

        indexes = list()
        index = 0
        found = False
        for r in rows:
            for k, v in kwargs.items():
                if r.get(k) != v:
                    break
            else:
                indexes.append(index)
                found = True
            index += 1

        # Didn't find any match
        if not found:
            return 0

        # Delete Matched Indexes
        for i in indexes[::-1]:
            rows.pop(i)
        self._write_table(rows)
        return len(indexes)

    def update(self, **kwargs):
        self.__check_is_slark_obj()
        rows = self._get_table()
        for r in rows:
            if r.get('_id') == self._id:
                for k, v in kwargs.items():
                    r[k] = v
                self._write_table(rows)

    def update_one(self, condition: dict, **kwargs) -> bool:
        rows = self._get_table()
        result = False

        if not condition:
            return result

        for r in rows:
            for k, v in condition.items():
                if r.get(k) != v:
                    break
            else:
                result = True
                for new_k, new_v in kwargs.items():
                    r[new_k] = new_v
                self._write_table(rows)
                break

        return result

    def update_many(self, condition: dict, **kwargs) -> int:
        rows = self._get_table()
        if not condition:
            return 0

        updated_count = 0
        for r in rows:
            for k, v in condition.items():
                if r.get(k) != v:
                    break
            else:
                updated_count += 1
                for new_k, new_v in kwargs.items():
                    r[new_k] = new_v

        if updated_count:
            self._write_table(rows)
        return updated_count

    def drop(self) -> None:
        self._get_table()
        self._drop_table()


class SlarkObject(SlarkTable):
    __data: dict

    def __init__(self, table_name: str, db_name: str, **kwargs):
        super().__init__(db_name=db_name, table_name=table_name)
        self.__data = kwargs

    def __str__(self) -> str:
        items = ', '.join(f'id={v}' if k == '_id' else f'{k}={v}' for k, v in self.__data.items())
        return f'{self.table_name}({items})'

    __repr__ = __str__

    def __getattr__(self, item: str):
        try:
            return object.__getattribute__(self, '_SlarkObject__data')[item]
        except KeyError:
            raise SlarkException(f'Invalid Table Key: "{item}"')

    def __setattr__(self, key, value):
        if key not in ['_SlarkObject__data', '_SlarkDB__content']:
            try:
                object.__getattribute__(self, key)
            except AttributeError:
                self.__data[key] = value
                return

        super().__setattr__(key, value)

    @property
    def id(self) -> int:
        return self.__data['_id']

    @property
    def data(self) -> dict:
        return self.__data

    def save(self) -> None:
        """Pop the old data & Insert new data at the index"""
        records = self._get_table()
        for i, r in enumerate(records):
            if r['_id'] == self.id:
                records.pop(i)
                records.insert(i, self.__data)
        super()._write_table(rows=records)

    def json(self) -> str:
        return json.dumps(self.__data).decode()
