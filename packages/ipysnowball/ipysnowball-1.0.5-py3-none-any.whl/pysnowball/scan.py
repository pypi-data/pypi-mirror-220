import time
from pysnowball import api_ref
from pysnowball import utls

def screener(current, volume, category='US', order_by='current', order='desc', page='1', size='30'):
    current_scope = f'{current}_524750'
    volume_scope = f'{volume}_223830530'
    return utls.fetch(api_ref.screener.format(category, order_by, order, page, size, current_scope, volume_scope, int(time.time()*1000)), 'xueqiu.com')