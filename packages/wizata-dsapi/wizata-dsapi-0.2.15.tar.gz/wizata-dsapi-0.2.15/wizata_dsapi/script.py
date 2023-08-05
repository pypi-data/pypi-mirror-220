import json
import uuid
import dill
import os
import types
from .api_dto import ApiDto
import inspect
from collections import OrderedDict


class ScriptConfig(ApiDto):
    """
    a script config defines execution properties for a specific script.
    usually to define how a pipeline should call your script.

    :ivar function: name of function referencing the script.
    """

    def __init__(self, function=None):
        self.function = function

    def from_json(self, obj):
        if isinstance(obj, str):
            self.function = obj
            return
        else:
            if "function" in obj:
                self.function = obj["function"]

    def to_json(self):
        obj = {
            "function": self.function
        }
        return obj

class Script(ApiDto):
    """
    A piece of python code that can either transform data, generate plot or train Machine Learning Models.

    Scripts once validated can be used from Python or directly inside Wizata App by users.

    :ivar script_id: The UUID of the ML Model.
    :ivar description: Provide an insight-full description of what does your script.
    :ivar status: 'draft', 'valid' or 'invalid' - to validate your script use client validate method.
    :ivar needExactColumnNumbers: False by default, define if the model requires exact columns numbers to be executed.
    :ivar needExactColumnNames: False by default, define if the model requires exact columns names to be executed.
    :ivar canGeneratePlot: Set during validation, inform if the script generate plotly figures from dataframe.
    :ivar canGenerateData: Set during validation, inform if the script transform input dataframe into another one.
    :ivar canGenerateModel: Set during validation, inform if the script trains Machine Learning models from dataframe.
    :ivar inputColumns: list of all columns used to call the script the model.
    :ivar outputColumns: list of all columns generated by the script if it generates data.
    :ivar function: Dill object containing the function code and decorators, please use copy()
    """

    def __init__(self, script_id=None, description=None, function=None,
                 exact_names=False, exact_numbers=False):

        # Id
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id
        self._name = None

        # Properties
        self.description = description
        self.needExactColumnNumbers = exact_numbers
        self.needExactColumnNames = exact_names

        # Validation Properties
        self.canGeneratePlot = False
        self.canGenerateModel = False
        self.canGenerateData = False
        self.status = "draft"
        self.inputColumns = []
        self.outputColumns = []

        # Source code property
        self.source = None

        # Function properties (code)
        self.function = None
        if function is not None:
            self.copy(function)


    @property
    def name(self):
        """
        Name of the function
        :return: name of the function
        """
        return self._name

    def api_id(self) -> str:
        """
        Id of the script (script_id)

        :return: string formatted UUID of the script.
        """
        return str(self.script_id).upper()

    def endpoint(self) -> str:
        """
        Name of the endpoints used to manipulate scripts.
        :return: Endpoint name.
        """
        return "Scripts"

    def to_json(self):
        """
        Convert the script to a dictionary compatible to JSON format.

        :return: dictionary representation of the Script object.
        """
        obj = {
            "id": str(self.script_id),
            "canGeneratePlot": str(self.canGeneratePlot),
            "canGenerateModel": str(self.canGenerateModel),
            "canGenerateData": str(self.canGenerateData),
            "status": str(self.status),
            "needExactColumnNumbers": str(self.needExactColumnNumbers),
            "needExactColumnNames": str(self.needExactColumnNames),
            "inputColumns": json.dumps(list(self.inputColumns)),
            "outputColumns": json.dumps(list(self.outputColumns))
        }
        if self.name is not None:
            obj["name"] = str(self.name)
        if self.name is not None:
            obj["description"] = str(self.description)
        return obj

    def from_json(self, obj):
        """
        Load the Script entity from a dictionary representation of the Script.

        :param obj: Dict version of the Script.
        """
        if "id" in obj.keys():
            self.script_id = uuid.UUID(obj["id"])
        if "name" in obj.keys():
            self._name = obj["name"]
        if "description" in obj.keys():
            if obj["description"] != "None":
                self.description = obj["description"]
        if "canGeneratePlot" in obj.keys():
            if isinstance(obj["canGeneratePlot"], str) and obj["canGeneratePlot"].lower() == "false":
                self.canGeneratePlot = False
            else:
                self.canGeneratePlot = bool(obj["canGeneratePlot"])
        if "canGenerateModel" in obj.keys():
            if isinstance(obj["canGenerateModel"], str) and obj["canGenerateModel"].lower() == "false":
                self.canGenerateModel = False
            else:
                self.canGenerateModel = bool(obj["canGenerateModel"])
        if "canGenerateData" in obj.keys():
            if isinstance(obj["canGenerateData"], str) and obj["canGenerateData"].lower() == "false":
                self.canGenerateData = False
            else:
                self.canGenerateData = bool(obj["canGenerateData"])
        if "status" in obj.keys():
            self.status = str(obj["status"]).lower()
        if "needExactColumnNumbers" in obj.keys():
            if isinstance(obj["needExactColumnNumbers"], str) and obj["needExactColumnNumbers"].lower() == "false":
                self.needExactColumnNumbers = False
            else:
                self.needExactColumnNumbers = bool(obj["needExactColumnNumbers"])
        if "needExactColumnNames" in obj.keys():
            if isinstance(obj["needExactColumnNames"], str) and obj["needExactColumnNames"].lower() == "false":
                self.needExactColumnNames = False
            else:
                self.needExactColumnNames = bool(obj["needExactColumnNames"])
        if "inputColumns" in obj.keys():
            if obj["inputColumns"].lower() == "false":
                self.inputColumns = False
            else:
                self.inputColumns = json.loads(obj["inputColumns"])
        if "outputColumns" in obj.keys():
            if obj["outputColumns"].lower() == "false":
                self.outputColumns = False
            else:
                self.outputColumns = json.loads(obj["outputColumns"])

    def copy(self, myfunction):
        """
        Copy your function code and decorators to a format executable by the Wizata App.
        :param myfunction: your function - pass the function itself as parameter
        """

        if myfunction.__code__.co_argcount < 1:
            raise ValueError('your function must contains at least one parameter')

        self.function = Function()

        self.function.id = myfunction.__name__
        self.function.params = inspect.signature(myfunction).parameters

        self._name = myfunction.__name__

        self.function.code = myfunction.__code__

        f_globals = myfunction.__globals__
        self.function.globals = []
        for k_global in f_globals:
            if isinstance(myfunction.__globals__[k_global], types.ModuleType):
                module = f_globals[k_global]
                self.function.globals.append({
                    "var": k_global,
                    "module": str(module.__name__)
                })

        if myfunction.__code__.co_filename is not None:
            if os.path.exists(myfunction.__code__.co_filename):
                with open(myfunction.__code__.co_filename, "r") as f:
                    source_code = f.read()
                self.source = source_code


class Function:
    """
    Python Code Function

    :ivar id: technical name and then id of the function
    :ivar code: code of the function __code__
    :ivar globals: modules references __globals__
    """

    def __init__(self):
        self.id = None
        self.code = None
        self.globals = None
        self.params = OrderedDict()
