""" 
Snippet to group a list of dictionaries based on values for one or more keys
"""

import itertools
from operator import itemgetter

test_list = [
            {'metric': 'metricA', 'metric_group': 'metricGroupA', 'metric_owner': 'abc'}, 
            {'metric': 'metricB', 'metric_group': 'metricGroupA', 'metric_owner': 'abc'},
            {'metric': 'metricC', 'metric_group': 'metricGroupB', 'metric_owner': 'abc'},
            {'metric': 'metricD', 'metric_group': 'metricGroupB', 'metric_owner': 'abc'},
            {'metric': 'metricE', 'metric_group': 'metricGroupA', 'metric_owner': 'xyz'},
            {'metric': 'metricF', 'metric_group': 'metricGroupA', 'metric_owner': 'xyz'},
            {'metric': 'metricG', 'metric_group': 'metricGroupB', 'metric_owner': 'xyz'},
            ]

sorted_list = sorted(test_list, key=itemgetter('metric_owner','metric_group'))

for group_key, grouped_dict in itertools.groupby(sorted_list, key=itemgetter('metric_owner','metric_group')):
    # group_key will have the values by which the dictionaries are grouped
    #  grouped_dict will be the dictionaries belonging to a particular group
    print(str(group_key),list(grouped_dict))