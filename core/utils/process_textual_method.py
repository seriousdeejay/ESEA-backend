from ..models import Method, Survey, Topic, DirectIndicator, IndirectIndicator
import re

def process_file():
	global start
	global myList

	start = 0
	myList = []

	with open('newMethod2.txt', 'r') as fp:

		for line in fp:
			line = line.strip()
			if line[:2] != '//' and len(line):
				myList.append(line)

		for index, entry in enumerate(myList):
			if re.search('^Topics:', entry):
				method_instance = process_method(processor(index))

			if re.search('^Indicators:', entry):
				topic_dict = process_topics(processor(index), method_instance)

			if re.search('^Surveys:', entry):
				process_indicators(processor(index), topic_dict)

def processor(index):
	Info = []
	subList = []

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

	globals()['start'] = index


	return Info

def process_method(M):
	isPublic = M['isPublic'] == 'true'	# Could use eval('True') If the Boolean string is capitalised
	Version = float(M['Version'])
	method_instance = Method.objects.create(name=M['Name'], description=M['Description'], ispublic=isPublic, version=Version)
	print('++', M)
	return method_instance


def process_topics(topics, method_instance):
	topic_dict = {}

	for topic in topics:
		# if 'Parent_topic' in topic.keys():
		topic_instance = Topic.objects.create(name=topic['Name'], description=topic['Description'], parent_topic=topic.get('Parent_topic'), method=method_instance)
		#	pass
		# else:
		# 	topic_instance = Topic.objects.create(name=topic['Name'], description=topic['Description'], parent_topic=None, method=method_instance)
		# 	pass
		topic_dict[topic['topic_id']] = topic_instance	# has to be topic_instance
	print(topic_dict)
	print('==', topics)
	return topic_dict

def process_indicators(indicators, topic_dict): #topic_dict
	for indicator in indicators:
		if indicator['Indicator_type'] == 'Direct':
			DI = DirectIndicator.objects.create(name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['topic']] pre_unit=indicator.get('PreUnit'), post_unit=indicator.get('PostUnit')) # DataType=indicator['DataType']

		if indicator['Indicator_type'] == 'Indirect':
			II = IndirectIndicator.objects.create(name=indicator['Name'], description=indicator['Description'], topic=topic_dict[indicator['topic']], formula=indicator['formula'], PreUnit=indicator.get('PreUnit'), PostUnit=indicator.get('PostUnit'), type=indicator.get('Type')) # DataType=indicator['DataType']
	print('**', indicators)
