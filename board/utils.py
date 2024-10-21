
import hashlib
import datetime

def create_id(ip_address):
    return hashlib.sha256((ip_address + str(datetime.date.today())).encode()).hexdigest()[:8]