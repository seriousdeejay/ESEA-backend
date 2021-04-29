from typing import List, Optional


class Indicator:
    id: int
    name: Optional[str]
    key: str
    description: Optional[str]
    formula: Optional[str]
    calculation: Optional[str]
    value: str
    responses: Optional[List[str]]

    def __init__(
        self,
        id: int,
        name: Optional[str],
        key: str,
        description: Optional[str],
        formula: Optional[str],
        calculation: Optional[str],
        value: str,
        responses: Optional[List[str]],
    ):
        self.id = id
        self.name = name 
        self.key = key
        self.description = description
        self.formula = formula
        self.calculation = calculation
        self.value = value