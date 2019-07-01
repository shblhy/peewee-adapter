from unittest import TestCase
import peewee
import casbin
import os
import simpleeval
from casbin_peewee_adapter import Adapter, CasbinRule
LOG_ENABLED = True
DATABAEE = peewee.SqliteDatabase('test.db')
CASBIN_ADAPTER = Adapter(database=DATABAEE)
# from casbin_peewee_adapter.config import DEFAULT_MYSQL_DATABAEE
# CASBIN_ADAPTER = Adapter(database=DEFAULT_MYSQL_DATABAEE)


def table_init():
    CasbinRule.create_table()

def data_init():
    CasbinRule(ptype='p', v0='alice', v1='data1', v2='read').save()
    CasbinRule(ptype='p', v0='bob', v1='data2', v2='write').save()
    CasbinRule(ptype='p', v0='data2_admin', v1='data2', v2='read').save()
    CasbinRule(ptype='p', v0='data2_admin', v1='data2', v2='write').save()
    CasbinRule(ptype='g', v0='alice', v1='data2_admin').save()


def get_fixture(path):
    dir_path = os.path.split(os.path.realpath(__file__))[0] + "/"
    return os.path.abspath(dir_path + path)


def get_enforcer():
    return casbin.Enforcer(get_fixture('rbac_model.conf'), CASBIN_ADAPTER, LOG_ENABLED)


class TestConfig(TestCase):
    def setUp(self):
        table_init()

    def tearDown(self):
        CasbinRule.delete().execute()

    def test_enforcer_basic(self):
        data_init()
        e = get_enforcer()
        self.assertTrue(e.enforce('alice', 'data1', 'read'))
        self.assertFalse(e.enforce('bob', 'data1', 'read'))
        self.assertTrue(e.enforce('bob', 'data2', 'write'))
        self.assertTrue(e.enforce('alice', 'data2', 'read'))
        self.assertTrue(e.enforce('alice', 'data2', 'write'))

    def test_add_policy(self):
        adapter = CASBIN_ADAPTER
        e = get_enforcer()
        try:
            self.assertFalse(e.enforce('alice', 'data1', 'read'))
            self.assertFalse(e.enforce('bob', 'data1', 'read'))
            self.assertFalse(e.enforce('bob', 'data2', 'write'))
            self.assertFalse(e.enforce('alice', 'data2', 'read'))
            self.assertFalse(e.enforce('alice', 'data2', 'write'))
        except simpleeval.NameNotDefined:
            # This is caused by an upstream bug when there is no policy loaded
            # Should be resolved in pycasbin >= 0.3
            pass
        adapter.add_policy(sec=None, ptype='p', rule=['alice', 'data1', 'read'])
        adapter.add_policy(sec=None, ptype='p', rule=['bob', 'data2', 'write'])
        adapter.add_policy(sec=None, ptype='p', rule=['data2_admin', 'data2', 'read'])
        adapter.add_policy(sec=None, ptype='p', rule=['data2_admin', 'data2', 'write'])
        adapter.add_policy(sec=None, ptype='g', rule=['alice', 'data2_admin'])

        e.load_policy()

        self.assertTrue(e.enforce('alice', 'data1', 'read'))
        self.assertFalse(e.enforce('bob', 'data1', 'read'))
        self.assertTrue(e.enforce('bob', 'data2', 'write'))
        self.assertTrue(e.enforce('alice', 'data2', 'read'))
        self.assertTrue(e.enforce('alice', 'data2', 'write'))
        self.assertFalse(e.enforce('bogus', 'data2', 'write'))

    def test_save_policy(self):
        model = casbin.Enforcer(get_fixture('rbac_model.conf'), get_fixture('rbac_policy.csv')).model
        adapter = CASBIN_ADAPTER
        adapter.save_policy(model)
        e = casbin.Enforcer(get_fixture('rbac_model.conf'), adapter)

        self.assertTrue(e.enforce('alice', 'data1', 'read'))
        self.assertFalse(e.enforce('bob', 'data1', 'read'))
        self.assertTrue(e.enforce('bob', 'data2', 'write'))
        self.assertTrue(e.enforce('alice', 'data2', 'read'))
        self.assertTrue(e.enforce('alice', 'data2', 'write'))

    def test_str(self):
        rule = CasbinRule(ptype='p', v0='alice', v1='data1', v2='read')
        self.assertEqual(str(rule), 'p, alice, data1, read')

    def test_repr(self):
        rule = CasbinRule(ptype='p', v0='alice', v1='data1', v2='read')
        print(repr(rule))
        self.assertEqual(repr(rule), '<CasbinRule: p, alice, data1, read>')
        rule.save()
        print(rule.id)
        print(repr(rule))
        self.assertRegex(repr(rule), r'<CasbinRule \d+: p, alice, data1, read>')