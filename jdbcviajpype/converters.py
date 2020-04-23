from jdbcviajpype.java_conn import get_types_map
from datetime import datetime


def _to_datetime(rs, col):
    java_val = rs.getTimestamp(col)
    if not java_val:
        return
    d = datetime.strptime(str(java_val)[:19], "%Y-%m-%d %H:%M:%S")
    d = d.replace(microsecond=int(str(java_val.getNanos())[:6]))
    return str(d)


def _to_time(rs, col):
    java_val = rs.getTime(col)
    if not java_val:
        return
    return str(java_val)


def _to_date(rs, col):
    java_val = rs.getDate(col)
    if not java_val:
        return
    d = datetime.datetime.strptime(str(java_val)[:10], "%Y-%m-%d")
    return d.strftime("%Y-%m-%d")


def _to_binary(rs, col):
    java_val = rs.getObject(col)
    if java_val is None:
        return
    return str(java_val)


def _java_to_py(rs, col, java_method):
    java_val = rs.getObject(col)
    if java_val is None:
        return
    elif isinstance(java_val, (str, int, float, bool)):
        return java_val
    return getattr(java_val, java_method)()


def _to_double(rs, col):
    return _java_to_py(rs, col, "doubleValue")


def _to_int(rs, col):
    return _java_to_py(rs, col, "intValue")


def _to_boolean(rs, col):
    return _java_to_py(rs, col, "booleanValue")


_DEFAULT_CONVERTERS = {
    # see
    # http://download.oracle.com/javase/8/docs/api/java/sql/Types.html
    # for possible keys
    "TIMESTAMP": _to_datetime,
    "TIME": _to_time,
    "DATE": _to_date,
    "BINARY": _to_binary,
    "DECIMAL": _to_double,
    "NUMERIC": _to_double,
    "DOUBLE": _to_double,
    "FLOAT": _to_double,
    "TINYINT": _to_int,
    "INTEGER": _to_int,
    "SMALLINT": _to_int,
    "BOOLEAN": _to_boolean,
    "BIT": _to_boolean,
}


def get_converters():
    types_map = get_types_map()
    converters = {types_map[i]: _DEFAULT_CONVERTERS[i] for i in _DEFAULT_CONVERTERS}
    return converters
