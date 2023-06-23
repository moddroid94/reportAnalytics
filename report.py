
import datetime
import pandas as pd

class ReportScraper():
    wf = pd.read_excel('reports/26503.xlsx', index_col=0, header=6)
    #states
    pulldown = False
    idling = False
    
    defroist = False
    
    #defrost states
    defrost_temp = None
    
    #pulldown states
    pulldown_frame = {}
    begin_pulldown = None
    end_pulldown = None
    delta_t_begin = None
    delta_t_end = None
    setp = 0

    def __init__(self) -> None:
        self.loader()

    def pulldown_check(self, pull_frame):
        self.end_pulldown = list(pull_frame)[-1]
        self.begin_pulldown = list(pull_frame)[0]
        dat1 = datetime.datetime.strptime(self.begin_pulldown, "%d/%m/%Y %H:%M")
        dat2 = datetime.datetime.strptime(self.end_pulldown, "%d/%m/%Y %H:%M")
        datf = dat2 - dat1
        self.setp = int(pull_frame[self.begin_pulldown]['Setpoint 1'].split(' ')[0])

        #begin pulldown
        tmp1 = float(pull_frame[self.begin_pulldown]['Sensore T1'].split(' ')[0])
        try:
            tmp2 = float(pull_frame[self.begin_pulldown]['Sensore T2'].split(' ')[0])
        except KeyError:
            tmp2 = tmp1
        if tmp1 < tmp2:
            start_temp = tmp1
        else:
            start_temp = tmp2
        self.delta_t_begin = start_temp - self.setp

        #end pulldown
        tmp1 = float(pull_frame[self.end_pulldown]['Sensore T1'].split(' ')[0])
        try:
            tmp2 = float(pull_frame[self.end_pulldown]['Sensore T2'].split(' ')[0])
        except KeyError:
            tmp2 = tmp1
        if tmp1 < tmp2:
            end_temp = tmp1
        else:
            end_temp = tmp2
        self.delta_t_end = end_temp - self.setp

        print('date:', str(dat1).split(' ', maxsplit=1)[0],
              '\nfrom:', str(dat1).split(' ')[1],
              'to:', str(dat2).split(' ')[1],
              '\nduration:', datf,
              '\ndelta begin:', self.delta_t_begin,
              '\ndelta end:', self.delta_t_end
              )
        print('\n__\n')

    def loader(self):
        for index, row in self.wf.iterrows():

            if 'C' in row['Setpoint 1']:
                if self.pulldown is True:
                    self.pulldown_frame[index] = row.to_dict()
                    setp = int(row['Setpoint 1'].split(' ')[0])
                    tmp1 = float(row['Sensore T1'].split(' ')[0])

                    try:
                        tmp2 = float(row['Sensore T2'].split(' ')[0])
                    except KeyError:
                        tmp2 = tmp1
                    if tmp1 < tmp2:
                        temp = tmp1
                    else:
                        temp = tmp2

                    if 'Spento' in row['Modalità comp. 1']:
                        self.pulldown = False
                        self.pulldown_check(self.pulldown_frame)
                        self.pulldown_frame.clear()
                    if abs(setp-temp) < 3:
                        if row['Gruppo frigo'].find('Spento'):
                            self.pulldown = False
                            self.pulldown_check(self.pulldown_frame)
                            self.pulldown_frame.clear()
                    if 'Sbrinamento' in row['Modalità comp. 1']:
                        if self.defrost_temp is None:
                            self.defrost_temp = temp
                        else:
                            if (temp - self.defrost_temp) > 5:
                                self.pulldown = False
                                self.pulldown_check(self.pulldown_frame)
                                self.pulldown_frame.clear()
                                self.defrost_temp = None
                            else:
                                self.defrost_temp = temp
                    elif 'Idle' in row['Modalità comp. 1']:
                        self.pulldown_check(self.pulldown_frame)
                        self.pulldown_frame.clear()
                        self.pulldown = False
                        self.idling = True

                else:
                    if self.idling is True:
                        if not 'C' in row['Setpoint 1']:
                            self.idling = False
                    elif self.idling is False:

                        setp = int(row['Setpoint 1'].split(' ')[0])
                        tmp1 = float(row['Sensore T1'].split(' ')[0])

                        try:
                            tmp2 = float(row['Sensore T2'].split(' ')[0])
                        except KeyError:
                            tmp2 = tmp1

                        if tmp1 < tmp2:
                            temp = tmp1
                        else:
                            temp = tmp2

                        if setp > temp:
                            self.pulldown = False

                        elif abs(setp-temp) > 5 and 'Raffreddamento' in row['Modalità comp. 1']:
                            self.pulldown = True
                            self.pulldown_frame[index] = row.to_dict()

            elif not 'C' in row['Setpoint 1']:
                if self.pulldown is True:
                    #print(pulldown_frame)
                    self.pulldown_check(self.pulldown_frame)
                    self.pulldown_frame.clear()
                    self.pulldown = False
                else:
                    self.idling = False
                    self.pulldown = False

if __name__ =="__main__":
    ReportScraper()