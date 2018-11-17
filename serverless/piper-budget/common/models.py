""" Set up models for budget software. """
import os

from pony.orm import Database, Required, Optional, PrimaryKey, Set, set_sql_debug

db = Database()


class Account(db.Entity):
    _table_ = ("finance", "accounts")

    id = PrimaryKey(int, auto=True)
    budget_id = Required("Budget")  # maps to budget
    name = Required(str)
    parent_id = Optional(int)  # maps to self
    created_at = Optional(int)

    # foreign references
    from_records = Set("Record", reverse="from_account_id")
    to_records = Set("Record", reverse="to_account_id")


class Budget(db.Entity):
    _table_ = ("finance", "budgets")

    id = PrimaryKey(int, auto=True)
    home_id = Required(int)
    name = Required(str)
    created_at = Optional(int)

    # foreign references
    record_sources = Set("RecordSource")
    accounts = Set("Account")
    records = Set("Record")


class RecordSource(db.Entity):
    _table_ = ("finance", "record_source")

    id = PrimaryKey(int, auto=True)
    budget_id = Required("Budget")  # maps to budget
    source_key = Required(str)
    source_type = Required(str)
    record_count = Required(int)
    created_at = Optional(int)

    # foreign references
    records = Set("Record")


class Record(db.Entity):
    _table_ = ("finance", "records")

    id = PrimaryKey(int, auto=True)
    hash = Required(str)
    budget_id = Required("Budget")  # maps to budget
    from_account_id = Optional("Account")  # maps to account
    to_account_id = Optional("Account")  # maps to account
    amount = Required(int)  # dollar value in cents
    description = Required(str)
    transaction_time = Required(int)
    record_source_id = Required("RecordSource")  # maps to RecordSource
    created_at = Optional(int)


db.bind(provider="postgres", host=os.environ["DB_HOST"], database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"], port=os.environ["DB_PORT"], application_name="piper-budget")

if os.environ.get("DEBUG", "false") == "true":
    set_sql_debug(True)

db.generate_mapping(check_tables=True, create_tables=False)
