# -*- coding: utf-8 -*-
import re
from .util import strtobool
from pyparsing import (
    Word,
    nums,
    alphanums,
    Combine,
    Regex,
    CaselessKeyword,
    Opt,
    one_of,
    Group,
    Suppress,
    pyparsing_common as ppc,
)


class DataTypes:
    STRING = "STRING"
    DATE = "DATE"
    DATETIME = "DATETIME"
    NUMBER = "NUMBER"
    BOOL = "BOOL"
    NULL = "NULL"


class DdbDataTypes:
    BOOLEAN = "BOOL"
    BINARY = "B"
    LIST = "L"
    MAP = "M"
    NUMBER = "N"
    NUMBER_SET = "NS"
    STRING_SET = "SS"
    STRING = "STRING"
    NULL = "NULL"


class Functions:
    DATE = "DATE"
    DATETIME = "DATETIME"
    NUMBER = "NUMBER"
    BOOL = "BOOL"

    TYPE_CONVERSION = [DATE, DATETIME, NUMBER, BOOL]
    WHERE_CONDITION = ["begins_with", "attribute_type", "contains"]
    WHERE_CONDITION_WITH_OP = ["size"]


class KeyWords:
    # Common sign definition
    (
        LPAR,
        RPAR,
        COMMA,
        SEMICOLON,
        COLON,
        DOT,
        SINGLEQUOTE,
        DOUBLEQUOTE,
        BACKQUOTE,
        EQUALS,
        SPACE,
    ) = map(Suppress, "(),;:.'\"`= ")
    STAR, QUESTION = "*", "?"
    SUPPRESS_QUOTE = (SINGLEQUOTE | BACKQUOTE | DOUBLEQUOTE).set_name("suppress_quote")
    QUOTE = one_of("' \" `").set_name("quote")

    # Operators
    (
        ADD,
        SUBTRACT,
        EQUAL_TO,
        NOT_EQUAL_TO,
        GREATER,
        LESS,
        GREATER_OR_EQUAL,
        LESS_OR_EQUAL,
        AND,
        BETWEEN,
        IN,
        IS,
        NOT,
        OR,
    ) = map(
        CaselessKeyword,
        [
            "+",
            "-",
            "=",
            "<>",
            ">",
            "<",
            ">=",
            "<=",
            "AND",
            "BETWEEN",
            "IN",
            "IS",
            "NOT",
            "OR",
        ],
    )
    ARITHMETIC_OPERATORS = one_of("+ -")("arithmetic_operators").set_name(
        "arithmetic_operators"
    )
    COMPARISON_OPERATORS = one_of("= <> < > >= <=")("comparison_operators").set_name(
        "comparison_operators"
    )

    # Common key word definition
    (
        CREATE,
        ALTER,
        DROP,
        TABLE,
        SELECT,
        FROM,
        WHERE,
        INSERT,
        GLOBAL,
        PARTITION_KEY,
        SORT_KEY,
        HASH,
        RANGE,
        UPDATE,
        DELETE,
        INDEX,
        REPLICA,
        ORDER_BY,
        LIMIT,
        AS,
    ) = map(
        CaselessKeyword,
        [
            "CREATE",
            "ALTER",
            "DROP",
            "TABLE",
            "SELECT",
            "FROM",
            "WHERE",
            "INSERT",
            "GLOBAL",
            "PARTITION KEY",
            "SORT KEY",
            "HASH",
            "RANGE",
            "UPDATE",
            "DELETE",
            "INDEX",
            "REPLICA",
            "ORDER BY",
            "Limit",
            "AS",
        ],
    )

    (
        LIST,
        SHOW,
        DESC,
        DESCRIBE,
        TABLES,
    ) = map(
        CaselessKeyword,
        [
            "LIST",
            "SHOW",
            "DESC",
            "DESCRIBE",
            "TABLES",
        ],
    )

    # Functions supported on Column
    FUNCTION_ON_COLUMN = one_of(
        Functions.TYPE_CONVERSION, caseless=True, as_keyword=True
    )("function").set_name("function")

    # Functions supported on Where conditions
    FUNCTION_ON_WHERE = one_of(
        Functions.WHERE_CONDITION, caseless=True, as_keyword=True
    )("function").set_name("function")

    FUNCTION_WITH_OP_ON_WHERE = one_of(
        Functions.WHERE_CONDITION_WITH_OP, caseless=True, as_keyword=True
    )("function_with_op").set_name("function_with_op")


class Tokens:
    # Common token definition
    TABLE_NAME = (
        Opt(KeyWords.SUPPRESS_QUOTE)
        + Word(alphanums + "-_<>")("table").set_name("table")
        + Opt(KeyWords.SUPPRESS_QUOTE)
    )
    ATTRIBUTE_NAME = (
        Opt(KeyWords.SUPPRESS_QUOTE)
        + Word(alphanums + "-_")("attribute_name").set_name("attribute_name")
        + Opt(KeyWords.SUPPRESS_QUOTE)
    )
    DATA_TYPE = one_of("NUMERIC STRING BINARY", caseless=True)("data_type").set_name(
        "data_type"
    )
    OPT_KEY_TYPE = one_of(["PARTITION KEY", "SORT KEY", "HASH", "RANGE", ""])(
        "key_type"
    ).set_name("key_type")
    KEY_TYPE = one_of(["PARTITION KEY", "SORT KEY", "HASH", "RANGE"])(
        "key_type"
    ).set_name("key_type")
    INDEX_NAME = (
        Opt(KeyWords.SUPPRESS_QUOTE)
        + Word(alphanums + "_")("index_name").set_name("index_name")
        + Opt(KeyWords.SUPPRESS_QUOTE)
    )
    INDEX_TYPE = one_of("GLOBAL LOCAL", caseless=True)("index_type").set_name(
        "index_type"
    )
    TAG = Group(
        Opt(KeyWords.SINGLEQUOTE)
        + Word(alphanums + "._$")("tag_key").set_name("tag_key")
        + Opt(KeyWords.SINGLEQUOTE)
        + ":"
        + Opt(KeyWords.SINGLEQUOTE)
        + Word(alphanums + "._$")("tag_value").set_name("tag_value")
        + Opt(KeyWords.SINGLEQUOTE)
    )("tag").set_name("tag")
    REGION_NAME = Word(alphanums + "-")("region_name").set_name("region_name")
    KMSMASTERKEYID = Word(alphanums + "+-=*_$")
    INT_VALUE = Word(nums).set_parse_action(ppc.convert_to_integer)
    BOOL_VALUE = one_of("True False", caseless=True).set_parse_action(
        lambda toks: strtobool(toks[0])
    )
    ORDER_BY_VALUE = one_of("DESC ASC", caseless=True)
    PARTIQL_DATA_TYPE = one_of(
        [
            DdbDataTypes.BOOLEAN,
            DdbDataTypes.BINARY,
            DdbDataTypes.LIST,
            DdbDataTypes.MAP,
            DdbDataTypes.NUMBER,
            DdbDataTypes.NUMBER_SET,
            DdbDataTypes.STRING_SET,
            DdbDataTypes.STRING,
            DdbDataTypes.NULL,
            "MISSING",
        ],
        caseless=True,
    )
    QUOTED_STRING = Combine(
        Suppress('"')
        + Regex(r'(?:[^"\n\r\\]|(?:"")|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*')
        + Suppress('"')
        | Suppress("'")
        + Regex(r"(?:[^'\n\r\\]|(?:'')|(?:\\(?:[^x]|x[0-9a-fA-F]+)))*")
        + Suppress("'")
    )


class QueryType:
    """
    Types of supported queries
    """

    CREATE = ("DDL", "WRITE", "CREATE TABLE")
    CREATE_GLOBAL = ("DDL", "WRITE", "CREATE GLOBAL TABLE")
    ALTER = ("DDL", "WRITE", "ALTER TABLE")
    DROP = ("DDL", "WRITE", "DROP TABLE")
    DROP_GLOBAL = ("DDL", "WRITE", "DROP GLOBAL TABLE")
    INSERT = ("DML", "WRITE", "INSERT")
    UPDATE = ("DML", "WRITE", "UPDATE")
    DELETE = ("DML", "WRITE", "DELETE")
    SELECT = ("DML", "READ", "SELECT")
    LIST = ("UTIL", "READ", "LIST TABLES")
    LIST_GLOBAL = ("UTIL", "READ", "LIST GLOBAL TABLES")
    DESC = ("UTIL", "READ", "DESC")
    DESC_GLOBAL = ("UTIL", "READ", "DESC GLOBAL")


SUPPORTED_QUERY_TYPES = {
    r"^\s*(SELECT).*": QueryType.SELECT,
    r"^\s*(INSERT).*": QueryType.INSERT,
    r"^\s*(UPDATE).*": QueryType.UPDATE,
    r"^\s*(DELETE).*": QueryType.DELETE,
    r"^\s*(CREATE)\s+(TABLE).*": QueryType.CREATE,
    r"^\s*(CREATE)\s+(GLOBAL)\s+(TABLE).*": QueryType.CREATE_GLOBAL,
    r"^\s*(ALTER)\s+(TABLE).*": QueryType.ALTER,
    r"^\s*(DROP)\s+(TABLE).*": QueryType.DROP,
    r"^\s*(DROP)\s+(GLOBAL)\s+(TABLE).*": QueryType.DROP_GLOBAL,
    r"^\s*(LIST|SHOW)\s+(TABLES).*": QueryType.LIST,
    r"^\s*(LIST|SHOW)\s+(GLOBAL)\s+(TABLES).*": QueryType.LIST_GLOBAL,
    r"^\s*(DESC|DESCRIBE)\s+(?!.*GLOBAL)": QueryType.DESC,
    r"^\s*(DESC|DESCRIBE)\s+(GLOBAL).*": QueryType.DESC_GLOBAL,
}


def get_query_type(sql: str) -> QueryType:
    for type_pattern, type in SUPPORTED_QUERY_TYPES.items():
        pattern_ = re.compile(type_pattern, re.IGNORECASE)
        match_ = pattern_.search(sql)

        if match_:
            return type

    raise LookupError("Not supported query type")
