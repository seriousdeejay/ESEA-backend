from django.db import models
import re
import statistics

from .direct_indicator import DirectIndicator

find_square_bracket_keys = re.compile(r"\[(.*?)\]")

class IndirectIndicator(models.Model):
    topic = models.ForeignKey('Topic', related_name='indirect_indicators', on_delete=models.SET_NULL, null=True)
    method = models.ForeignKey("Method", related_name="indirect_indicators", on_delete=models.CASCADE, null=True)
    key = models.CharField(max_length=255, blank=False)
    formula = models.CharField(max_length=1000, unique=False, blank=False)
    name = models.CharField(max_length=255, unique=False, blank=False)
    description = models.TextField(blank=True, null=True)
    pre_unit = models.CharField(max_length=30, blank=True, default="")      # Examples: $,€
    post_unit = models.CharField(max_length=30, blank=True, default="")     # Examples: %, points, persons
    
    TEXT = "text"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    BOOLEAN = "boolean"
    SINGLECHOICE = "singlechoice"
    MULTIPLECHOICE = "multiplechoice"
    

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
        unique_together = ['key', 'method']

    def __init__(self, *args, **kwargs):
        super(IndirectIndicator, self).__init__(*args, **kwargs)
        self.calculation = self.formula.replace("\n", "")

        if self.calculation.strip().startswith("IF"):
            self.has_conditionals = True
    
    def __str__(self):
        return self.key
    
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
                if key_value_list[calculation_key] is not None:
                    value = key_value_list[calculation_key]
                    if isinstance(value, dict):
                        value = max(value, key=value.get)
                    calculation = calculation.replace(f"[{calculation_key}]", f"{value}")

        self.calculation = calculation

    def calculate(self):
        if len(self.calculation_keys) and not self.has_conditionals:
            self.exception = Exception("Not all keys are replaced with values")
            return

        self.exception = None
        self.error = None
        functionList = ['sum(', 'avg(', 'min(', 'max(', 'median(', 'mode(']

        ## CONDITIONALS
        if self.has_conditionals:
            self.value = None
            value = self.calculate_conditionals()
            print('vallueee', type(value))
            self.value = value
            print('||', self.key, self.value)
        
        ## FUNCTIONS
        elif any(func in self.calculation for func in functionList):
            key = re.findall(find_square_bracket_keys, self.formula)
            if len(key):
                directind = DirectIndicator.objects.filter(method=self.method, key=key[0]).first()
                indirectind = IndirectIndicator.objects.filter(method=self.method, key=key[0]).first()
                if directind is not None:
                    indicator = directind
                else:
                    indicator = indirectind
                if True: # len(direct_indicator.responses) or not len(direct_indicator.responses)
                    # responses = [float(r) for r in indicator.responses]
                    responses = [1, 3, 4, 7, 8]
                    if 'avg(' in self.calculation:
                        self.value = sum(responses)/len(responses) # int(direct_indicator.value)
                    elif 'sum(' in self.calculation:
                            self.value = sum(responses)
                    elif 'min(' in self.calculation:
                        self.value = min(responses)
                    elif 'max(' in self.calculation:
                        self.value = max(responses)
                    elif 'median(' in self.calculation:
                        self.value = statistics.median(responses)
                    elif 'mode(' in self.calculation:
                        self.value = statistics.mode(responses)
                else:
                    self.value = 1
                    print('There are no responses to calculate the sum with.')
                    return

        # REGULAR CALCULATIONS
        else:
            print(self.method)
            print(self.key, self.calculation)
            try:
                self.value = eval(self.calculation)
            except:
                self.value = None

    def calculate_conditionals(self):
        formula = self.calculation.replace('IF', '@@IF').replace('ELSE', '##ELSE').replace('THEN', '%%THEN')
        formula = [x.strip() for x in re.split('@@|##|%%', formula)]
        formula = list(filter(lambda x: x != '', formula))
        print(f'\n  {self.key}: Start Conditional Calculations... \nformula: {formula}')

        ifs = 1
        elses = 0
        last_if = False
        search_else = False
        val = None

        for cond in formula:
            print('-->', cond)
            bracket_keys = list(set(re.findall(find_square_bracket_keys, cond)))

            if self.key in bracket_keys:
                bracket_keys.remove(self.key)
            if len(bracket_keys):
                print('Invalid Partial Condition: ', bracket_keys)
                # raise Exception("invalid partial condition")

            ## Skips code till it finds the corresponding then/else statements corresponding to the IF statement that fails or succeeds.
            if search_else:
                if 'IF' in cond:
                    ifs += 1
                if 'ELSE' in cond:
                    elses += 1
                if ifs != elses:
                    continue
                else:
                    search_else = False
                    last_if = True
                    ifs = 1
                    elses = 0

            ## Checks whether if statement equates to True
            if 'IF' in cond:
                cond = cond.replace('IF', '').replace('(', '').replace(')', '').replace('"', '').strip()
                last_if = False
                
                if 'AND' in cond:
                    conds = cond.split("AND")
                    conds = self.process_expression(conds)
                    evaluatedconds = [eval(n) for n in conds]

                    if not False in evaluatedconds:
                        last_if = True
                    else:
                        search_else = True
                    continue
                
                if 'OR' in cond:
                    conds = cond.split("OR")
                    conds = self.process_expression(conds)
                    evaluatedconds = [eval(n) for n in conds]      

                    if True in evaluatedconds:
                        last_if = True
                    else:
                        search_else = True
                    continue

                cond = self.process_expression(cond)
                if eval(cond):
                    last_if = True
                else:
                    search_else = True
                continue

            # Serves conditional outcome
            if (last_if and '=' in cond) or (cond == formula[-1]):
                cond = cond.replace('(', '').replace(')', '')
                [var, val] = cond.split('=')
                var = var.replace('THEN', '').replace('ELSE', '')
                var = var.replace('[', '').replace(']', '').strip()
                if var != self.key:
                    raise Exception('Assignment variable does not match the key of this indirect indicator')
                val = val.replace('"', '')
                try:
                    val = eval(val)
                except:
                    pass
                
                return str(val)
        
    def process_expression(self, conds):
        allowedOperators = ['<', '<=', '==', '>=', '>', '=']

        if not isinstance(conds, list):
            conds = [conds]

        for index, cond in enumerate(conds):
            # cond = cond.replace('=', '==')
            processed_cond = re.split('(<|<=|==|>=|>|=)', cond)
            for idx, value in enumerate(processed_cond):
                if value not in allowedOperators:
                    ## Makes eval() of string equals string possible
                    processed_cond[idx] = f'"{value.strip().lower()}"'
            conds[index] = ''.join(processed_cond)

        if len(conds) == 1:
            conds = conds[0]

        return conds

            
        # @property
        # def key(self):
        #     return self.name
        # except Exception as e:
        #     print('reee', e)
        #     self.exception_detail = e
        #     self.exception = Exception("Invalid calculation")
        # for x in conditions:
        #     print('-->', x)
        #     for y, index in enumerate(x.split('THEN')):
        #         print('\n', y, index)
        #     #[cond, val] = [y.strip() for y in x.split('THEN')]
        #     #print(cond)

        # for condition in conditions:
        #     if 'THEN' in condition:
        #         bracket_keys = list(set(re.findall(find_square_bracket_keys, condition)))

        #         if self.key in bracket_keys:
        #             bracket_keys.remove(self.key)
        #         if len(bracket_keys):
        #             # print(bracket_keys)
        #             raise Exception("invalid partial condition")

        #         [cond, val] = [x.strip() for x in condition.split('THEN')] #
        #         cond = cond.replace('IF', '')

        #         if 'AND' in cond:
        #             conds = [eval(n) for n in cond.split("AND")]

        #             if not False in conds:
        #                 break
        #             cond = 'False'
        #             continue
                
        #         if 'OR' in cond:
        #             conds = [eval(n) for n in cond.split('OR')]
        #             # print('IIIIIIIIIIIII', conds, val)
        #             if True in conds:
        #                 break
        #             cond = 'False'
        #             continue

        #         if eval(cond):
        #             break

        #         if condition == conditions[-1]:
        #             break
        # if '=' in val:
        #     # print(val)
        #     [thenn, elsee] = [x.strip() for x in val.split('ELSE')]
        #     # print('then', thenn)
        #     # print('else', elsee)
        #     # print('----dd---')
        #     if eval(cond):
        #         # print('-------')
        #         val = thenn
        #     else:
        #         # print(self.key, val)
        #         val = elsee

        #     # print(val)
        #     val = val.replace('"', '').replace('(', '').replace(')', '').replace('\\', '')
        #     [var, val] = val.split('=')
        #     var = var.replace('[', '').replace(']', '').strip()

        #     if var != self.key:
        #         raise Exception('Assignment variable does not match the key of this indirect indicator')

        return []
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