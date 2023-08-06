# -*- coding: utf-8 -*-

from hil_general_test.case_help.case_execute_prepare import *
from hil_general_test.case_help.case_step import Case_step
import pytest
import allure

@allure.suite(suite_name)
@pytest.mark.parametrize("caseInfo", cases, ids=caseName)
def test_(caseInfo,manage_env):
    case_log.info(msg=hil_generalTest.benchInfo)
    cases = caseInfo
    cn = list(cases.keys())[0]
    case_start_msg = f"\n\tCASE STATUS: '{cn}' Start Test!"
    case_log.info(msg=case_start_msg)
    for steps in cases.values():
        resultValue = []
        for step_d in steps:
            for stepid, step in step_d.items():
                step_start_msg = f"\n\t>>  CASE STEP STATUS: step {stepid} Start Test!"
                case_log.info(msg=step_start_msg)
                kword = step[0]
                envName = step[1]
                stepData, expect, re = Case_step().execute\
                    (kword,step,stepid,envName,exs,case_log,resultValue,cn)
                if re == "continue":
                    continue
                resultValue.append(re)
                expect_id = 0
                for ex in expect:
                    expectValue, Left_right_assertion = exs.expect_parse\
                        (ex, cn, stepid, resultValue, expect_id)
                    exs.assertion_log(expectValue, Left_right_assertion, cn, stepid, expect_id, kword, stepData)
                    expect_id += 1
                    assert expectValue[0]
                    assert Left_right_assertion[0]
                step_end_msg = f"\n\t>>  CASE STEP STATUS: step {stepid} End Test!"
                case_log.info(msg=step_end_msg)
    case_end_msg = f"\n\t>>  CASE STATUS: '{cn}' End Test!"
    case_log.info(msg=case_end_msg)
