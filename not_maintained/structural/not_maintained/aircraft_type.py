import pandas as pd
def type():
    my_value = False
    new_aircrafts = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx",sheet_name='New Data Entry')
    babikian = pd.read_excel(r"C:\Users\PRohr\Desktop\Masterarbeit\Data\Aircraft Databank v2.xlsx",sheet_name='Data Table')
    # Data retrieved by me from Janes all Aircrafts and Manufacturers website.
    babikian = babikian.loc[babikian['Babikian'] == 'Yes']
    if my_value:
        babikian = babikian[['Name', 'YOI', 'Exit Limit', 'OEW', 'MTOW', 'Type', 'MZFW']]
        babikian['OEW/MTOW'] = babikian['OEW'] / babikian['MTOW']
    else:
        babikian = babikian[['Name', 'YOI', 'Exit Limit', 'OEW/MTOW', 'OEW', 'Type', 'MZFW']]
    babikian['OEW/Pax'] = babikian['OEW'] / babikian['Exit Limit']
    new_aircrafts = new_aircrafts.groupby(['Name', 'Type'], as_index=False).agg(
        {'OEW': 'mean', 'MTOW': 'mean', 'Exit Limit': 'mean', 'YOI': 'mean', 'Range': 'mean', 'MZFW':'mean'})
    new_aircrafts['OEW/Pax'] = new_aircrafts['OEW'] / new_aircrafts['Exit Limit']
    new_aircrafts['OEW/MTOW'] = new_aircrafts['OEW'] / new_aircrafts['MTOW']
    new_aircrafts = new_aircrafts.append(babikian)
    #new_aircrafts = new_aircrafts.dropna(subset='OEW/MTOW')

    new_aircrafts.loc[new_aircrafts['Exit Limit'] < 100, 'Type'] = 'Regional'

    return(new_aircrafts)