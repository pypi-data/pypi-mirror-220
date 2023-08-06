
import json
import os,sys

r=os.path.abspath(os.path.dirname(__file__))
rootpath=os.path.split(r)[0]
sys.path.append(rootpath)
from hil_general_test.case_help.case_getMappingFile import download_caseFile
from hil_general_test.case_help.case_configParser import Case_config

download_caseFile(rootpath + r"/case_jsons")
_case_jsonPath = rootpath + fr"/case_jsons/{Case_config.get_case_file()}"
with open(_case_jsonPath, 'r',encoding='utf-8') as jsonf:
    _case_json = json.load(jsonf)


class Case_json():

    @staticmethod
    def get_test_suite_name():
        test_suite_name = _case_json["test_suite_name"]
        return test_suite_name

    @staticmethod
    def get_EM_project():
        EM_project = _case_json["EM_project"]
        return EM_project

    @staticmethod
    def get_env_names():
        env_names = _case_json["env_names"]
        return env_names

    @staticmethod
    def get_cases():
        cases = _case_json["cases"]
        return cases

    @staticmethod
    def get_suit():
        test_suite_name = _case_json["test_suite_name"]
        return test_suite_name



