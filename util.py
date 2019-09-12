#!/usr/bin/python3

from functools import reduce
from os.path import dirname, exists
from os import mkdir
from time import localtime, time
try:
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)

'''
    Takes a Dict[str, int], which is generated by function(s) defined below 
    ( categorizes company dataset, for a certain State in India, using various parameters )
    & a targetPath on local file system ( an image of `*.png` form ),
    where to store this generated PIE chart.
'''


def plotCategorizedCompanyDataForACertainState(dataSet, targetPath, title):
    try:
        if(not exists(dirname(targetPath))):
            # creating target directory if not existing already
            mkdir(dirname(targetPath))
        font = {
            'family': 'serif',
            'color': '#264040',
            'weight': 'normal',
            'size': 12
        }
        labels = sorted(dataSet, key=lambda elem:
                        dataSet[elem], reverse=True)
        # this is the actual data to be plotted
        data = [dataSet[i] for i in labels]
        # figure on which pie chart to be drawn ( of size 2400x1200 )
        plt.figure(figsize=(24, 12), dpi=100)
        patches, _ = plt.pie(data)  # plotting pie chart
        plt.legend(patches, labels, loc='best', fontsize='medium')
        plt.title(title, fontdict=font)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.5)  # exporting plotted PIE chart
        plt.close()  # closing this figure on which we just plotted a PIE chart
        return True
    except Exception:
        return False


'''
    Takes a list of all companies present in one State ( instances of model.corporateStat.Company )
    as argument & returns a Dict[str, int] holding count of all companies of a
    certain state, categorzied as per their STATUS, which is to be used for plotting a PIE chart.
'''


def categorizeAsPerCompanyStatus(dataSet):
    return reduce(lambda acc, cur: dict([(cur.status, 1)] + [(k, v) for k, v in acc.items()]) if cur.status not in acc else dict(((k, v + 1) if k == cur.status else (k, v) for k, v in acc.items())), dataSet, {})


'''
    Takes a list of all companies present in one State ( instances of model.corporateStat.Company )
    as argument & returns a Dict[str, int] holding count of all companies of a
    certain state, categorzied as per their CLASS, which is to be used for plotting a PIE chart.
'''


def categorizeAsPerCompanyClass(dataSet):
    return reduce(lambda acc, cur: dict([(cur.companyClass, 1)] + [(k, v) for k, v in acc.items()]) if cur.companyClass not in acc else dict(((k, v + 1) if k == cur.companyClass else (k, v) for k, v in acc.items())), dataSet, {})


'''
    Takes a list of all companies present in one State ( instances of model.corporateStat.Company )
    as argument & returns a Dict[str, int] holding count of all companies of a
    certain state, categorzied as per their CATEGORY, which is to be used for plotting a PIE chart.
'''


def categorizeAsPerCompanyCategory(dataSet):
    return reduce(lambda acc, cur: dict([(cur.category, 1)] + [(k, v) for k, v in acc.items()]) if cur.category not in acc else dict(((k, v + 1) if k == cur.category else (k, v) for k, v in acc.items())), dataSet, {})


'''
    Takes a list of all companies present in one State ( instances of model.corporateStat.Company )
    as argument & returns a Dict[str, int] holding count of all companies of a
    certain state, categorzied as per their SUB_CATEGORY, which is to be used for plotting a PIE chart.
'''


def categorizeAsPerCompanySubCategory(dataSet):
    return reduce(lambda acc, cur: dict([(cur.subCategory, 1)] + [(k, v) for k, v in acc.items()]) if cur.subCategory not in acc else dict(((k, v + 1) if k == cur.subCategory else (k, v) for k, v in acc.items())), dataSet, {})


'''
    Takes a list of all companies present in one State ( instances of model.corporateStat.Company )
    as argument & returns a Dict[str, int] holding count of all companies of a
    certain state, categorzied as per their PRINCIPAL_BUSINESS_ACTIVITY, which is to be used for plotting a PIE chart.
'''


def categorizeAsPerCompanyPrincipalBusinessActivity(dataSet):
    return reduce(lambda acc, cur: dict([(cur.principalBusinessActivity, 1)] + [(k, v) for k, v in acc.items()]) if cur.principalBusinessActivity not in acc else dict(((k, v + 1) if k == cur.principalBusinessActivity else (k, v) for k, v in acc.items())), dataSet, {})


'''
    Plots a graph of year of registration vs. #-of companies registered
    in that certain year, while using dataset obtained from function defined just below it.
'''


def plotCompanyRegistrationDateWiseCategorizedData(dataSet, targetPath, title):
    try:
        if(not exists(dirname(targetPath))):
            # creating target directory if not existing already
            mkdir(dirname(targetPath))
        # style `ggplot` is in use
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'color': '#264040',
                'weight': 'normal',
                'size': 12
            }
            # a range from `first when a company was registered` to `nearest year upto which we have any status`
            # filtering out improper years ( may be higher than current year ), lets us clean dataset, so that things go smooth
            x = range(min(dataSet), max(
                filter(lambda v: v < (localtime(time()).tm_year + 1), dataSet)) + 1)
            y = [dataSet.get(i, 0) for i in x]
            plt.figure(figsize=(24, 12), dpi=100)
            # creating major x-tick locator every 10 years
            plt.gca().xaxis.set_major_locator(MultipleLocator(10))
            # creating x-tick formatter using only year name
            plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%d'))
            # setting minor x-tick locator every 1 year
            plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
            plt.plot(x, y, 'r-', lw=1.5)
            plt.xlabel('Year', fontdict=font, labelpad=16)
            plt.ylabel('# of Companies Registered', fontdict=font, labelpad=16)
            plt.title(title, fontdict=font)
            plt.savefig(targetPath, bbox_inches='tight', pad_inches=.5)
            plt.close()
        return True
    except Exception:
        return False


'''
    Filters out those companies which has `dateOfRegistration` field None
    & classifies remaining ones using year of registration

    So finally we get a Dict[int, int], holding a mapping between
    year of registration & #-of companies registered in that year,
    which is going to be used by above function for plotting a graph.
'''


def categorizeAsPerCompanyDateOfRegistration(dataSet):
    return reduce(lambda acc, cur: dict([(cur.dateOfRegistration.year, 1)] + [(k, v) for k, v in acc.items()]) if cur.dateOfRegistration.year not in acc else dict(((k, v + 1) if k == cur.dateOfRegistration.year else (k, v) for k, v in acc.items())),
                  filter(lambda v: v.dateOfRegistration is not None, dataSet), {})


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
