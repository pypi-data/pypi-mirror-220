import sys
import os

# 将项目根目录（pysnowball）添加到Python搜索路径中
sys.path.remove(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pysnowball.token import set_token
from pysnowball.scan import screener


# 主函数       
if __name__ == '__main__':
	set_token('23b8a762a65329ac5f454fc18dae4c1d44006cfe')
	response_list = screener(15, 2000000)
	# print('response_list', response_list)