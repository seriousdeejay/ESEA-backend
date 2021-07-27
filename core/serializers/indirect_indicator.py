import re
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from ..models import IndirectIndicator, DirectIndicator, Topic

find_questions_by_square_brackets = re.compile(r"\[.*?\]")

class IndirectIndicatorSerializer(WritableNestedModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(queryset=Topic.objects.all(), required=False)


    class Meta:
        model = IndirectIndicator
        fields = '__all__'

    # def validate_topic(self, value):
    #     method_pk = self.initial_data['method']
    #     if value.method.pk != method_pk:
    #         raise serializers.ValidationError('Topic not found in method')
    #     return value

    def validate_formula(self, value):
        value = value.lower()
        if self.instance:
            method_pk = self.instance.method
        else:
            method_pk = self.initial_data['method']

        questions = re.findall(find_questions_by_square_brackets, value)
        print(questions)
        if not len(questions):
            raise serializers.ValidationError("Needs to contain atleast one question")
        
        if ((value.count('[') + value.count(']')) % 2):
            raise serializers.ValidationError('Uneven amount of brackets!')

        testformula = value
        for question in questions:
            question = question[1:-1]
            if question != self.initial_data['key']:
                try:
                    DirectIndicator.objects.get(key=question, method=method_pk)
                except:
                    try:
                        IndirectIndicator.objects.get(key=question, method=method_pk)
                    except Exception:
                        raise serializers.ValidationError(f"Question with id '{question}' not found")
                
            testformula = testformula.replace(f"[{question}]", " 1 ")

        if 'if' in value or 'then' in value or 'else' in value:
            if value.count('if ') > value.count('then'):
                raise serializers.ValidationError("Missing 'then' statement")

            if value.count('if ') < value.count('then'):
                raise serializers.ValidationError("Missing 'if' statement")
            
            if value.count('if') < value.count('else'):
                raise serializers.ValidationError("Missing 'if' statement")
            
            conditionalformula = value.replace('if', 'temporaryif').replace('then', 'temporarythen').replace('else', 'temporaryelse')
            splittedvalue = re.split('temporary', conditionalformula)

            expecting_if = False
            for index, cond in enumerate(splittedvalue):
                questions = re.findall(find_questions_by_square_brackets, cond)
                cleanedcond = cond

                for question in questions: 
                    cleanedcond = cleanedcond.replace(f"{question}", "123 ")

                if 'if' in cond:
                    try:
                        eval(cleanedcond.replace('if', '').strip())
                    except:
                        raise serializers.ValidationError(f"'{cond}': Invalid conditional")
                    expecting_if = False

                if expecting_if:
                    raise serializers.ValidationError(f" '{splittedvalue[index-1] + '^^' + splittedvalue[index]}': Should contain valid if-statement or assignment")
                if 'then' in cond or 'else' in cond:
                    if '=' in cond:
                        [var, val] = cleanedcond.replace('then', '').replace('else', '').replace('(', '').replace(')', '').split('=')
                        var = var.strip()
                        val = val.strip()
                        if not len(val):
                            raise serializers.ValidationError(f" '{cond}': Assigment requires a value")
                        if not len(var):
                            raise serializers.ValidationError(f" '{cond}': Assignment requires a variable")
                        if var != '123' and var != self.initial_data['key']:
                            print('-->', var)
                            raise serializers.ValidationError(f" '{cond}': Assignment variable is an invalid bracket indicator")

                        continue

                    if cond == splittedvalue[-1]:
                        raise serializers.ValidationError(f" '{cond}': Assignment expected")

                    expecting_if = True

        else:
            try:
                eval(testformula)
            except:
                raise serializers.ValidationError('Questions should be separated by arithmetic symbols')

        return value
    
    def validate_name(self, value):

        if self.instance:
            method_pk = self.instance.method
        else:
            method_pk = self.initial_data['method']

        if self.instance and self.instance.name == value:
            return value
        
        indirect_indicator = IndirectIndicator.objects.filter(name=value, method=method_pk)

        if indirect_indicator.exists():
            raise serializers.ValidationError('Name is not unique')

        return value

    def validate_key(self, value):
        if self.instance:
            method_pk = self.instance.method
        else:
            method_pk = self.initial_data['method']

        if self.instance and self.instance.key == value:
            return value
        
        indirect_indicator = IndirectIndicator.objects.filter(key=value, method=method_pk)

        if indirect_indicator.exists():
            raise serializers.ValidationError('Key is not unique')

        return value