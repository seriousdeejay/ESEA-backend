from ..models import Method, Survey, Section, Topic, Question, DirectIndicator, IndirectIndicator

def process_textual_method(file, uploader):
    global start
    global myList

    start = 0
    myList = []

    for line in file:
        line = line.decode('cp1252').strip()

        if line[:2] != '//' and len(line):
            myList.append(line)
   
    for index, entry in enumerate(myList):
        if entry.startswith('Topics:'):
            method_instance = process_method(processor(index), uploader)

        if entry.startswith('Indicators:'):
            topic_dict = process_topics(processor(index), method_instance)

        if entry.startswith('Surveys:'):
        #if re.search('^Surveys:', entry):
            process_indicators(processor(index), method_instance, topic_dict)
        
        if entry.startswith('Surveys:'):
            process_surveys(index, method_instance)



def processor(index):
    FormulaLine = False
    partialList = myList[start:index]

    if partialList[0] in ['Indicators:', 'Topics:']:
        partialList = partialList[1:]

    for ix, item in enumerate(partialList):
        if item.startswith('Formula:'):
            FormulaLine = True
            correctindex = ix
            formula = ''
        
        if item.startswith('Type:'):
            FormulaLine = False
            partialList[correctindex] = formula
        
        if FormulaLine:
            formula += ' ' + item
    
    result = [{}]

    for item in partialList:
        try:
            key, value = item.split(":", 1)
            key = key.strip()

            if key in result[-1] and key in ['Indicator_id', 'topic_id']:
                result.append({})

            if key == 'Answer_options':
                result[-1][key] = [{}]
                continue
            
            if key in ['Order', 'Text']:
                if key in result[-1]['Answer_options'][-1]:
                    result[-1]['Answer_options'].append({})
                result[-1]['Answer_options'][-1][key] = value.strip().strip('"')
            
            result[-1][key] = value.strip('"')
        except:
            pass
    '''
    if myList[start] in ['Indicators:', 'Topics:']:
        for item in myList[start+1:index]:
            if any(word in item for word in ['Indicator_id', 'topic_id:']):
                if len(subList):
                    Info.append(subList)
                subList = []
            subList.append(item)

        Info = [[x.split(':') for x in y] for y in Info]

        for idx, nestedList in enumerate(Info):
            ### if statement only for now, since Formula can be on multiple lines
            Info[idx] = {lst[0]: lst[1].strip('"') for lst in nestedList if len(lst) > 1}
    else:
        Info = [x.split(':') for x in myList[start: index]]
        Info = {lst[0]: lst[1].strip('"') for lst in Info}
    '''

    globals()['start'] = index
    print('iii', result)
    return result


def process_method(M, uploader):
    M = M[0]
    print('>>>>>>>>>>>>>>>>', M)
    isPublic = M['isPublic'] == 'true'	# Could use eval('True') If the Boolean string is capitalised
    Version = float(M['Version'])
    method_instance = Method.objects.create(created_by=uploader, name=M['Name'], description=M['Description'], ispublic=isPublic, version=Version)
    print('++', M)
    print('\n', method_instance.__dict__)
    return method_instance


def process_topics(topics, method_instance):
    topic_dict = {}
    print('oooooo', method_instance)
    for topic in topics:
        if 'Parent_topic' in topic.keys():
            topic_instance = Topic.objects.create(name=topic['Name'], description=topic['Description'], parent_topic=topic_dict[topic['Parent_topic']], method=method_instance)
        else:
            topic_instance = Topic.objects.create(name=topic['Name'], description=topic['Description'], parent_topic=None, method=method_instance)

        topic_dict[topic['topic_id']] = topic_instance
        print(topic_instance.__dict__)

        
    #Topic.objects.filter(method__name='newmethod2').delete()
    #Method.objects.filter(name="newmethod2").delete()
    #method_instance.delete()
    print(topic_dict)
    #print('==', topics)
    return topic_dict

def process_indicators(indicators, method_instance, topic_dict):
    for indicator in indicators:
        if indicator['Indicator_type'] == 'Direct':
            I = DirectIndicator.objects.create(method=method_instance, key=indicator['Indicator_id'], name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['Topic']], pre_unit=indicator.get('PreUnit', ''), post_unit=indicator.get('PostUnit', ''), datatype=indicator['DataType'], answer_options=indicator.get('Answer_options')) # DataType=indicator['DataType']
        if indicator['Indicator_type'] == 'Indirect':
            I = IndirectIndicator.objects.create(key=indicator['Indicator_id'], name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['Topic']], formula=indicator['Formula'], pre_unit=indicator.get('PreUnit', ''), post_unit=indicator.get('PostUnit', ''), type= indicator['Type']) # DataType=indicator['DataType'] indicator.get('Type')
    print('**', indicators)

def process_surveys(index, method_instance):
    result = []
    partialList = myList[index+1:]

    segmentsDict = {'Questions': False, 'TextFragments': False, 'Certification_levels': False, 'Validation_rules': False}
    Sections = False
    
    for item in partialList:
        key, value = [x.strip('"') for x in item.split(":", 1)]
        if value in ['true', 'True', 'false', 'False']:
            value = eval(value.capitalize())

        if key == 'survey_id':
            result.append({})
            Sections = False
        
        elif item.startswith('Sections:'):
            Sections = True
            result[-1]['Sections'] = []
            continue
        
        elif Sections:
            if key == 'section_id':
                segmentsDict = {x: False for x in segmentsDict}
                result[-1]['Sections'].append({})
            
            elif item.startswith(tuple(segmentsDict)):
                segment = next(filter(item.startswith, tuple(segmentsDict)))
                segmentsDict = {x: False for x in segmentsDict}
                segmentsDict[segment] = True

                result[-1]['Sections'][-1][segment] = []
                continue

            elif True in segmentsDict.values():
                segment, = [x for x in segmentsDict if segmentsDict[x] is True]
                
                if key in ['question_id', 'certification_id', 'Text', 'Type']:
                    result[-1]['Sections'][-1][segment].append({})

                result[-1]['Sections'][-1][segment][-1][key] = value
            
            elif True not in segmentsDict.values():
                result[-1]['Sections'][-1][key] = value
        
        if not Sections:
            result[-1][key] = value
    
    print(result)

    for survey in result:
        surv = Survey.objects.create(method=method_instance, name=survey['Name'], description=survey['Description'], response_type=survey['SurveyType'], welcome_text=survey.get('WelcomeTxt', ''), closing_text=survey.get('ClosingTxt', ''), min_threshold=float(survey['MinThreshold']), anonymous=survey.get('Anonymous', False))
        
        surveyQuestions = []
        for section in survey['Sections']:
            sect = Section.objects.create(survey=surv, order=section['Order'], title=section['Title'])
            for question in section['Questions']:
                # q, created = Question.objects.get_or_create()
                i = DirectIndicator.objects.filter(key=question['Indicator']).first()
                topic = i.topic
                # Question.objects.filter(name=question['Name']).delete()
                q = Question.objects.create(section=sect, name=question['Name'], description=question['Description'], isMandatory=question['isMandatory'], indicator=i, uiComponent=question['UIComponent'], order=question['Order'], instruction=question['Instruction'], topic=topic)
                surveyQuestions.append(i.id)

                print('zzzzzzzzzz', q)
        print(survey)