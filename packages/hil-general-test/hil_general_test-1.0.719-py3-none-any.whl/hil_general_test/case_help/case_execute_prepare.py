# -*- coding: utf-8 -*-

from hil_general_test.case_help.case_data_prepare import *
from hil_general_test.case_help.case_configParser import Case_config


hil_generalTest = Case_dataPrepare()
mytest = hil_generalTest.mytests
full_cases = hil_generalTest.case_analyse()

# get final cases
start_case, end_case = Case_config.get_caseIndex()
cases = full_cases[start_case:end_case]
hil_generalTest.check_caseIndex(full_cases, start_case, end_case)

# get case name
suite_name = hil_generalTest.test_suite_name
caseName = []
caseId = start_case
for c in cases:
    caseName.append(str(caseId) + '_' + list(c.keys())[0])
    caseId += 1
exs = Case_Step(mytest)