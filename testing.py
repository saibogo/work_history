import unittest

from wh_app.supporting import functions
from wh_app.supporting.utests.test_functions import MyTestCaseFunctions

functions.info_string(__name__)


def start_all_test() -> None:
    unittest.main(MyTestCaseFunctions())


start_all_test()