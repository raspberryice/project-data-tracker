from pdt.models import *

def render_graph(devsession_list,remsession_list):
    dev = []
    rem = []
    ret = []
    for session in devsession_list:
        entry = [session.start_date.date(), session.SLOC]
        dev.append(entry)
    for session in remsession_list:
        entry = [session.start_date.date(), session.defectno]
        rem.append(entry)
    # combine two lists
    dev.sort(key=lambda e: e[0])# sort by date
    rem.sort(key=lambda e: e[0])

    i,j=0,0
    cur_date = min(rem[0][0], dev[0][0])
    last_date = max(rem[-1][0],dev[-1][0])
    while cur_date <= last_date:
        sloc,defect =0,0
        while i < len(dev) and dev[i][0] == cur_date:
            sloc += dev[i][1]
            i+=1
        while j <len(rem) and rem[j][0] == cur_date:
            defect += rem[j][1]
            j+=1
        entry = [cur_date.strftime('%Y-%m-%d'),sloc,defect]
        if len(ret) != 0:
            entry[1] += ret[-1][1]
            entry[2] += ret[-1][2]
        ret.append(entry)
        if i == len(dev):
            if j == len(rem):
                break
            else:
                cur_date = rem[j][0]
        elif j == len(rem):
            cur_date = dev[i][0]
        else:
            cur_date = min(dev[i][0],rem[j][0])
    return ret

l1 = SLOCSession.objects.filter(iteration__phase__project = 1)
l2 = DefectSession.objects.filter(iteration__phase__project =1)


