#!/usr/bin/python3
"""
Infrastructure/Db4eApp/Db4eApp.py
"""

import sys

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports",
  "/opt/prod/db4e/src/JobSearch"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

# Import required db4e modules.
from Db4eStartup.Db4eStartup import Db4eStartup
from Db4eDb.Db4eDb import Db4eDb
from MiningApp.MiningApp import MiningApp
from JobSearchApp.JobSearchApp import JobSearchApp

class Db4eApp():
  def __init__(self):
    pass

  def menu(self):
    keep_looping = True
    while keep_looping:
      print("\n---------- App Menu -----------------------")
      print("  Menu options:")
      print("    1. Status")
      print("    2. Mining Menu")
      print("    3. Job Search Menu")
      print("    4. Exit")
      try:
        choice = input("  Enter your choice: ")
      except KeyboardInterrupt:
        print("Exiting the Database 4 Everything...")
  
      if choice == "1":
        startup = Db4eStartup()
        startup.print_status()
        db = Db4eDb()
        db.print_status()
       
      elif choice == "2":
        mining_app = MiningApp()
        mining_app.menu()
      
      elif choice == "3":
        job_app = JobSearchApp()
        job_app.menu()

      elif choice == "4" or choice == "X" or choice == "x":
        keep_looping = False

      else:
        print("Invalid choice, try again")
    
  
def main():
  app = Db4eApp()
  app.menu()
  

if __name__ == '__main__':
  main()