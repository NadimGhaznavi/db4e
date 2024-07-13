"""
Mining/XMRTransaction/XMRTransaction.py

A record to store the transaction information for when the P2P deamon detects
a XMR payout for shares found in the PPLNS window.
"""

class XMRTransaction():

  def __init__(self, sender, receiver, amount, block_height, txid, timestamp, memo=None):
    self._sender = sender
    self._receiver = receiver
    self._amount = amount
    self._block_height = block_height
    self._memo = memo
    self._timestamp = timestamp
    self._txid = txid

  def __str__(self):
    return f"{self._timestamp} : Transaction for ({self._amount}) XMR"
  
  def amount(self, new_amount=None):
    if new_amount:
      self._amount = new_amount
    return self._amount

  def block_height(self, new_block_height=None):
    if new_block_height:
      self._block_height = new_block_height
    return self._block_height

  def memo(self, new_memo=None):
    if new_memo:
      self._memo = new_memo
    return self._memo

  def receiver(self, new_receiver=None):
    if new_receiver:
      self._receiver = new_receiver
    return self._receiver

  def sender(self, new_sender=None):
    if new_sender:
      self._sender = new_sender
    return self._sender
  
  def timestamp(self, new_timestamp=None):
    if new_timestamp:
      self._timestamp = new_timestamp
    return self._timestamp

  def txid(self, new_txid=None):
    if new_txid:
      self._txid = new_txid
    return self._txid

  