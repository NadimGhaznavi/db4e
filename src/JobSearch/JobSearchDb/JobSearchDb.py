"""
JobSearch/JobSearchApp/JobSearchApp.py
"""

import sys
from datetime import datetime

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
from Db4eDb.Db4eDb import Db4eDb

class JobSearchDb():

  def __init__(self):
    pass

  def add_job(self, title, company, agency, location, desc, url):
    timestamp = datetime.now()
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    new_job = {
      'doc_type' : 'job_application',
      'title' : title,
      'company' : company,
      'agency' : agency,
      'location' : location,
      'desc' : desc,
      'url' : url,
      'timestamp' : timestamp
    }
    db = self.db()
    jobs_col = db["job_search"]
    jobs_col.insert_one(new_job)

  def db(self):
    db = Db4eDb()
    return db.db()
    
  def get_jobs(self):
    db = self.db()
    jobs_col = db["job_search"]
    jobs = jobs_col.find({'doc_type': 'job_search'})
    job_count = 0
    for job in jobs:
      job_count = job_count + 1
      title = job['title']
      company = job['company']
      agency = job['agency']
      url = job['url']
      print(f"  {title} - {company} - {agency} - {url}")    
    print(f"Total: {job_count}")