import time
from pysnowball import api_ref
from pysnowball import utls

def screener(current, volume, category='US', order_by='current', order='desc', page='1', size='30'):
    return utls.fetch(api_ref.screener.format(category, order_by, order, page, size, current, volume, int(time.time()*1000)))