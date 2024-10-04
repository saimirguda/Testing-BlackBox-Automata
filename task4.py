reference_log = []
customer_log = []

with open('task4-ReferenceLogs.txt', 'r') as f:
    for line in f.readlines():
        reference_log.append(line.strip())

with open('task4-CustomerLogs.txt', 'r') as f:
    for line in f.readlines():
        customer_log.append(line.strip())

# TODO
# Find the bug in the customer logs
# Learn models of both coffee machines
