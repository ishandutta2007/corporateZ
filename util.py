#!/usr/bin/python3

from functools import reduce
from os.path import dirname, exists
from os import mkdir
try:
    from matplotlib import pyplot as plt
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)

'''
    Takes a Dict[str, model.corporateStat.Company], which is generated by
    function defined below & a targetPath on local file system ( an image of `*.png` form ),
    where to store this generated PIE chart.
'''


def plotCompanyStatusDataForAState(dataSet, targetPath):
    try:
        if(not exists(dirname(targetPath))):
            # creating target directory if not existing already
            mkdir(dirname(targetPath))
        labels = list(dataSet.keys())
        # this is the actual data to be plotted
        data = [len(v) for k, v in dataSet.items()]
        plt.pie(data, labels=labels, shadow=True,
                autopct='%1.1f%%')  # plotting pie chart
        plt.title('Status of Companies at West Bengal')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.5)  # exporting plotted PIE chart
        plt.close()  # closing this figure on which we just plotted a PIE chart
        return True
    except Exception:
        return False


'''
    Takes a generator ( generating model.corporateStat.Company as stream ) as argument
    & returns a Dict[str, model.corporateStat.Company] holding all companies of a 
    certain state, categorzied as per their status, which is to be used for plotting.
'''


def categorizeAsPerCompanyStatus(dataSet):
    return reduce(lambda acc, cur: dict([(cur.status, [cur])] + [(k, v) for k, v in acc.items()] if cur.status not in acc else ((k, [cur] + v) if k == cur.status else (k, v) for k, v in acc.items())), dataSet, {})


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
