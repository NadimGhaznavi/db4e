#!/usr/bin/python3
"""
Charts/P2poolPayouts/P2PoolPayouts.py
"""
import sys

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports",
  "/opt/prod/db4e/src/Charts"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

# Import required db4e modules.
from Db4eStartup.Db4eStartup import Db4eStartup
from ChartsDb.ChartsDb import ChartsDb

class P2PoolPayouts():

  def __init__(self):
    startup = Db4eStartup()
    self._payouts_csv = startup.p2pool_payouts_csv()

  def generate_csv(self):
    db = ChartsDb()
    payouts = db.get_p2pool_payouts()
    
    print(f"FOO payouts")
    print(f"{payouts}")
    rows = []
    rows.append('Date,Total')
    for payout in payouts:
      timestamp = payout.timestamp()
      amount = payout.amount()
      rows.append[str(timestamp) + ',' + str(amount)]
    print(rows)


def main():
  p2pool_chart = P2PoolPayouts()
  p2pool_chart.generate_csv()

if __name__ == '__main__':
  main()