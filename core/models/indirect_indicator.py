from django.db import models
import re

find_square_bracket_keys = re.compile(r"\[(.*?)\]")

class IndirectIndicator(models.Model):
    topic = models.ForeignKey('Topic', related_name='indirect_indicators', on_delete=models.CASCADE)

    key = models.CharField(max_length=255, blank=False)
    formula = models.CharField(max_length=511, unique=False, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(blank=True, null=True)
    pre_unit = models.CharField(max_length=30, blank=True, default="")      # Examples: $,€
    post_unit = models.CharField(max_length=30, blank=True, default="")     # Examples: %, points, persons
    
    TEXT = "text"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    SINGLECHOICE = "singlechoice" # UI: RadioButton, Scale, Dropdown
    MULTIPLECHOICE = "multiplechoice" # UI: Checkbox, Scale (1-3 on 1:10 scale for example)
    

    DATA_TYPES = (
        (TEXT, "text"),
        (INTEGER, "integer"),
        (DOUBLE, "double"),
        (DATE, "date"),
        (BOOLEAN, "boolean"),
        (SINGLECHOICE, "singlechoice"),
        (MULTIPLECHOICE, "multiplechoice")
    )

    datatype = models.CharField(max_length=50, blank=False, choices=DATA_TYPES, default="text")
    
    PERFORMANCE = "PERFORMANCE"
    SCORING = "SCORING"

    INDICATOR_TYPES = (
        (PERFORMANCE, "performance"),
        (SCORING, "scoring")
    )

    
    type = models.CharField(max_length=50, blank=False, choices=INDICATOR_TYPES, default="SCORING")

    calculation = ''
    value = None
    has_conditionals = False
    exception = None
    exception_detail = None
    responses = None



    class Meta: 
        unique_together = ['key', 'topic']

    def __init__(self, *args, **kwargs):
        super(IndirectIndicator, self).__init__(*args, **kwargs)
        self.calculation = self.formula.replace("\n", "") # .lower()

        if self.calculation.startswith("IF"):
            if self.key == "gender_decision_making_ratio_score":
                print('xxxxxxxxxxxxxxxx', self.calculation.startswith("IF"))
            self.has_conditionals = True
    
    def __str__(self):
        return self.key
    
    # @property
    # def key(self):
    #     return self.name
    
    @property
    def calculation_keys(self):
        calculation_keys =  re.findall(find_square_bracket_keys, self.calculation)
        calculation_keys_uniques = list(set(calculation_keys))

        if self.key in calculation_keys_uniques:
            calculation_keys_uniques.remove(self.key)
        return calculation_keys_uniques

    def find_values(self, key_value_list):
        calculation = self.calculation

        for calculation_key in self.calculation_keys:
            if calculation_key in key_value_list:
                if calculation_key == "decision_making_ratio_score":
                    print('yyyyyyyyyyyyy', key_value_list[calculation_key])
                if key_value_list[calculation_key] is not None:
                    value = key_value_list[calculation_key]
                    if isinstance(value, dict):
                        value = max(value, key=value.get)
                    calculation = calculation.replace(f"[{calculation_key}]", f"{value}")
                # else:
                #     print(f'[{calculation_key}] ... could not be used, since it has a none value!')

        self.calculation = calculation

    def calculate(self):
        # if self.value:
        #     return
        if self.key == 'gender_equity_score':
                    print('--->',self.calculation, self.has_conditionals, self.calculation_keys)

        if len(self.calculation_keys) and not self.has_conditionals:
            self.exception = Exception("Not all keys are replaced with values")
            return

        self.exception = None
        self.error = None
        try:
            if self.has_conditionals:
                self.value = None
                value = self.calculate_conditionals()
                if not value:
                    return
                print('ss',value)
                #if '=' in value:
                #    print('check')
                #     value = value.replace('”', '')
                #     [var, value] = value.split('=')
                print('dd', value)
                # value = value.replace(" ", "").replace('"', "")
                print('>>',value)
                self.value = value
                try:
                    self.value = eval(value)
                    print(self.value)
                except:
                    self.value = value
                print('>>',self.value)
            else:
                self.value = eval(self.calculation)
        except Exception as e:
            print('reee', e)
            self.exception_detail = e
            self.exception = Exception("Invalid calculation")
            
    def calculate_conditionals(self):
        conditions = self.calculation.split("ELSE")
        #print(conditions)
        for condition in conditions:
            bracket_keys = list(set(re.findall(find_square_bracket_keys, condition)))
            bracket_keys.remove(self.key)
            if len(bracket_keys):
                print(self.key)
                raise Exception("invalid partial condition")

            if condition == conditions[-1]:
                val = condition
                # print(val)
                break

            [cond, val] = [x.strip() for x in condition.split('THEN')]
            cond = cond.replace('IF', '')

            if 'AND' in cond:
                conds = [eval(n) for n in cond.split("AND")]

                if not False in conds:
                    break

                continue
            
            if 'OR' in cond:
                conds = [eval(n) for n in cond.split('OR')]

                if True in conds:
                    break

                continue

            if eval(cond):
                #print(cond)
                break
            #print(condition)
        if '=' in val:
            val = val.replace('"', '').replace('(', '').replace(')', '').replace('\\', '')
            [var, val] = val.split('=')
            var = var.replace('[', '').replace(']', '').strip()

            if var != self.key:
                raise Exception('Assignment variable does not match the key of this indirect indicator')

        return val
'''
    def calculate_conditionals(self):
        conditions = self.calculation.split("else")

        for condition in conditions:
            print('=================', condition)
            # Checks if all required indicators have values
            if len(re.findall(find_square_bracket_keys, condition)):
                raise Exception("invalid partial condition")
                
            if condition == conditions[-1]:
                return condition
                break

            [cond, value] = condition.split("THEN")
            cond = cond.replace("if", "")

            if 'if' in cond:
                [cond, value] = condition.split("THEN")
                cond = cond.replace("if", "")

            if '==' in cond:
                [val1, val2] = cond.split("==")
                if eval(f'"{val1}"=="{val2}"'):
                    return value

            if 'AND' in cond:
                conds = [eval(n) for n in condition.split("AND")]
                if not False in conds:
                    return value

            if 'OR' in cond:
                conds = [eval(n) for n in condition.split("OR")]
                if True in conds:
                    return value

            if eval(cond):
                return value
        '''
        

# TODO: Accept ((cond AND cond) OR cond), instead of (cond AND cond) on itself and (cond OR cond) 
'''
formula = "if 'workers_cooperative'=='workers.cooperative' then if (0.67 < 0.60) then decision_making_ratio_score = 0 else decision_making_ratio_score = 10 else if (0.25 < 0.30) then decision_making_ratio_score = 15 else decision_making_ratio_score = 20"


formula = formula.replace('if', '@@if').replace('else', '##else').replace('then', '%%then')
formula = re.split('@@|##|%%', formula)
print(formula)
ifs = 1
elses = 0
last_if = False
search_else = False

for cond in formula:

    # Skips code till it finds the corresponding else statement of the if statement that equalled to False.
	if search_else:
		if 'if' in cond:
			ifs += 1
		if 'else' in cond:
			elses += 1
		if ifs != elses:
			continue
		else:
			search_else = False
			last_if = True
			ifs = 1
			elses = 0

    # Checks whether if statement equals to True
	if 'if' in cond:
		cond = cond.replace('if', '').strip()
		last_if = False
		if eval(cond):
			last_if = True
		else:
			search_else = True

    # Serves conditional outcome
	if (last_if and ' = ' in cond) or (cond == formula[-1]):
		print('\nConditional outcome:\n-', cond) #cond.replace('then ', '').replace('else', ''))
		break
'''