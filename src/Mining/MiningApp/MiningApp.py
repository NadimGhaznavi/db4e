#!/usr/bin/python3
"""
Mining/MiningApp/MiningApp.py
"""
import sys

# Append the directories holding our code to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

from P2Pool.P2Pool import P2Pool
from MiningMongoDb.MiningMongoDb import MiningMongoDb

class MiningApp():

  def menu(self):
    keep_looping = True
    while keep_looping:
      print("\n---------- Mining Menu --------------------")
      print("  Menu options:")
      print("    (S)tatus")
      print("    (M)onitor P2Pool log")
      print("    (E)xit")
      choice = input("  Enter your choice [SME]: ")

      if choice == "M" or choice == "m":
        p2pool = P2Pool()
        p2pool.monitor_log()

      elif choice == "S" or choice == "s":
        self.print_status()

      elif choice == "E" or choice == "e":
        keep_looping = False

      else:
        print("\nInvalid choice, try again!")

  def print_status(self):
    print("\n---------- Mining App Status --------------")
    miningDb = MiningMongoDb()
    miningDb.print_status()

def main():
  mining_app = Db4eMiningApp()
  mining_app.menu()

if __name__ == '__main__':
  main()