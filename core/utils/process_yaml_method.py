from ..models import Method, Survey, Topic, DirectIndicator, IndirectIndicator

def process_yaml_method(yaml_file):
    method_instance = Method.objects.create(name='newmethod 3.0', description='A Method Description')
 
    topic_dict, topic_errors = process_topics(yaml_file['topics'], method_instance)
    indicator_errors = process_indicators(yaml_file['indicators'], topic_dict)
    survey_errors = process_surveys(yaml_file['surveys'], method_instance, topic_dict)

    errors = {'topic': topic_errors, 'indicator': indicator_errors, 'survey': survey_errors}
    errors = errors = [({x: [str(y) for y in errors[x]]}) for x in errors] # [({x : str(errors[x])}) for x in errors] # [(x, str(errors[x])) for x in errors]   #[[str(x) for x in y] for y in errors.values]
    return method_instance, errors
    

def process_topics(topics, method):
    errors = []
    topic_dict = {}


    for topic_key in topics:
        topic = topics[topic_key]
        try:
            if not 'topic' in topic.keys():
                topic_instance = Topic.objects.create(name=topic['name'], parent_topic=None, method=method)
            else:
                topic_instance = Topic.objects.create(name=topic['name'], parent_topic=topic_dict[topic['topic']], method=method)
            topic_dict[topic_key] = topic_instance
        except Exception as e:
            errors.append(e)
            break

    return topic_dict, errors


def process_indicators(indicators, topic_dict):
    errors = []
    for indicator_key in indicators:
        try:
            indicator = indicators[indicator_key]

            if indicator['type'] == 'indirectindicator':
                key = indicator_key
                name = indicator['name']
                formula = indicator['formula']
                topic = topic_dict[indicator['topic']]

                indirect_indicator_instance = IndirectIndicator.objects.create(key=key, name=name, formula=formula, topic=topic)

                if indirect_indicator_instance:
                    print(f'{indirect_indicator_instance} was created succesfully!')
        except Exception as e:
            errors.append(e)
            break

    return errors

        

def process_surveys(surveys, method, topic_dict):
    errors = []
    for survey_key in surveys:
        try:
            survey = surveys[survey_key]
            description = None

            name = survey['name']
            stakeholdergroup = survey['stakeholdergroup']
            if 'description' in survey.keys():
                description = survey['description']
            responserate = survey['responserate']

            survey_instance = Survey.objects.create(name=name, anonymous=False, method=method, description=description, rate=responserate, stakeholdergroup=stakeholdergroup)
            
            for question in survey['questions']:
                question = survey['questions'][question]

                key = question['indicator']
                topic = topic_dict[question['topic']]
                name = question['name']
                isMandatory = True if (question['isMandatory'] == 'Y') else False
                print(isMandatory)
                description = question['description']
                answertype = question['answertype']
                try:
                    options = question['options']
                except:
                    options = 0
                otheroption = question['others']

                question_instance = DirectIndicator.objects.create(key=key, topic=topic, name=name, isMandatory=isMandatory, description=description, answertype=answertype, options=options, survey=survey_instance)

        except Exception as e:
            errors.append(e)
            break

    return errors


