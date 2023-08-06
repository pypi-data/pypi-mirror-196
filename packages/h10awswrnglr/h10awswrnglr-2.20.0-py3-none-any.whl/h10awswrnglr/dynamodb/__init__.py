"""Amazon DynamoDB Module."""

from h10awswrnglr.dynamodb._delete import delete_items
from h10awswrnglr.dynamodb._read import read_items, read_partiql_query
from h10awswrnglr.dynamodb._utils import execute_statement, get_table
from h10awswrnglr.dynamodb._write import put_csv, put_df, put_items, put_json

__all__ = [
    "delete_items",
    "execute_statement",
    "get_table",
    "put_csv",
    "put_df",
    "put_items",
    "put_json",
    "read_partiql_query",
    "read_items",
]
