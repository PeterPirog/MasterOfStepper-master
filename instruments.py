
import pyvisa
import numpy as np
import pandas as pd



class KeithleyCard():
    def __init__(self, visa_adres='GPIB0::16::INSTR',channels=None):
        self.visa_adres=visa_adres

        if channels is None:
            self.channels=np.array([*range(10)])+1
        else:
            self.channels=np.array(channels)

        self.measurements={'Time':[]}


        for chanel in self.channels:
            self.measurements.update({'chan{}'.format(str(chanel)):[]})


        self.rm = pyvisa.ResourceManager()
        print('Znaleziono zasoby: ',self.rm.list_resources())
        try:
            self.inst = self.rm.open_resource(self.visa_adres)
            print('Połaczono z przyrządem: ',self.inst.query("*IDN?"))
        except:
            print('Nie znaleziono przyrządu sprawdź poprawnośc połączenia interfejsów i adresowania')
        self.inst.write('*RST')
        self.inst.write('SYST:PRES')
        self.inst.write('FUNC "FRES"')
        self.inst.write('FRES:RANG 100')


        self.inst.write('Trig:sour IMM')
        self.inst.query('*OPC?')
        self.inst.write('TRIG:TIM 0')
        self.inst.query('*OPC?')


        self.inst.query('*OPC?')



    def meas(self,number_of_measurements):

        for i in range(number_of_measurements):
            self.measurements['Time'].append(str(i))
            for chanel in self.channels:
                chan_str=str(chanel)
                self.inst.write("ROUT:CLOS (@{})".format(chan_str))

                self.inst.query('*OPC?')
                meas=self.inst.query("MEAS?")
                meas=np.float(meas)
                self.measurements['chan'+chan_str].append(meas)


                print('Pomiar na kanale {}='.format(chan_str), meas)

        self.export_mesurements()

    def export_mesurements(self,xlsx_file="output.xlsx"):
        self.xlxs_file=xlsx_file
        df = pd.DataFrame.from_dict(self.measurements, orient="columns")
        df.to_excel(self.xlxs_file)
        return df

card=KeithleyCard(channels=[1,2,9])
card.meas(3)
pd=card.export_mesurements()
print(pd)