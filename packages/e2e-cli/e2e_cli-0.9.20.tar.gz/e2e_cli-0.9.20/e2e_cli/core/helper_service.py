import json
import traceback
import warnings

from e2e_cli.logs.logs_service import save_to_logs

warnings.simplefilter(action='ignore', category=FutureWarning)

EMPTY_DATA = "Your requested data seems to be empty"


class StatusChecks:

    @classmethod
    def status_error_check(cls, status):
        try:
            if (status['errors']):
                print("errors : ", status['errors'])
                return False
            else:
                return True
        except Exception:
            return False

    @classmethod
    def status_msg_check(cls, status):
        print("message : ", status['message'])

    @classmethod
    def status_data_check(cls, status, request_method):
        EMPTY_DATA_ALLOWED = ["DELETE"]

        if (status['data']):
            return True
        else:
            if request_method in EMPTY_DATA_ALLOWED:
                return True
            print(EMPTY_DATA)
            return False

    # def status_code_check(status, error_result):
    #         a= str(status['code'])
    #         msg= status['message'].lower()
    #         if(error_result==True):
    #             if( a[0]=="2" and len(a)==3):
    #             pass
    #             elif( a[0]=="5" and len(a)==3):
    #                 if("success" in msg) and ("unsuccess" not in msg):
    #                     print("issue with response in no error status code -> ", status['code'])
    #                 elif("server" in msg)or ("error" in msg) or ("wrong" in msg) or ("issue" in msg) or ("failed" in msg):
    #                     pass
    #             else:
    #                 print("issue with response in no error status code -> ", status['code'])
    #         elif(error_result==False):
    #             if( a[0]=="2" and len(a)==3):
    #                 print("issue with response in errors status code -> ", status['code'])


class Checks:

    @classmethod
    def is_int(self, id):
        try:
            int(id)
            return True
        except:
            return False

    @classmethod
    def status_result(self, status, request_method=""):
        StatusChecks.status_msg_check(status)
        error_result = StatusChecks.status_error_check(status)
        return error_result

    @classmethod
    def manage_exception(self, e, arguments, trace):
        print(e)
        traceback.print_exc()
        save_to_logs(arguments, trace)

    @classmethod
    def show_json(self, status, e=None):
        if (e is not None):
            print("Errors while reading json ", e)
        print(json.dumps(status, sort_keys=True, indent=4))
        return status

    @classmethod
    def take_input(self, inputs, value):
        if value in inputs:
            return inputs[value]
        else:
            return input("Please enter " + value + " : ")


class ApiFilter:
    def __init__(self, inputs, required, optional):
        if ("info" in inputs):
            self.api_inputs_info(required, optional)
        else:
            self.inputs_and_required_check(inputs, required)
            self.inputs_and_optional_check(inputs, optional)

    def inputs_and_required_check(self, inputs, required):
        """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
        for arg_input in required:
            type_check = required[arg_input]
            value = inputs.get(arg_input)
            if (not value):
                value = inputs[arg_input] = input(
                    f"Please enter {arg_input} : ")
            try:
                if (type_check):
                    inputs[arg_input] = type_check(value)
            except Exception as e:
                import sys
                sys.exit(f"TypeError/ValueError for {arg_input} : {e}")

    def inputs_and_optional_check(self, inputs, optional):
        """Note here type_check variable is used to check data type like int, bool and validity of the input given ex-bucket_name"""
        for arg_input in optional:
            type_check = optional[arg_input]
            value = inputs.get(arg_input)
            if (value):
                try:
                    if (type_check):
                        inputs[arg_input] = type_check(value)
                except Exception as e:
                    inputs[arg_input] = input(
                        f"Please enter valid {arg_input} : ")

    def api_inputs_info(self, required, optional):
        print("required inputs :")
        print(*required.keys(), sep="\n")
        print()
        print("optional inputs :")
        print(*optional.keys(), sep="\n")
