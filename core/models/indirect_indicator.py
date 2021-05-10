from django.db import models
import re

find_square_bracket_keys = re.compile(r"\[(.*?)\]")

class IndirectIndicator(models.Model):
    topic = models.ForeignKey('Topic', related_name='indirect_indicators', on_delete=models.CASCADE)

    key = models.CharField(max_length=255, blank=False)
    formula = models.CharField(max_length=255, unique=False, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(blank=True, null=True)
    
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    DOUBLE = "DOUBLE"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"

    DATA_TYPES = (
        (TEXT, "Text"),
        (INTEGER, "Integer"),
        (DOUBLE, "Double"),
        (DATE, "Date"),
    )
    datatype = models.CharField(max_length=100, blank=False, choices=DATA_TYPES, default="TEXT")
    
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
        self.calculation = self.formula.lower().replace("\n", "")
        if self.calculation.startswith("if"):
            self.has_conditionals = True
    
    def __str__(self):
        return self.key
    
    # @property
    # def key(self):
    #     return self.name
    
    @property
    def calculation_keys(self):
        return re.findall(find_square_bracket_keys, self.calculation)

    def find_values(self, key_value_list):
        calculation = self.calculation
        for calculation_key in self.calculation_keys:
            # print(calculation_key)
            if calculation_key in key_value_list:
                # if calculation_key == 'gender_decision_making_ratio_score':
                #     print('gottem', key_value_list['gender_decision_making_ratio_score'])
                #     self.value="0"
                if key_value_list[calculation_key] is not None:
                    value = key_value_list[calculation_key]
                    if isinstance(value, dict):
                        value = max(value, key=value.get)
                    calculation = calculation.replace(f"[{calculation_key}]", f"{value}")
                    # if self.key == 'gender_equity_score':
                    #     print('-------------------------',key_value_list)
                    #     ii = IndirectIndicator.objects.filter(key='gender_pay_gap_score').first()
                    #     print('hh', ii.value)
                    #     print('f:', calculation, key_value_list)
                    # if self.key == 'gender_decision_making_ratio_score':
                    #     print('f::>>', calculation, self.value)
                # else:
                #     print(f'[{calculation_key}] ... could not be used, since it has a none value!')

        self.calculation = calculation

    def calculate(self):
        if self.value:
            return

        if len(self.calculation_keys) and not self.has_conditionals:
            self.exception = Exception("Not all keys are replaced with values")
            return

        self.exception = None
        self.error = None
        try:
            if self.has_conditionals:
                self.value = None
                #print(self.key, self.value)
                value = self.calculate_conditionals()

                #print(self.key,' = ' , value)
                if self.key =='company_size':
                    print(value)
                if '=' in value:
                    value = value.replace('”', '')
                    [var, value] = value.split('=')
                value = value.replace(" ", "").replace('"', "")

                try:
                    self.value = eval(value)
                except:
                    self.value = value
                if self.key == 'gender_ratio_score':
                    pass #print('----', self.value)

                

                #if self.key == 'gender_decision_making_ratio_score':
                
            else:
                if self.key == 'gender_equity_score':
                    print(self.calculation)
                self.value = eval(self.calculation)
            # print('>>>>>>>>', type(self.value))
        except Exception as e:
            self.exception_detail = e
            self.exception = Exception("Invalid calculation")

    def calculate_conditionals(self):
        conditions = self.calculation.split("else")

        for condition in conditions:

            # Checks if all required indicators have values
            if len(re.findall(find_square_bracket_keys, condition)):

                raise Exception("invalid partial condition")
                
            if condition == conditions[-1]:
                return condition
                break

            [cond, value] = condition.split("then")
            cond = cond.replace("if", "")

            if 'if' in cond:
                [cond, value] = condition.split("then")
                cond = cond.replace("if", "")

            if '==' in cond:
                [val1, val2] = cond.split("==")
                if eval(f'"{val1}"=="{val2}"'):
                    return value

            if 'AND' in cond:
                conds = [eval(n) for n in condition.split("and")]
                if not False in conds:
                    return value

            if 'OR' in cond:
                conds = [eval(n) for n in condition.split("or")]
                if True in conds:
                    return value

            if eval(cond):
                return value
        

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