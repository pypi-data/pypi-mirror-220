from pathlib import Path

# printtime = 3612.094839593339
# printtime_div_ms = divmod(printtime, 60)
# printtime_div_hm = divmod(printtime_div_ms[0], 60)
# printtime_div = (printtime_div_hm[0], printtime_div_hm[1], printtime_div_ms[1])
# printtime_str = ("{0:.0f}h {1:.0f}m {2:.2f}s".format(*printtime_div))
# # printtime_str = str(printtime_div[0]) + "h " + str(printtime_div[1]) + str("m ") + str(printtime_div[2]) + str("s")
# print(printtime_str)

nrm_delay = 0.0
inv_delay = 0.0

with open('test/nrm.txt', 'r') as f:
    for l_no, line in enumerate(f):
        nrm_delay += float(line)

with open('test/inv.txt', 'r') as f:
    for l_no, line in enumerate(f):
        inv_delay += float(line)

print('norm: ' + str(nrm_delay))
print('inv: ' + str(inv_delay))