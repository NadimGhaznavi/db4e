#!/usr/bin/python3
"""
Mining/MiningDb/MiningDb.py
"""
import csv
import sys
from datetime import datetime, timedelta

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/db4e/src/Infrastructure", 
  "/opt/db4e/src/Mining", 
  "/opt/db4e/src/Reports"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

# Import required db4e modules.
from Db4eDb.Db4eDb import Db4eDb
from BlockFoundEvent.BlockFoundEvent import BlockFoundEvent
from ShareFoundEvent.ShareFoundEvent import ShareFoundEvent
from XMRTransaction.XMRTransaction import XMRTransaction

class MiningDb():

  def add_block_found_event(self, block_found_event):
    pool_name = block_found_event.pool_name()
    timestamp = block_found_event.timestamp()
    new_event = {
      'doc_type' : 'block_found_event',
      'p2pool' : pool_name,
      'timestamp' : timestamp
    }
    self.insert_uniq_one(new_event)

  def add_share_found_event(self, share_found_event):
    miner = share_found_event.miner()
    effort = share_found_event.effort()
    difficulty = share_found_event.difficulty()
    ip_addr = share_found_event.ip_addr()
    timestamp = share_found_event.timestamp()
    new_event = {
      'doc_type' : 'share_found_event',
      'miner' : miner,
      'effort' : effort,
      'difficulty' : difficulty,
      'ip_addr' : ip_addr,
      'timestamp' : timestamp
    }
    self.insert_uniq_one(new_event)

  def add_xmr_transaction(self, xmr_transaction):
    sender = xmr_transaction.sender()
    receiver = xmr_transaction.receiver()
    amount = xmr_transaction.amount()
    block_height = xmr_transaction.block_height()
    memo = xmr_transaction.memo()
    timestamp = xmr_transaction.timestamp()
    new_transaction = {
      'doc_type' : 'xmr_transaction',
      'sender' : sender,
      'receiver' : receiver,
      'amount' : amount,
      'block_height' : block_height,
      'memo' : memo,
      'timestamp' : timestamp
    }
    self.insert_uniq_one(new_transaction)
  
  def db(self):
    db = Db4eDb()
    return db.db()

  def get_events(self, event_type):
    db = self.db()
    mining_col = db['mining']
    events = mining_col.find({'doc_type': event_type})
    return events
  
  def get_wallet_balance(self):
    db = self.db()
    mining_col = db['mining']
    balance = mining_col.find_one({'doc_type': 'wallet_balance'})
    if not balance:
      balance = {
        'doc_type': 'wallet_balance',
        'balance': 0
      }
      mining_col.insert_one(balance)
    return balance['balance']
  
  def get_num_events(self, event_type):
    return len(self.get_events(event_type))

  def insert_uniq_one(self, new_event):
    db = self.db()
    mining_col = db['mining']
    timestamp = new_event['timestamp']
    if not mining_col.find_one({'timestamp': timestamp}):
      mining_col.insert_one(new_event)

  def print_block_found_events(self):
    events = self.get_events('block_found_event')
    # Sort events by timestamp
    events = sorted(events, key=lambda event: event['timestamp'])

    print(f"-- Block Found Events ---------------------")
    block_count = 0
    for event in events:
      block_count = block_count + 1
      p2pool = event['p2pool']
      timestamp = event['timestamp']
      print(f"{timestamp} : {p2pool}")
    print(f"Total number of records ({block_count})")

  def print_p2pool_transactions(self):
    events = self.get_events('xmr_transaction')
    # Sort events by timestamp
    events = sorted(events, key=lambda event: event['timestamp'])

    print(f"-- XMR Transactions -----------------------")
    xmr_count = 0
    total_amount = 0
    for event in events:
      xmr_count = xmr_count + 1
      sender = event['sender']
      receiver = event['receiver'][0:6] 
      amount = round(event['amount'], 6)
      memo = event['memo']
      timestamp = event['timestamp']
      print(f"{timestamp} : From ({sender}) To ({receiver}...) Amount ({amount}) Memo ({memo})")
      total_amount = total_amount + amount
    print(f"Total number of records ({xmr_count})")
    print(f"           Total amount ({round(total_amount, 6)})")

  def print_share_found_events(self):
    events = self.get_events('share_found_event')
    # Sort events by timestamp
    events = sorted(events, key=lambda event: event['timestamp'])

    print(f"-- Share Found Events ---------------------")
    share_count = 0
    for event in events:
      share_count = share_count + 1
      miner = event['miner']
      difficulty = event['difficulty']
      ip_addr = event['ip_addr']
      timestamp = event['timestamp']
      print(f"{timestamp} : Miner {miner} Difficulty ({difficulty}) IP Address ({ip_addr})") 
    print(f"Total number of records ({share_count})")

  def print_status(self):
    print("---------- MiningDb Status ----------------")

    events = self.get_events('xmr_transaction')
    print(f"-- XMR Transactions -----------------------")
    xmr_count = 0
    for event in events:
      xmr_count = xmr_count + 1
      sender = event['sender']
      receiver = event['receiver'][0:6]
      amount = round(event['amount'], 6)
      memo = event['memo']
      timestamp = event['timestamp']
      print(f"{timestamp} : From ({sender}) To ({receiver}) Amount ({amount}) Memo ({memo})")
    print(f"Total number of records ({xmr_count})")

    events = self.get_events('share_found_event')
    #print(f"-- Share Found Events ({len(events)})")
    print(f"-- Share Found Events ---------------------")
    share_count = 0
    for event in events:
      share_count = share_count + 1
      miner = event['miner']
      effort = event['effort']
      difficulty = event['difficulty']
      ip_addr = event['ip_addr']
      timestamp = event['timestamp']
      print(f"{timestamp} : Miner ({miner}) Effort ({effort}) Difficulty ({difficulty}) IP Address ({ip_addr}))")
    print(f"Total number of records ({share_count})")

    events = self.get_events('block_found_event')
    #print(f"-- Block Found Events ({len(events)})")
    print(f"-- Block Found Events ---------------------")
    block_count = 0
    for event in events:
      block_count = block_count + 1
      p2pool = event['p2pool']
      timestamp = event['timestamp']
      print(f"{timestamp} : P2Pool ({p2pool})")
    print(f"Total number of records ({block_count})")

    print("-- Wallet Balance -------------------------")
    balance = self.get_wallet_balance()
    print("  Balance : {balance}")
    
    print("-------------------------------------------")
    print("Total number of records:\n")
    print(f"  XMR Transactions   : {xmr_count}")
    print(f"  Block Found Events : {block_count}")
    print(f"  Share Found Events : {share_count}")
    print(f"\n               Total : {xmr_count + block_count + share_count}")

  def add_to_wallet_balance(self, amount):
    db = self.db()
    mining_col = db['mining']

    balance = mining_col.find_one_and_update(
      {'doc_type': 'wallet_balance'},
      {'$inc': {'balance': amount}}
    )

    if not balance:
      raise Exception("Wallet balance document not found")

    return balance['balance']


def main():
  db4e = Db4eRoot()
  db = db4e.db()
  mining = Db4eMining(db)
  mining.print_status()

if __name__ == '__main__':
    main()