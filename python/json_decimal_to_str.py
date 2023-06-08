"""
Snippet to convert decimal values in dicts recursively to string
Helps address the "Object of type Decimal is not JSON serializable"
error when using json.loads() or json.dumps() on dicts
"""

import json
from decimal import Decimal

def decimal_to_str(orig_dict):
    new_dict = { }
    for (k,v) in orig_dict.items():
        if isinstance(v, Decimal):
            new_dict[k] = str(v)
        elif isinstance(v, dict):
            new_dict[k] = decimal_to_str(v)
        else:
            new_dict[k] = v
    return new_dict
