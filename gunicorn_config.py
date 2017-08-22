import multiprocessing

command = "gunicorn"
pythonpath = "/home/django/djangocms,/home/django/custom"
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
user = None
proc_name = "djangocms"

errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
accesslog = "/var/log/gunicorn/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
