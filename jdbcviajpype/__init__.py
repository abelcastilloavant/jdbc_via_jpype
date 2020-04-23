from jdbcviajpype.java_conn import (
    initialize_jvm,
    java_connection,
)

from jdbcviajpype.converters import get_converters
from jdbcviajpype.dbapi import Connection


def _listify(obj):
    if obj:
        if isinstance(obj, str):
            return [obj]
        else:
            return obj
    else:
        return []


def connect(*, jclassname, url, driver_args=None, jars=None, libs=None):
    """Open a connection to a database using a JDBC driver and return
    a Connection instance.
    jclassname: Full qualified Java class name of the JDBC driver.
    url: Database url as required by the JDBC driver.
    driver_args: Dictionary or sequence of arguments to be passed to
           the Java DriverManager.getConnection method. Usually
           sequence of username and password for the db. Alternatively
           a dictionary of connection arguments (where `user` and
           `password` would probably be included). See
           http://docs.oracle.com/javase/7/docs/api/java/sql/DriverManager.html
           for more details
    jars: Jar filename or sequence of filenames for the JDBC driver
    libs: Dll/so filenames or sequence of dlls/sos used as shared
          library by the JDBC driver
    """
    driver_args = _listify(driver_args)
    jars = _listify(jars)
    libs = _listify(libs)
    initialize_jvm(jars, libs)
    java_conn = java_connection(jclassname, url, driver_args)
    return Connection(java_conn, get_converters())
