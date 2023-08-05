# copyright 2003-2011 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of logilab-database.
#
# logilab-database is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# logilab-database is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with logilab-database. If not, see <http://www.gnu.org/licenses/>.
"""
unit tests for module logilab.common.db
"""

import socket
import unittest

from logilab.common.shellutils import getlogin
from logilab.database import (
    set_prefered_driver,
    UnknownDriver,
    get_connection,
    PyConnection,
    PyCursor,
    get_dbapi_compliant_module,
    get_db_helper,
    FunctionDescr,
    register_function,
    UnsupportedFunction,
)
from logilab.database import _PREFERED_DRIVERS as PREFERED_DRIVERS
from logilab.database.postgres import _PGAdvFuncHelper
from logilab.database.sqlite import _SqliteAdvFuncHelper


class PreferedDriverTC(unittest.TestCase):
    def setUp(self):
        self.drivers = {"pg": [("foo", None), ("bar", None)]}
        self.drivers = {"pg": ["foo", "bar"]}
        self.old_drivers = PREFERED_DRIVERS["postgres"][:]

    def tearDown(self):
        """Reset PREFERED_DRIVERS as it was"""
        PREFERED_DRIVERS["postgres"] = self.old_drivers

    def testNormal(self):
        set_prefered_driver("pg", "bar", self.drivers)
        self.assertEqual("bar", self.drivers["pg"][0])

    def testFailuresDb(self):
        with self.assertRaises(UnknownDriver) as cm:
            set_prefered_driver("oracle", "bar", self.drivers)
        self.assertEqual(str(cm.exception), "Unknown driver oracle")

    def testFailuresDriver(self):
        with self.assertRaises(UnknownDriver) as cm:
            set_prefered_driver("pg", "baz", self.drivers)
        self.assertEqual(str(cm.exception), "Unknown module baz for pg")

    def testGlobalVar(self):
        # XXX: Is this test supposed to be useful ? Is it supposed to test
        #      set_prefered_driver ?
        old_drivers = PREFERED_DRIVERS["postgres"][:]
        expected = old_drivers[:]
        expected.insert(0, expected.pop(expected.index("psycopg2ct")))
        set_prefered_driver("postgres", "psycopg2ct")
        self.assertEqual(PREFERED_DRIVERS["postgres"], expected)
        set_prefered_driver("postgres", "psycopg2")
        # self.assertEqual(PREFERED_DRIVERS['postgres'], old_drivers)
        expected.insert(0, expected.pop(expected.index("psycopg2")))
        self.assertEqual(PREFERED_DRIVERS["postgres"], expected)


class GetCnxTC(unittest.TestCase):
    def setUp(self):
        self.host = "localhost"
        try:
            socket.gethostbyname(self.host)
        except Exception:
            self.skipTest("those tests require specific DB configuration")
        self.db = "template1"
        self.user = getlogin()
        self.passwd = getlogin()
        self.old_drivers = PREFERED_DRIVERS["postgres"][:]

    def tearDown(self):
        """Reset PREFERED_DRIVERS as it was"""
        PREFERED_DRIVERS["postgres"] = self.old_drivers

    def test_connection_wrap(self):
        """Tests the connection wrapping"""
        try:
            import psycopg2
        except ImportError:
            self.skipTest("psycopg2 module not installed")
        try:
            cnx = get_connection(
                "postgres", self.host, self.db, self.user, self.passwd, quiet=1
            )
        except psycopg2.OperationalError:
            self.skipTest("pgsql test requires a specific configuration")
        self.assertNotIsInstance(
            cnx, PyConnection, "cnx should *not* be a PyConnection instance"
        )
        cnx = get_connection(
            "postgres", self.host, self.db, self.user, self.passwd, quiet=1, pywrap=True
        )
        self.assertIsInstance(
            cnx, PyConnection, "cnx should be a PyConnection instance"
        )

    def test_cursor_wrap(self):
        """Tests cursor wrapping"""
        try:
            import psycopg2
        except ImportError:
            self.skipTest("psycopg2 module not installed")
        try:
            cnx = get_connection(
                "postgres",
                self.host,
                self.db,
                self.user,
                self.passwd,
                quiet=1,
                pywrap=True,
            )
        except psycopg2.OperationalError:
            self.skipTest("pgsql test requires a specific configuration")
        cursor = cnx.cursor()
        self.assertIsInstance(cursor, PyCursor, "cnx should be a PyCursor instance")


class DBAPIAdaptersTC(unittest.TestCase):
    """Tests DbApi adapters management"""

    def setUp(self):
        """Memorize original PREFERED_DRIVERS"""
        self.old_drivers = PREFERED_DRIVERS["postgres"][:]

    def tearDown(self):
        """Reset PREFERED_DRIVERS as it was"""
        PREFERED_DRIVERS["postgres"] = self.old_drivers

    def test_raise(self):
        self.assertRaises(UnknownDriver, get_dbapi_compliant_module, "pougloup")

    def test_adv_func_helper(self):
        try:
            helper = get_db_helper("postgres")
        except ImportError:
            self.skipTest("postgresql dbapi module not installed")
        self.assertIsInstance(helper, _PGAdvFuncHelper)
        try:
            helper = get_db_helper("sqlite")
        except ImportError:
            self.skipTest("sqlite dbapi module not installed")
        self.assertIsInstance(helper, _SqliteAdvFuncHelper)

    def test_register_funcdef(self):
        class MYFUNC(FunctionDescr):
            supported_backends = ("postgres",)
            name_mapping = {
                "postgres": "MYFUNC",
                "sqlite": "SQLITE_MYFUNC",
            }

        register_function(MYFUNC)

        pghelper = get_db_helper("postgres")
        slhelper = get_db_helper("sqlite")
        self.assertRaises(UnsupportedFunction, slhelper.function_description, "MYFUNC")
        try:
            pghelper.function_description("MYFUNC")
        except UnsupportedFunction:
            self.fail('MYFUNC should support "postgres"')

    def test_funcname_with_different_backend_names(self):
        class MYFUNC(FunctionDescr):
            supported_backends = ("postgres", "sqlite")
            name_mapping = {
                "postgres": "MYFUNC",
                "sqlite": "SQLITE_MYFUNC",
            }

        register_function(MYFUNC)

        pghelper = get_db_helper("postgres")
        slhelper = get_db_helper("sqlite")
        self.assertEqual(slhelper.func_as_sql("MYFUNC", ()), "SQLITE_MYFUNC()")
        self.assertEqual(pghelper.func_as_sql("MYFUNC", ("foo",)), "MYFUNC(foo)")


class BaseSqlServer(unittest.TestCase):
    def tearDown(self):
        cursor = self.cnx.cursor()
        cursor.execute("drop table TestBlob")
        cursor.execute("drop table TestLargeString")
        self.cnx.commit()
        cursor.close()
        self.cnx.close()

    def blob(self):
        cursor = self.cnx.cursor()
        data_length = range(400 * 1024 - 10, 400 * 1024 + 10)
        for length in data_length:
            data = memoryview("\x00" * length)
            print("inserting string of length", len(data))
            cursor.execute(
                "insert into TestBlob(id, data) VALUES(%(id)s, %(data)s)",
                {"id": length, "data": data},
            )
            self.cnx.commit()
        cursor.execute("select count(*) from TestBlob")
        print("%d rows in table" % (cursor.fetchone()[0]))
        cursor.close()

    def large_string(self):
        cursor = self.cnx.cursor()
        data_length = range(400 * 1024 - 10, 400 * 1024 + 10)
        for length in data_length:
            data = "1" * length
            print("inserting string of length", len(data))
            cursor.execute(
                "insert into TestLargeString(id, data) VALUES(%(id)s, %(data)s)",
                {"id": length, "data": data},
            )
            self.cnx.commit()
        cursor.execute("select count(*) from TestLargeString")
        print("%d rows in table" % (cursor.fetchone()[0]))
        cursor.close()

    def varbinary_none(self):
        cursor = self.cnx.cursor()
        cursor.execute("insert into TestBlob (id) values (42)")
        self.cnx.commit()
        cursor.execute("select * from TestBlob where id=42")
        print(cursor.fetchall())
        cursor.execute("update TestBlob set id=43, data=NULL where id=42")
        self.cnx.commit()
        cursor.execute("select * from TestBlob where id=43")
        print(cursor.fetchall())
        cursor.execute(
            "update TestBlob set id = %(id)s, data=%(data)s where id=%(old_id)s",
            {"data": None, "id": 42, "old_id": 43},
        )
        self.cnx.commit()
        cursor.execute("select * from TestBlob where id=42")
        print(cursor.fetchall())
        cursor.close()


class PostgresqlDatabaseSchemaTC(unittest.TestCase):
    host = "localhost"
    database = "template1"
    user = password = getlogin()
    schema = "tests"

    def setUp(self):
        try:
            self.module = get_dbapi_compliant_module("postgres")
        except ImportError:
            self.skipTest("postgresql dbapi module not installed")
        try:
            cnx = self.get_connection()
        except Exception:
            self.skipTest(
                "could not connect to %s:%s@%s/%s"
                % (self.user, self.password, self.host, self.database)
            )
        self._execute(cnx, "CREATE SCHEMA %s" % self.schema)
        cnx.close()

    def tearDown(self):
        cnx = self.get_connection()
        self._execute(cnx, "DROP SCHEMA %s" % self.schema)
        cnx.close()

    def _execute(self, cnx, sql):
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
        cnx.close()

    def get_connection(self, schema=None):
        return self.module.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            schema=schema,
        )

    def assertRsetEqual(self, rset, expected_rset):
        # NOTE: different drivers will use different result structures
        #       (list of lists, list of tuples, etc.)
        self.assertEqual(len(rset), len(expected_rset))
        for line, expected_line in zip(rset, expected_rset):
            self.assertSequenceEqual(line, expected_line)

    def test_database_schema(self):
        """Tests database schema support"""
        cnx = self.get_connection(schema=self.schema)
        cursor = cnx.cursor()
        try:
            cursor.execute("CREATE TABLE x(x integer)")
            cursor.execute("INSERT INTO x VALUES(12)")
            cursor.execute("SELECT x from x")
            self.assertRsetEqual(cursor.fetchall(), [[12]])
            cursor.execute("SELECT x from tests.x")
            self.assertRsetEqual(cursor.fetchall(), [[12]])
            self.assertRaises(
                self.module.Error, cursor.execute, "SELECT x from public.x"
            )
        finally:
            cnx.rollback()
            cnx.close()

    def test_list_tables(self):
        helper = get_db_helper("postgres")
        cnx = self.get_connection(schema=self.schema)
        cursor = cnx.cursor()
        try:
            cursor.execute("CREATE TABLE x(x integer)")
            self.assertNotIn("x", helper.list_tables(cursor))
            self.assertIn("x", helper.list_tables(cursor, schema=self.schema))
        finally:
            cnx.close()

    def test_list_indices(self):
        helper = get_db_helper("postgres")
        cnx = self.get_connection(schema=self.schema)
        cursor = cnx.cursor()
        try:
            cursor.execute("CREATE TABLE x(x integer)")
            cursor.execute("CREATE INDEX x_idx ON x(x)")
            self.assertIn("x_idx", helper.list_indices(cursor))
            self.assertIn("x_idx", helper.list_indices(cursor, table="x"))
        finally:
            cnx.close()


if __name__ == "__main__":
    unittest.main()
