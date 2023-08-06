import configparser
from enum import Enum
import re


class DataSpec:
    _rule_reg = re.compile(r'"(?P<unit1>[^#]+)" +(?P<operation>addto|rename) +"(?P<unit2>[^#]+)" *(?P<comment>$| *#.+)')
    _default_var_name = "_DEFAULT"
    _default_datatype = "str"
    _default_unit = ""
    _default_rounding = "warn"
    _default_precision = 3

    def __init__(self):
        """
        Helper class, for extracting data from the .conf file into nice OOP form
        """
        self.index_rules = None
        self.default_varspec = self._gen_default_varspec()
        self.varspecs = {}

    def add_varspec(self, var_name, varspec):
        self.varspecs[var_name] = varspec

    def get_default_varspec(self):
        return self.default_varspec

    def get_index_rule(self, var_name):
        if var_name in self.index_rules:
            # print(f"Returning index rules: {var_name}")
            return self.index_rules[var_name]
        else:
            # print(f"No rules found: {var_name}")
            return {}

    def get_index_rules(self):
        return self.index_rules

    def get_varspec(self, var_name):
        # If we have a spec for the var, return it
        return self.varspecs[var_name] if var_name in self.varspecs else self.default_varspec

    def set_default_rule(self, default_varspec):
        self.default_varspec = default_varspec

    def set_index_rules(self, index_rules):
        self.index_rules = index_rules

    @classmethod
    def _gen_default_varspec(cls):
        # All the default values for every setting
        default_varspec = VarSpec(
            name=cls._default_var_name,
            datatype=cls._default_datatype,
            unit=cls._default_unit,
            rounding=cls._default_rounding,
            precision=cls._default_precision,
        )
        return default_varspec

    @classmethod
    def _parse_index_rule(cls, rule_str):
        reg_result = cls._rule_reg.search(rule_str)
        result_dict = reg_result.groupdict()
        # Strip the "#" (and leading/trailing whitespace) from the comment
        result_dict["comment"] = result_dict["comment"].replace("#", "").strip()
        result_rule = IndexRule.from_dict(result_dict)
        return result_rule

    @classmethod
    def _parse_index_rules(cls, rules_str):
        rule_str_list = [r.strip() for r in rules_str.split("\n") if len(r.strip()) > 0]
        rule_info_list = []
        for rule_str in rule_str_list:
            cur_rule_dict = cls._parse_index_rule(rule_str)
            rule_info_list.append(cur_rule_dict)
        return rule_info_list

    @classmethod
    def from_file(cls, fpath):
        loaded_spec = DataSpec()
        parser = configparser.ConfigParser()
        parser.read(fpath)
        section_list = parser.sections()
        # First we "pull out" the special sections
        # index_rules
        if "index_rules" in section_list:
            index_rule_dict = dict(parser["index_rules"])
            # Keys are index vars, values are the rules
            # And we need to treat any newlines as the same as "|" and then
            # apply the parser
            index_rule_dict = {k: cls._parse_index_rules(v.replace("|", "\n")) for k, v in index_rule_dict.items()}
            loaded_spec.set_index_rules(index_rule_dict)
            section_list.remove("index_rules")
        # We also make a "_DEFAULT" spec, which will just get the "GLOBAL" section
        # copied to it and nothing else
        # And we also need to copy the "GLOBAL" section contents to all the other
        # sections (if it exists)
        if "GLOBAL" in section_list:
            # We just copy this setting into all the other sections
            # Remove GLOBAL
            section_list.remove("GLOBAL")
            # And copy it over the rest
            for cur_var in section_list:
                parser[cur_var].update(parser["GLOBAL"])
        # Now the only sections in section_list should be (non-index) vars
        for cur_varname in section_list:
            var_config = dict(parser[cur_varname])
            ### Variable type
            # Default type: str
            var_datatype = var_config["datatype"] if "datatype" in var_config else cls._default_datatype
            ### Desired unit
            # Default is "" (representing just "ones")
            unit_spec = var_config["unit"] if "unit" in var_config else cls._default_unit
            ### Rounding spec
            # Default is "warn"
            rounding_spec = var_config['rounding'] if 'rounding' in var_config else cls._default_rounding
            ### Precision spec
            # Default is 3
            precision_spec = var_config["precision"] if "precision" in var_config else cls._default_precision
            # And create the full spec dict for this var
            var_dict = {"name": cur_varname, "datatype": var_datatype, "unit": unit_spec,
                        "rounding": rounding_spec, "precision": precision_spec}
            var_spec = VarSpec.from_dict(var_dict)
            # And add it to loaded_spec
            loaded_spec.add_varspec(cur_varname, var_spec)
        # And lastly the defaults
        loaded_spec.set_default_rule(cls._gen_default_varspec())
        return loaded_spec


class IndexRule:
    class RuleType(Enum):
        RENAME = 1
        ADDTO = 2

    def __init__(self, unit1, operation, unit2, comment=''):
        """
        :param unit1:
        :param operation:
        :param unit2:
        :param comment:
        """
        self.unit1 = unit1
        self.operation = self.RuleType[operation.upper()]
        self.unit2 = unit2
        self.comment = comment

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "IndexRule[ " + ("Add " if self.is_addto() else "Rename ") + self.unit1 + " to " + self.unit2 + " ]"

    def is_addto(self):
        return self.operation == self.RuleType.ADDTO

    def is_rename(self):
        return self.operation == self.RuleType.RENAME

    @classmethod
    def from_dict(cls, rule_dict):
        return IndexRule(rule_dict['unit1'], rule_dict['operation'],
                         rule_dict['unit2'], rule_dict['comment'])


class VarSpec:
    def __init__(self, name, datatype, unit, rounding, precision):
        """

        """
        self.name = name
        self.datatype = datatype
        self.unit = unit
        self.rounding = rounding
        self.precision = precision

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"VarSpec[{self.name}: datatype={self.datatype}, unit={self.unit}, rounding={self.rounding}, precision={self.precision}]"

    def get_datatype(self):
        return self.datatype

    def get_precision(self):
        return self.precision

    @classmethod
    def from_dict(cls, rule_dict):
        return VarSpec(
            name=rule_dict['name'], datatype=rule_dict['datatype'],
            unit=rule_dict['unit'], rounding=rule_dict['rounding'],
            precision=rule_dict['precision']
        )