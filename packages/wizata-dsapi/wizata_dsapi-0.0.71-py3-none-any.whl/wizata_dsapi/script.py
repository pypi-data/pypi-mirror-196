import uuid
import dill


class Script:

    def __init__(self, script_id=None):

        # Id
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id

        # Properties
        self.name = None
        self.description = None
        self.canGeneratePlot = False
        self.canGenerateModel = False
        self.canGenerateData = False
        self.status = "draft"
        self.needExactColumnNumbers = False
        self.needExactColumnNames = False
        self.inputColumns = []
        self.outputColumns = []

        # Function properties (code)
        self.function = None

    def to_json(self):
        return {
            "script_id": str(self.script_id),
            "name": str(self.name),
            "description": str(self.description),
            "canGeneratePlot": str(self.canGeneratePlot),
            "canGenerateModel": str(self.canGenerateModel),
            "canGenerateData": str(self.canGenerateData),
            "status": str(self.status),
            "needExactColumnNumbers": str(self.needExactColumnNumbers),
            "needExactColumnNames": str(self.needExactColumnNames),
            "inputColumns": list(self.inputColumns),
            "outputColumns": list(self.outputColumns)
        }

    def from_json(self, json):
        if "script_id" in json.keys():
            self.script_id = uuid.UUID(json["script_id"])
        if "name" in json.keys():
            self.name = json["name"]
        if "description" in json.keys():
            self.name = json["description"]
        if "canGeneratePlot" in json.keys():
            self.name = bool(json["canGeneratePlot"])
        if "canGenerateModel" in json.keys():
            self.name = bool(json["canGenerateModel"])
        if "canGenerateData" in json.keys():
            self.name = bool(json["canGenerateData"])
        if "status" in json.keys():
            self.name = json["status"]
        if "needExactColumnNumbers" in json.keys():
            self.name = bool(json["needExactColumnNumbers"])
        if "needExactColumnNames" in json.keys():
            self.name = bool(json["needExactColumnNames"])
        if "inputColumns" in json.keys():
            self.name = json["inputColumns"]
        if "outputColumns" in json.keys():
            self.name = json["outputColumns"]

    def copy(self, myfunction):
        self.function = Function()
        self.function.code = myfunction.__code__


class Function:

    def __init__(self):
        self.code = None
