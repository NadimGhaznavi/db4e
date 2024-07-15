#!/usr/bin/python3
"""
scripts/db4e.py
"""
import sys

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

# Import required db4e modules.
from P2Pool.P2Pool import P2Pool
from Db4eStartup.Db4eStartup import Db4eStartup
from Db4eApp.Db4eApp import Db4eApp
from MiningDb.MiningDb import MiningDb

def main():
  startup = Db4eStartup()
  if startup.action():
    action = startup.action()

    if action == 'monitor_p2pool_log':
      p2pool = P2Pool()
      try:
        p2pool.monitor_log()
      except KeyboardInterrupt:
        print("Exiting the P2Pool log monitoring application...")

    if action == 'get_p2pool_xmr_payments':
      miningDb = MiningDb()
      miningDb.print_p2pool_transactions()

  else:
    app = Db4eApp()
    app.menu()

if __name__ == '__main__':
  main()

