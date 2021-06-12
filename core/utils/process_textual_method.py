from ..models import Method, Survey, Topic, DirectIndicator, IndirectIndicator
import re

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
        #if re.search('^Topics:', entry):
            method_instance = process_method(processor(index), uploader)

        if entry.startswith('Indicators:'):
        #if re.search('^Indicators:', entry):
            topic_dict = process_topics(processor(index), method_instance)

        if entry.startswith('Surveys:'):
        #if re.search('^Surveys:', entry):
            process_indicators(processor(index), topic_dict)


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

            if key in result[-1] and key in ['Indicator_id', 'topic_id']:
                result.append({})

            if key == 'Answer_options':
                result[-1][key] = [{}]
                continue
            
            if key in ['Order', 'Text']:
                if key in result[-1]['Answer_options'][-1]:
                    result[-1]['Answer_options'].append({})
                result[-1]['Answer_options'][-1][key] = value
            
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

        topic_dict[topic['topic_id']] = topic_instance	# has to be topic_instance
        print(topic_instance.__dict__)

        
    #Topic.objects.filter(method__name='newmethod2').delete()
    #Method.objects.filter(name="newmethod2").delete()
    #method_instance.delete()
    print(topic_dict)
    #print('==', topics)
    return topic_dict

def process_indicators(indicators, topic_dict): #topic_dict
    for indicator in indicators:
        if indicator['Indicator_type'] == 'Direct':
            DI = DirectIndicator.objects.create(name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['topic']], pre_unit=indicator.get('PreUnit'), post_unit=indicator.get('PostUnit'), datatype=indicator['DataType']) # DataType=indicator['DataType']
        if indicator['Indicator_type'] == 'Indirect':
            II = IndirectIndicator.objects.create(name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['topic']], formula=indicator['formula'], PreUnit=indicator.get('PreUnit'), PostUnit=indicator.get('PostUnit'), type=indicator.get('Type')) # DataType=indicator['DataType']

    #print('**', indicators)
