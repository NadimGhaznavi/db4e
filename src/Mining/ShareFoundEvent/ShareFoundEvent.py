"""
Mining/ShareFoundEvent/ShareFoundEvent.py

A record to store the Miner and the timestamp when the message appeared in the P2Pool log.
"""

class ShareFoundEvent():

  def __init__(self, miner, effort, difficulty, ip_addr, timestamp):
    self._miner = miner
    self._effort = effort
    self._difficulty = difficulty
    self._ip_addr = ip_addr
    self._timestamp = timestamp
    
  def __str__(self):
    return f"Share found by {self._miner} at {self._timestamp}"
  
  def miner(self, new_miner=None):
    if new_miner:
      self._miner = new_miner
    return self._miner
  
  def effort(self, new_effort=None):
    if new_effort:
      self._effort = new_effort
    return self._effort

  def difficulty(self, new_difficulty=None):
    if new_difficulty:
      self._difficulty = new_difficulty
    return self._difficulty
  
  def ip_addr(self, new_ip_addr=None):
    if new_ip_addr:
      self._ip_addr = new_ip_addr
    return self._ip_addr

  def timestamp(self, new_timestamp=None):
    if new_timestamp:
      self._timestamp = new_timestamp
    return self._timestamp

  def ip(self, new_ip=None):
    if new_ip:
      self._ip = new_ip
    return self._ip
