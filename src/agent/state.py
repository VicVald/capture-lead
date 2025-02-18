from typing import List, TypedDict

class AgentState(TypedDict):
    niche: str
    locations: List[str]
    limit_per_location: int
    role: str
    online_appearance: List[dict]
    final_sheet: List[dict]