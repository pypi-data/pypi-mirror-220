import re
from dataclasses import dataclass
from typing import Any, Optional

from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.orm import Session

OPERATOR_TO_SQL = {
    "eq": "=",
    "neq": "!=",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
    "in": "IN",
}


@dataclass
class Filter:
    field_name: str
    placeholder: str
    operator: str
    value: Any


class Queryer:
    def __init__(self, dsn: str) -> None:
        self.engine = create_engine(dsn, echo=True)

    def _split_filter(self, filter: tuple[str, str]) -> tuple[str, str, Any]:
        value = filter[1]
        if "__" not in filter[0]:
            field = filter[0]
            operator = "eq"
        else:
            sep = filter[0].split("__")
            if len(sep) != 2:
                field = "".join(sep[:-1])
                operator = sep[-1]
            else:
                field, operator = sep
        return field, operator, value

    def _parse_filters(self, filters: list[tuple[str, Any]]) -> list[Filter]:
        results = []
        for idx, filter in enumerate(filters):
            field, operator, value = self._split_filter(filter)
            placeholder = f"{field}__{idx}"
            match operator:
                case "startswith":
                    operator = "LIKE"
                    value = f"{value}%"
                case "endswith":
                    operator = "LIKE"
                    value = f"%{value}"
                case "contains":
                    operator = "LIKE"
                    value = f"%{value}%"
                case "icontains":
                    operator = "LIKE"
                    value = f"%{value}%"
                    field = f"LOWER({field})"
                case _:
                    operator = OPERATOR_TO_SQL.get(operator)
            if operator is None:
                raise ValueError("Invalid operator")
            results.append(
                Filter(
                    field_name=field,
                    placeholder=placeholder,
                    operator=operator,
                    value=value,
                )
            )
        return results

    def _build_where_conditions(self, conditions: list[Filter]) -> str:
        if len(conditions) == 0:
            return ""
        return " WHERE " + " AND ".join(
            [
                f"{filter.field_name} {filter.operator} :{filter.placeholder}"
                for filter in conditions
            ]
        )

    def _check_table_name(self, table_name: str) -> None:
        TABLE_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_]+$")
        if not TABLE_NAME_REGEX.match(table_name):
            raise ValueError("Invalid table name")

    def _check_if_fields_in_table(
        self, table_name: str, parsed_filters: list[tuple[str, str, Any]]
    ) -> None:
        metadata = MetaData()
        table = Table(table_name, metadata, autoload=True, autoload_with=self.engine)
        select_stmt = table.select()
        with Session(self.engine) as session:
            session.execute(select_stmt)
            column_names = set(table.columns.keys())
            for field in parsed_filters:
                if field[0] not in column_names:
                    raise ValueError(f"Invalid field {field[0]}")

    def query(
        self,
        resource_name: str,
        filters: list[tuple[str, Any]],
        order: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Executes a query on the specified resource.

        Args:
            resource_name (str): The name of the resource to query.
            filters (list[tuple[str, Any]]): A list of tuples representing the filters to apply.
            order (Optional[str], optional): The field to order the results by. Defaults to None.
            limit (int, optional): The maximum number of results to return. Defaults to 10.
            offset (int, optional): The number of results to skip. Defaults to 0.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the query results.
        """  # noqa: E501
        self._check_table_name(resource_name)
        parsed_filters = self._parse_filters(filters)
        where_conditions = self._build_where_conditions(parsed_filters)
        query_sql = f'SELECT * FROM "{resource_name}"{where_conditions}'
        if order is not None:
            query_sql += " ORDER BY :_order"
        query_sql += " LIMIT :_limit OFFSET :_offset"
        statement = text(query_sql)
        params = {
            **{filter.placeholder: filter.value for filter in parsed_filters},
            **{"_limit": limit, "_offset": offset},
        }
        if order is not None:
            params["_order"] = order
        with Session(self.engine) as session:
            result = session.execute(statement, params)
            return [dict(row) for row in result]
