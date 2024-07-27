"""
Mining/P2Pool/P2Pool.py
"""
import os, sys
from datetime import datetime
import time
import re

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

# Import required db4e modules.
from Db4eStartup.Db4eStartup import Db4eStartup
from MiningDb.MiningDb import MiningDb
from BlockFoundEvent.BlockFoundEvent import BlockFoundEvent
from ShareFoundEvent.ShareFoundEvent import ShareFoundEvent
from XMRTransaction.XMRTransaction import XMRTransaction

class P2Pool():

  def __init__(self):
    self._name = 'P2Pool'
    self._hostname = None
    self._ip_addr = None
    self._wallet = None
    self._miners = []

    startup = Db4eStartup()
    self._p2pool_log = startup.p2pool_log()
  
  def config_menu(self):
    self._name = input("Enter a name for this P2Pool daemon: ")
    self._hostname = input("Enter the hostname where P2Pool is running: ")
    self._ip_addr = input("Enter IP address of the host where P2Pool is running: ")
    self._wallet = input("Enter the wallet def print_address for payouts:\n  ")
    self._p2pool_log = input("Enter path to P2Pool logfile: ")
  
  def monitor_log(self):
    self._log_handle = open(self._p2pool_log)
    p2log = self._log_handle
    p2log.seek(0, os.SEEK_END) # End-of-file
    print(f"Monitoring log file ({self.p2pool_log()})")
    count = 0

    db = MiningDb()

    while True:
      count = count + 1
      if count % 1000 == 0:
        time.sleep(1)
      log_line = p2log.readline()
      if not log_line:
        time.sleep(5)
        continue

      #print(f"Log   : {log_line}"[0:-1])

      ### BLOCK FOUND events
      # 2024-06-12 10:06:28.0478 P2Pool BLOCK FOUND: main chain block at height 3169541 was mined by someone else in this p2pool
      pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+P2Pool BLOCK FOUND.*$"
      match = re.search(pattern, log_line)
      if match:
        # "Block Found" event
        timestamp_str = match.group('timestamp')
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        print("Event : BLOCK FOUND EVENT")
        print(f"  P2Pool    : {self._name}")
        print(f"  Timestamp : {timestamp}")
        event = BlockFoundEvent(self._name, timestamp)
        db.add_block_found_event(event)

      ### SHARE FOUND events
      # 2024-06-19 16:32:00.5836 StratumServer SHARE FOUND: mainchain height 3174862, sidechain height 7944668, diff 107488844, client 192.168.1.5:39114, user maia, effort 37.115%
      pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+StratumServer SHARE FOUND.*mainchain height \d+, sidechain height \d+, diff (?P<difficulty>\d+), client (?P<ip_address>[^:]+):\d+, user (?P<user>\S+), effort (?P<effort>\d+\.\d+%)$"
      match = re.search(pattern, log_line)
      if match:
        # "Share Found" event
        timestamp_str = match.group('timestamp')
        try:
          timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
        except Exception as e:
          print(f"Failed to parse timestamp {timestamp_str}: {e}")
          continue

        difficulty = int(match.group('difficulty'))
        miner = match.group('user')
        effort_str = match.group('effort')

        try:
          effort = float(effort_str.rstrip('%'))  # Remove the '%' before converting to float
        except ValueError as e:
          print(f"Failed to convert effort {effort_str} to float: {e}")
          continue

        ip_addr = match.group('ip_address')

        event = ShareFoundEvent(miner, effort, difficulty, ip_addr, timestamp)
        db.add_share_found_event(event)
      
        print(f"Event : SHARE FOUND EVENT - Miner: {miner}, Effort: {effort}, Difficulty: {difficulty}, IP address: {ip_addr}, Timestamp: {timestamp}")
        event = ShareFoundEvent(miner, effort, difficulty, ip_addr, timestamp)
        db.add_share_found_event(event)

      ### XMR TRANSACTION events
      # NOTICE  2024-04-05 08:13:56.8792 P2Pool Your wallet 48wY7nYBsQNSw7v4LjoNnvCtk1Y6GLNVmePGrW82gVhYhQtWJFHi6U6G3X5d7JN2ucajU9SeBcijET8ZzKWYwC3z3Y6fDEG got a payout of 0.000474598149 XMR in block 3120548
      pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\s+P2Pool\s+Your wallet\s+(?P<wallet_address>\S+)\s+got a payout of\s+(?P<payout_amount>\d\.\d+)\s+XMR in block\s+(?P<block_height>\d+)$"
      match = re.search(pattern, log_line)

      if match:
        wallet_address = match.group('wallet_address')
        payout_amount = float(match.group('payout_amount'))
        timestamp = datetime.strptime(match.group('timestamp'), "%Y-%m-%d %H:%M:%S.%f")
        block_height = int(match.group('block_height'))
        
        print("XMR TRANSACTION FOUND")
        print(f"  Wallet       : {wallet_address[0:4]}...")
        print(f"  Amount       : {payout_amount}")
        print(f"  Block number : {block_height}")
        print(f"  Timestamp    : {timestamp}")
        
        # XMRTransaction.__init__(self, sender, receiver, amount, block_height, txid, timestamp, memo=None)
        xmr_transaction = XMRTransaction('P2Pool', wallet_address, payout_amount, block_height, '', timestamp, 'Mining')
        db.add_xmr_transaction(xmr_transaction)
      
  def p2pool_log(self):
    return self._p2pool_log

  def menu(self):
    keep_looping = True
    while keep_looping:
      print(f"---------- P2Pool Menu ------------------")
      print("  Menu options:")
      print("    1. Status")
      print("    2. Monitor P2Pool Daemon Log")
      print("    3. Configure P2Pool")
      print("    4. Exit menu")
      try:
        choice = input("enter your choice: ")
      except KeyboardInterrupt:
        choice = 4

      if choice == "1":
        self.print_status()

      elif choice == "2":
        self.monitor_log()

      elif choice == "3":
        self.config_menu()

      elif choice == "4":
        keep_looping = False

      else:
        print("Invalid choice, please try again")

  def name(self, new_name=None):
    if new_name:
      self._name = new_name
    return self._name

  def print_status(self):
    p2pool_log = self.p2pool_log()
    print(f"---------- P2Pool Status ---------------")
    print(f"  P2Pool Daemon Log: {p2pool_log}")

  
