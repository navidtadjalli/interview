import os

from django.test import TestCase
from achare_interview.constants import EnvVarKeys


class EnvVarsTestCase(TestCase):
    def test_if_env_vars_loaded(self):
        for env_var_key in filter(lambda m: False if m.startswith('__') else True, dir(EnvVarKeys)):
            self.assertIsNotNone(os.environ.get(getattr(EnvVarKeys, env_var_key), None))
