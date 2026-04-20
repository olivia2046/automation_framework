# -*- coding: utf-8 -*-
'''
@author: olivia.dou
Created on: 2026/4/20 14:51
desc: to be added in jenkins job, to calculate test result
'''

import json
import os

# Define the path to the Allure summary file(**** to be executed from project root folder ****)
summary_file = "testreport/allure-report/widgets/summary.json"

# Open the summary file and load the data
with open(summary_file, 'r') as f:
    summary_data = json.load(f)

# Extract the values from the JSON
test_count = summary_data['statistic']['total']
passed_tests = summary_data['statistic']['passed']
failed_tests = summary_data['statistic']['failed']
skipped_tests = summary_data['statistic']['skipped']
duration = summary_data['time']['duration']

# Print the results (for debugging)
print(f"Total Tests: {test_count}")
print(f"Tests Passed: {passed_tests}")
print(f"Tests Failed: {failed_tests}")
print(f"Tests Skipped: {skipped_tests}")
print(f"Total Duration: {duration}")

# Set environment variables for Jenkins
os.environ['TEST_COUNT'] = str(test_count)
os.environ['PASSED_TESTS'] = str(passed_tests)
os.environ['FAILED_TESTS'] = str(failed_tests)
os.environ['SKIPPED_TESTS'] = str(skipped_tests)
os.environ['DURATION'] = str(duration)