import re
from typing import Any, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

FIELD_REGEX = re.compile(r"^[a-zA-Z0-9_]+$")
ALLOWED_ORDER_OPTIONS = ["ASC", "DESC"]
OPERATORS_MAP = {
    "eq": "=",
    "neq": "!=",
    "lt": "<",
    "gt": ">",
    "lte": "<=",
    "gte": ">=",
}


class Queryer:
    def __init__(
        self, dsn: str, connect_args: Optional[dict] = None, echo: bool = False
    ) -> None:
        connect_args = connect_args or {}
        self.engine = create_engine(dsn, echo=echo, connect_args=connect_args)

    def _build_statement(
        self,
        table_name: str,
        filters: list[tuple[str, str]],
        order: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[str, dict[str, Any]]:
        if not self._valid_field(table_name):
            raise ValueError(f"Invalid table name: {table_name}")
        where, params = self._build_where_condition_and_params(filters)
        return (
            f"SELECT * FROM {table_name}"
            f"{where}{self._build_order(order)} "
            f"LIMIT {limit} OFFSET {offset}"
        ), params

    def _build_order(self, order: Optional[str] = None) -> str:
        if order is None:
            return ""
        match order.split():
            case [field]:
                if not self._valid_field(field):
                    raise ValueError(f"Invalid field: {field}")
                return f" ORDER BY {field} ASC"
            case [field, option]:
                if not self._valid_field(field):
                    raise ValueError(f"Invalid field: {field}")
                option = option.upper()
                if option not in ALLOWED_ORDER_OPTIONS:
                    raise ValueError(f"Invalid order option: {option}")
                return f" ORDER BY {field} {option}"
            case _:
                raise ValueError(f"Invalid order option: {order}")

    def _build_where_condition_and_params(
        self, filters: list[tuple[str, Any]]
    ) -> tuple[str, dict[str, Any]]:
        result = ""
        params = {}
        wheres = []
        if filters:
            result += " WHERE "
        for idx, filter in enumerate(filters):
            field, operator, value = self._split_filter(filter)
            if not self._valid_field(field):
                raise ValueError(f"Invalid field: {field}")
            placeholder = f"param__{idx}"
            match operator:
                case "eq" | "neq" | "lt" | "gt" | "lte" | "gte":
                    operator = OPERATORS_MAP[operator]
                    wheres.append(f"{field} {operator} :{placeholder}")
                    params[placeholder] = value
                case "startswith":
                    operator = "LIKE"
                    value = f"{value}%"
                    wheres.append(f"{field} {operator} :{placeholder}")
                    params[placeholder] = value
                case "endswith":
                    operator = "LIKE"
                    value = f"%{value}"
                    wheres.append(f"{field} {operator} :{placeholder}")
                    params[placeholder] = value
                case "contains":
                    operator = "LIKE"
                    value = f"%{value}%"
                    wheres.append(f"{field} {operator} :{placeholder}")
                    params[placeholder] = value
                case "icontains":
                    operator = "LIKE"
                    value = f"%{value}%"
                    wheres.append(f"LOWER({field}) {operator} :{placeholder}")
                    params[placeholder] = value.lower()
                case "isnull":
                    operator = "IS NULL" if value else "IS NOT NULL"
                    wheres.append(f"{field} {operator}")
                case _:
                    raise ValueError(f"Invalid operator: {operator}")
        result += " AND ".join(wheres)
        return result, params

    def _split_filter(self, filter: tuple[str, str]) -> tuple[str, str, Any]:
        """
        Splits a filter tuple into its individual components.

        Args:
            filter (tuple[str, str]): The filter tuple to be split.

        Returns:
            tuple[str, str, Any]: A tuple containing the field, operator, and value extracted from the filter tuple.
        """  # noqa: E501
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

    def _valid_field(self, field: str) -> bool:
        if not FIELD_REGEX.match(field):
            return False
        return True

    def query(
        self,
        resource_name: str,
        filters: list[tuple[str, Any]],
        order: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """
        Executes a query on the database using the provided parameters and returns the results.

        Args:
            resource_name (str): The name of the resource to query.
            filters (list[tuple[str, Any]]): A list of tuples representing the filters to apply to the query.
            order (Optional[str]): The field to order the results by. Defaults to None.
            limit (int): The maximum number of results to return. Defaults to 10.
            offset (int): The number of results to skip. Defaults to 0.

        Returns:
            list[dict[str, Any]]: A list of dictionaries representing the query results. Each dictionary contains the column names as keys and the corresponding row values.

        """  # noqa: E501
        stmt, params = self._build_statement(
            resource_name, filters, order, limit, offset
        )
        with Session(self.engine) as session:
            result = session.execute(text(stmt), params)
            columns = result.keys()
            rows = result.fetchall()
            return [dict(zip(columns, row)) for row in rows]
