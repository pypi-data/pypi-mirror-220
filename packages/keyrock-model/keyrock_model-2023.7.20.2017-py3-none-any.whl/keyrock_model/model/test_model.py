import unittest
import math
import json

from pydantic import parse_obj_as

from . import *

import logging
logger = logging.getLogger(__name__)


class ExampleModel(KrBaseModel):
    pub_var: float = 1.0
    _pri_var: float = 2.0

    def __post_init__(self):
        pass

class TestExampleModel(unittest.TestCase):
    def test_example_model(self):
        test_obj = ExampleModel()
        logger.debug(json.dumps(test_obj.dict(), indent=2))

        self.assertEqual(1, 1)
