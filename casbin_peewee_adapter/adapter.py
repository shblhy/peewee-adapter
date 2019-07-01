import casbin
import peewee as pw
from functools import reduce


class Adapter(casbin.persist.Adapter):
    def __init__(self, database=None):
        self.database = database
        proxy = pw.Proxy()
        CasbinRule._meta.database = proxy
        proxy.initialize(database)

    def load_policy(self, model):
        for line in CasbinRule.select():
            casbin.persist.load_policy_line(str(line), model)

    def _save_policy_line(self, ptype, rule):
        data = dict(zip(['v0', 'v1', 'v2', 'v3', 'v4', 'v5'], rule))
        item = CasbinRule(ptype=ptype)
        item.__data__.update(data)
        item.save()

    def save_policy(self, model):
        """saves all policy rules to the storage."""
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)
        return True

    def add_policy(self, sec, ptype, rule):
        """adds a policy rule to the storage."""
        self._save_policy_line(ptype, rule)

    def remove_policy(self, sec, ptype, rule):
        """removes a policy rule from the storage."""
        if sec in ["p", "g"]:
            condition = [CasbinRule.ptype==ptype]
            data = dict(zip(['v0', 'v1', 'v2', 'v3', 'v4', 'v5'], rule))
            condition.extend([getattr(CasbinRule, k) == data[k] for k in data])
            check = CasbinRule.select().filter(*condition)
            if check.exists():
                CasbinRule.delete().where(*condition).execute()
                return True
            else:
                return False
        else:
            return False

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes policy rules that match the filter from the storage.
        This is part of the Auto-Save feature.
        """
        pass

class CasbinRule(pw.Model):
    class Meta:
        table_name = 'casbin_rule'
    ptype = pw.CharField(max_length=255, null=True)
    v0 = pw.CharField(max_length=255, null=True)
    v1 = pw.CharField(max_length=255, null=True)
    v2 = pw.CharField(max_length=255, null=True)
    v3 = pw.CharField(max_length=255, null=True)
    v4 = pw.CharField(max_length=255, null=True)
    v5 = pw.CharField(max_length=255, null=True)


    def __str__(self):
        return reduce(lambda x, y: str(x) + ', ' + str(y) if y else x,
                      [self.ptype, self.v0, self.v1, self.v2, self.v3, self.v4, self.v5])

    def __repr__(self):
        if not self.id:
            return "<{cls}: {desc}>".format(cls=self.__class__.__name__, desc=self)
        return "<{cls} {pk}: {desc}>".format(cls=self.__class__.__name__, pk=self.id, desc=self)