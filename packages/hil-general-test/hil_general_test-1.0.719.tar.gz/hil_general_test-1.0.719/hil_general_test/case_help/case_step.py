

class Case_step():

    def execute(self,kword,step, stepid, envName, exs, case_log, resultValue, cn):
        re = ''
        expect = ''
        stepData = {}
        if kword == "write":
            stepData, expect, re = self.write(step, stepid, envName, exs, case_log, resultValue, cn)
        elif kword == "read":
            stepData, expect, re = self.read(step, envName, exs)
        elif kword == "wait":
            stepData, expect, re =self.wait(step, stepid, resultValue, exs, case_log)
        return stepData, expect, re

    def write(self,step,stepid,envName,exs,case_log,resultValue,cn):
        portTypeId = step[6][0]
        stepData = {"env_name": envName, "port_type": "InputPort", "instances": step[2],
                    "signal_name": step[3], "signal_data_type": step[4]}
        if portTypeId == 0:
            expect = step[9]
            stepData["write_value"] = step[5]
            re = exs.key_word_write(envName, *(step[1:9]))
        elif portTypeId == 3:
            expect = step[7]
            stepData["port_type"] = "Calibration"
            stepData["write_value"] = step[14]
            re = exs.write_cal(envName, *(step[1:5]), *(step[8:]))
        else:
            case_log.warning(
                msg=f"\n\tcase name:{cn}>>  this signal:'{envName}/{step[3]}' does not support write!")
            resultValue.append(None)
            step_end_msg = f"\n\t>>  CASE STEP: step {stepid} End Test!"
            case_log.info(msg=step_end_msg)
            expect = None
            re = "continue"
        return stepData,expect , re

    def read(self,step,envName,exs):
        portTypeId = step[5][0]
        stepData = {"env_name": envName, "port_type": "InputPort", "instances": step[2],
                    "signal_name": step[3]}
        if portTypeId == 3:
            stepData["port_type"] = "Calibration"
            expect = step[6]
            re = exs.read_cal(envName, *(step[1:5]), *(step[7:]))
        else:
            if portTypeId == 2:
                stepData["port_type"] = "Measurement"
            elif portTypeId == 1:
                stepData["port_type"] = "OutputPort"
            expect = step[8]
            re = exs.key_word_read(envName, *(step[1:8]))
        return stepData, expect, re

    def wait(self,step,stepid,resultValue,exs,case_log):
        t = int(step[1])
        exs.key_word_wait(t)
        resultValue.append(None)
        case_log.info(
            msg=f"\n\t>>  CASE KEY WORD: wait\n\t>>  CASE STEP: step{stepid} \n\t>>  WAIT TIME: {t}s")
        step_end_msg = f"\n\t>>  CASE STEP STATUS: step {stepid} End Test!"
        case_log.info(msg=step_end_msg)

        return None , None , "continue"