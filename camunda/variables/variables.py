
import json

class Variables:
    def __init__(self, variables={}):
        self.variables = variables

    def get_variable(self, variable_name, with_meta=False):
        variable = self.variables.get(variable_name, None)
        if not variable:
            return None
        if with_meta:
            return variable
        return variable["value"]

    @classmethod
    def format(cls, variables):
        """
        Gives the correct format to variables.
        :param variables: dict - Dictionary of variable names to values.
        :return: Dictionary of well formed variables
            {"var1": 1, "var2": True}
            ->
            {"var1": {"value": 1}, "var2": {"value": True}}
        """
        formatted_vars = {}
        if variables:
            for i in variables.keys():
                 if type(variables[i]) in [bool, int, float, str]:
                     formatted_vars[i] = {"value": variables[i]}
                 elif type(variables[i]) == dict and "value" in variables[i] and type(variables[i]['value']) in [bool, int, float, str]:
                     formatted_vars[i] = variables[i]
                 elif type(variables[i]) == list:
                     formatted_vars[i] = {"value": json.dumps(variables[i]), #r'[\"{}\"]'.format(r'\",\"'.join(variables[i]))
                                          "type": "object",
                                          "valueInfo": { 
                                            "objectTypeName": "java.util.ArrayList", 
                                            "serializationDataFormat": "application/json"
                                          }
                                         }
                 else:
                     formatted_vars[i] = {"value": json.dumps(variables[i]), "type": "json"}
        return formatted_vars

    def to_dict(self):
        """
        Converts the variables to a simple dictionary
        :return: dict
            {"var1": {"value": 1}, "var2": {"value": True}}
            ->
            {"var1": 1, "var2": True}
        """
        result = {}
        for k, v in self.variables.items():
            result[k] = v["value"]
        return result
