# from pynvml import *

# def schedule_device():
#     ''' output id of the graphic card with most free memory
#     '''
#     nvmlInit()
#     deviceCount = nvmlDeviceGetCount()
#     frees = []
#     for i in range(deviceCount):
#         handle = nvmlDeviceGetHandleByIndex(i)
#         # print("GPU", i, ":", nvmlDeviceGetName(handle))
#         info = nvmlDeviceGetMemoryInfo(handle)
#         frees.append(info.free / 1e9)
#     nvmlShutdown()
#     # print(frees)
#     id = frees.index(max(frees))
#     # print(id)
#     return id

import os
def schedule_device():
    info_per_card = os.popen('"nvidia-smi" --query-gpu=memory.total,memory.used --format=csv,nounits,noheader').read().split('\n')         # ['40536, 9948', '40536, 18191', '40536, 14492', '']

    card_memory_used = []
    for i in range(len(info_per_card)):
        if info_per_card[i] == '':
            continue
        else:
            total, used = int(info_per_card[i].split(',')[0]), int(info_per_card[i].split(',')[1])
            # print('Total GPU mem:', total, 'used:', used)
            card_memory_used.append(used)
    # print(card_memory_used.index(min(card_memory_used)))
    return int(card_memory_used.index(min(card_memory_used)))
