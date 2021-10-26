"""
Load IRQ to CSV from TXT
"""

import re

import pandas as pd

with open("affordances/data/irq.txt") as f:
    irq = f.readlines()

rows = []

for l in irq:
    match = re.search("([^0]+) ([0-9/.]+) ([0-9/.]+) ([0-9/.]+) ([0-9/.]+)", l)
    rows.append(list(match.groups()))


df = pd.DataFrame(rows)

df.columns = ["Sentence", "Visual", "Verbal", "Orthographic", "Manipulation"]

df.to_csv("affordances/data/irq.csv")