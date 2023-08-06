import re
from typing import Any, Optional

from sqlalchemy import MetaData, Table, create_engine, text
from sqlalchemy.orm import Session

SUPPORTED_OPERATORS = {
    "eq",
    "neq",
    "ne",
    "lt",
    "gt",
    "lte",
    "gte",
    "in",
    "startswith",
    "endswith",
    "contains",
    "icontains",
}


class Queryer:
    def __init__(self, dsn: str) -> None:
        self.engine = create_engine(dsn, echo=True)

    def _parse_filters(
        self, filters: list[tuple[str, Any]]
    ) -> list[tuple[str, str, Any]]:
        results = []
        for filter in filters:
            if "__" not in filter[0]:
                results.append((filter[0], "=", filter[1]))
                continue

            sep = filter[0].split("__")
            if len(sep) != 2:
                field = "".join(sep[:-1])
                operator = sep[-1]
            else:
                field, operator = sep

            if operator not in SUPPORTED_OPERATORS:
                raise ValueError("Invalid operator")

            value = filter[1]
            match operator:
                case "eq":
                    results.append((field, "=", value))
                case "neq":
                    results.append((field, "!=", value))
                case "ne":
                    results.append((field, "!=", value))
                case "lt":
                    results.append((field, "<", value))
                case "gt":
                    results.append((field, ">", value))
                case "lte":
                    results.append((field, "<=", value))
                case "gte":
                    results.append((field, ">=", value))
                case "in":
                    results.append((field, "IN", value))
                case "startswith":
                    results.append((field, "LIKE", value + "%"))
                case "endswith":
                    results.append((field, "LIKE", "%" + value))
                case "contains":
                    results.append((field, "LIKE", "%" + value + "%"))
                case "icontains":
                    results.append(
                        (f"LOWER({field})", "LIKE", "%" + str(value).lower() + "%")
                    )
        return results

    def _build_where_conditions(self, conditions: list[tuple[str, str, Any]]) -> str:
        return " AND ".join(
            [
                f"{condition[0]} {condition[1]} :{condition[0]}__{idx}"
                for idx, condition in enumerate(conditions)
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
        self._check_table_name(resource_name)
        parsed_filters = self._parse_filters(filters)
        where_conditions = self._build_where_conditions(parsed_filters)
        query_sql = f'SELECT * FROM "{resource_name}" WHERE {where_conditions} ORDER BY :_order_by LIMIT :_limit OFFSET :_offset'  # noqa: E501
        with Session(self.engine) as session:
            result = session.execute(
                text(query_sql),
                {
                    **{
                        f"{condition[0]}__{idx}": condition[2]
                        for idx, condition in enumerate(parsed_filters)
                    },
                    **{"_order_by": order, "_limit": limit, "_offset": offset},
                },
            )
            return [dict(row) for row in result]
