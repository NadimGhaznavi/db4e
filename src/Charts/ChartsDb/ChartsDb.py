#!/usr/bin/python3
"""
Charts/ChartsDb/ChartsDb.py
"""
import sys
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

class ChartsDb():

  def db(self):
    db = Db4eDb()
    return db.db()
  
  def get_p2pool_payouts(self):
    db = self.db()
    mining_col = db['mining']
    payouts = mining_col.find({'doc_type': 'xmr_transaction'})
    #sorted_payouts = sorted(payouts, key=lambda event: event['timestamp'])
    #print(sorted_payouts)
    xmr_transactions = []
    for payout in payouts:
      sender = payout['sender']
      receiver = payout['receiver']
      amount = payout['amount']
      block_height = payout['block_height']
      memo = payout['memo']
      timestamp = payout['timestamp']
      xmr_transaction = XMRTransaction(sender, receiver, amount, block_height, '', timestamp, memo)
      xmr_transactions.append(xmr_transaction)
    print(f"ChartsDb:get_p2pool_payouts()")
    print(xmr_transactions)
    return xmr_transactions