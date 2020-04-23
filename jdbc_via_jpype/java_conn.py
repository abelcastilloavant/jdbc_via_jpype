import os
import sys
import jpype
from jdbc.errors import (
    DatabaseError,
    InterfaceError,
)


def _reraise(tp, value, tb=None):
    if value is None:
        value = tp()
    else:
        value = tp(value)
    if tb:
        raise value.with_traceback(tb)
    raise value


def initialize_jvm(jars, libs):
    if jpype.isJVMStarted():
        return
    else:
        args = []
        class_path = []
        if jars:
            class_path.extend(jars)
        if class_path:
            args.append("-Djava.class.path=%s" % os.path.pathsep.join(class_path))
        if libs:
            # path to shared libraries
            libs_path = os.path.pathsep.join(libs)
            args.append("-Djava.library.path=%s" % libs_path)
        jvm_path = jpype.getDefaultJVMPath()
        jpype.startJVM(jvm_path, *args)
    if not jpype.isThreadAttachedToJVM():
        jpype.attachThreadToJVM()


def java_connection(jclassname, url, driver_args):
    if isinstance(driver_args, dict):
        Properties = jpype.java.util.Properties
        info = Properties()
        for k, v in driver_args.items():
            info.setProperty(k, v)
        dargs = [info]
    else:
        dargs = driver_args
    return jpype.java.sql.DriverManager.getConnection(url, *dargs)


def get_types_map():
    if not jpype.isJVMStarted():
        raise ValueError("can't get types map if JVM hasn't started!")
    return {
        i.getName(): i.getStaticAttribute()
        for i in jpype.java.sql.Types.__javaclass__.getClassFields()
    }


def _handle_sql_exception():
    SQLException = jpype.java.sql.SQLException
    exc_info = sys.exc_info()
    if issubclass(exc_info[1].__javaclass__, SQLException):
        exc_type = DatabaseError
    else:
        exc_type = InterfaceError
    _reraise(exc_type, exc_info[1], exc_info[2])
