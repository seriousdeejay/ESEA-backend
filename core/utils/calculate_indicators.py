from typing import Dict, List
from ..models import DirectIndicator, IndirectIndicator
from ..classes import Indicator

def calculate_indicators(direct_indicators) -> Dict[str, Indicator]:
    indicators = {}

    for direct_indicator in direct_indicators:
        indicators[direct_indicator.key] = direct_indicator.value
        #for response in direct_indicator.responses:
            # print(response.all())
        #indicators[direct_indicator.key] = direct_indicator.responses
    return indicators

def calculate_indicators(indirect_indicators: List[IndirectIndicator], direct_indicators: List[DirectIndicator],) -> Dict[str, Indicator]:
    indicators = merge_indicators(indirect_indicators, direct_indicators)
 
    for indicator in indicators.values():
        calculate_indicator(indicator, indicators)
    
    #print(type(indicators))
    for indicator in indicators.values():
        if indicator.value is None:
            # print(indicator.key, ':', indicator.value)
            # print('dat kan toch nie!')
            calculate_indicator(indicator, indicators)

    return indicators


def calculate_indicator(indicator, value_list) -> str:
    if indicator.value:
        return indicator.value
    if not len(indicator.calculation_keys):
        return indicator.calculate()
    else:
        values = {}
        for calculation_key in indicator.calculation_keys:
            child_indicator = value_list[calculation_key]
            values[child_indicator.key] = calculate_indicator(
                child_indicator, value_list
            )
        indicator.find_values(values)
        return indicator.calculate()


def map_responses_by_indicator(direct_indicators, question_responses) -> None:
    for direct_indicator in direct_indicators:
        direct_indicator.filter_responses(question_responses)



# TODO: Remove function when direct and indirect indicators are merged.
def merge_indicators(
    indirect_indicators: List[IndirectIndicator],
    direct_indicators: List[DirectIndicator],
) -> Dict[str, Indicator]:
    indicators = {}

    for indirect_indicator in indirect_indicators:
        indicators[indirect_indicator.key] = indirect_indicator

    for direct_indicator in direct_indicators:
        indicators[direct_indicator.key] = direct_indicator

    return indicators