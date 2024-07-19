#!/usr/bin/python3
"""
scripts/db4e.py
"""
import sys
import argparse
import configparser

# Append the Infrastructure directory to the Python path
project_dirs = [ 
  "/opt/prod/db4e/src/Infrastructure", 
  "/opt/prod/db4e/src/Mining", 
  "/opt/prod/db4e/src/Reports"
]
for project_dir in project_dirs:
  sys.path.append(project_dir)

"""
Global Variables

This module uses two global variables shown below with their default
values.

* ini_file (/opt/prod/db4e/src/scripts/db4e.ini)
* environment (dev)

"""

ini_file = '/opt/prod/db4e/conf/db4e.ini'
environment = 'dev'

class Db4eStartup():

  def __init__(self):
    parser = argparse.ArgumentParser(description='db4e application')  
    parser.add_argument('-a', '--action', type=str, default=None, help='[monitor_p2pool_log|get_p2pool_xmr_payments|get_share_found_events]')
    parser.add_argument('-w', '--wallet_csv', type=str, default=None, help='Monero GUI wallet transaction data export file')
    parser.add_argument('-e', '--environ', type=str, default=environment, help='The operating environment e.g. prod, qa, dev')
    parser.add_argument('-i', '--ini_file', type=str, default=ini_file, help='Configuration file for the system')
  
    
    # Parse arguments
    args = parser.parse_args()
    self._args = args
  
    # prod, qa or dev
    environ = args.environ
    self._environ = environ

    # Action 
    self._action = args.action

    # Access the INI file 
    config = configparser.ConfigParser()
    config.read(args.ini_file)

    # Read the ini file settings
    self._storage_file = config[environ]['storage_path']
    self._p2pool_log = config[environ]['p2pool_log']
    self._db_name = config[environ]['db_name']
    self._mongodb_server = config[environ]['mongodb_server']
    self._mongodb_port = config[environ]['mongodb_port']
    self._p2pool_payouts_csv = config[environ]['p2pool_payouts_csv']
    self._wallet_csv = config[environ]['wallet_csv']
    
  def action(self):
    return self._action

  def print_status(self):
    print(f"\n---------- Db4eStartup Status -------------")
    print(f"  Config file       : {ini_file}")
    print(f"  Environment       : {self._environ}")
    print(f"  Storage file      : {self._storage_file}")
    print(f"  P2P log           : {self._p2pool_log}")
    print(f"  P2Pool payouts CSV file : {self._p2pool_payouts_csv}")
    print(f"  Mongo DB name     : {self._db_name}")
    print(f"  Mongo server host : {self._mongodb_server}")
    print(f"  Mongo server port : {self._mongodb_port}")
    print(f"  Wallet CSV file   : {self._wallet_csv}")
    
  def p2pool_log(self):
    return self._p2pool_log

  def storage_file(self):
    return self._storage_file
  
  def environ(self):
    return self._environ
  
  def db_name(self):
    return self._db_name
  
  def mongodb_server(self):
    return self._mongodb_server
  
  def mongodb_port(self):
    return int(self._mongodb_port)
  
  def p2pool_payouts_csv(self):
    return self._p2pool_payouts_csv

  def wallet_csv(self):
    return self._wallet_csv

  def args(self):
    """
    Get method.
    """
    return self._args

def main():
  startup = Db4eStartup()
  startup.print_status()

if __name__ == '__main__':
  main()