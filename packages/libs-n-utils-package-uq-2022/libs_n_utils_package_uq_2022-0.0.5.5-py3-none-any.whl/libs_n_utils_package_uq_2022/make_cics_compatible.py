from .config_template import FlowMeter as FM


CIC_IDS_2018 = ['ACK Flag Cnt', 'Active Max', 'Active Mean', 'Active Min', 'Active Std', 'Attack', 'Bwd Blk Rate Avg',
                'Bwd Byts/b Avg', 'Bwd Header Len', 'Bwd IAT Max', 'Bwd IAT Mean', 'Bwd IAT Min', 'Bwd IAT Std',
                'Bwd IAT Tot', 'Bwd PSH Flags', 'Bwd Pkt Len Max', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Min',
                'Bwd Pkt Len Std', 'Bwd Pkts/b Avg', 'Bwd Pkts/s', 'Bwd Seg Size Avg', 'Bwd URG Flags',
                'CWE Flag Count', 'Down/Up Ratio', 'Dst IP', 'Dst Port', 'ECE Flag Cnt', 'FIN Flag Cnt',
                'Flow Byts/s', 'Flow Duration', 'Flow IAT Max', 'Flow IAT Mean', 'Flow IAT Min', 'Flow IAT Std',
                'Flow ID', 'Flow Pkts/s', 'Fwd Act Data Pkts', 'Fwd Blk Rate Avg', 'Fwd Byts/b Avg', 'Fwd Header Len',
                'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min', 'Fwd IAT Std', 'Fwd IAT Tot', 'Fwd PSH Flags',
                'Fwd Pkt Len Max', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Min', 'Fwd Pkt Len Std', 'Fwd Pkts/b Avg',
                'Fwd Pkts/s', 'Fwd Seg Size Avg', 'Fwd Seg Size Min', 'Fwd URG Flags', 'Idle Max', 'Idle Mean',
                'Idle Min', 'Idle Std', 'Init Bwd Win Byts', 'Init Fwd Win Byts', 'Label', 'PSH Flag Cnt',
                'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Min', 'Pkt Len Std', 'Pkt Len Var', 'Pkt Size Avg',
                'Protocol', 'RST Flag Cnt', 'SYN Flag Cnt', 'Src IP', 'Src Port', 'Subflow Bwd Byts',
                'Subflow Bwd Pkts', 'Subflow Fwd Byts', 'Subflow Fwd Pkts', 'Timestamp', 'Tot Bwd Pkts',
                'Tot Fwd Pkts', 'TotLen Bwd Pkts', 'TotLen Fwd Pkts', 'URG Flag Cnt']

CIC_BoT_IoT= ['ACK Flag Cnt', 'Active Max', 'Active Mean', 'Active Min', 'Active Std', 'Attack', 'Bwd Blk Rate Avg',
              'Bwd Byts/b Avg', 'Bwd Header Len', 'Bwd IAT Max', 'Bwd IAT Mean', 'Bwd IAT Min', 'Bwd IAT Std',
              'Bwd IAT Tot', 'Bwd PSH Flags', 'Bwd Pkt Len Max', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Min',
              'Bwd Pkt Len Std', 'Bwd Pkts/b Avg', 'Bwd Pkts/s', 'Bwd Seg Size Avg', 'Bwd URG Flags',
              'CWE Flag Count', 'Down/Up Ratio', 'Dst IP', 'Dst Port', 'ECE Flag Cnt', 'FIN Flag Cnt',
              'Flow Byts/s', 'Flow Duration', 'Flow IAT Max', 'Flow IAT Mean', 'Flow IAT Min', 'Flow IAT Std',
              'Flow ID', 'Flow Pkts/s', 'Fwd Act Data Pkts', 'Fwd Blk Rate Avg', 'Fwd Byts/b Avg', 'Fwd Header Len',
              'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min', 'Fwd IAT Std', 'Fwd IAT Tot', 'Fwd PSH Flags',
              'Fwd Pkt Len Max', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Min', 'Fwd Pkt Len Std', 'Fwd Pkts/b Avg',
              'Fwd Pkts/s', 'Fwd Seg Size Avg', 'Fwd Seg Size Min', 'Fwd URG Flags', 'Idle Max', 'Idle Mean',
              'Idle Min', 'Idle Std', 'Init Bwd Win Byts', 'Init Fwd Win Byts', 'Label', 'PSH Flag Cnt',
              'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Min', 'Pkt Len Std', 'Pkt Len Var', 'Pkt Size Avg',
              'Protocol', 'RST Flag Cnt', 'SYN Flag Cnt', 'Src IP', 'Src Port', 'Subflow Bwd Byts',
              'Subflow Bwd Pkts', 'Subflow Fwd Byts', 'Subflow Fwd Pkts', 'Timestamp', 'Tot Bwd Pkts',
              'Tot Fwd Pkts', 'TotLen Bwd Pkts', 'TotLen Fwd Pkts', 'URG Flag Cnt']


CIC_ToN_IoT = ['ACK Flag Count', 'Active Max', 'Active Mean', 'Active Min', 'Active Std', 'Attack', 'Average Packet Size', 'Bwd Bulk Rate Avg',
               'Bwd Bytes/Bulk Avg', 'Bwd Header Length', 'Bwd IAT Max', 'Bwd IAT Mean', 'Bwd IAT Min', 'Bwd IAT Std',
               'Bwd IAT Total', 'Bwd Init Win Bytes', 'Bwd PSH Flags', 'Bwd Packet Length Max', 'Bwd Packet Length Mean', 'Bwd Packet Length Min',
               'Bwd Packet Length Std', 'Bwd Packet/Bulk Avg', 'Bwd Packets/s', 'Bwd Segment Size Avg', 'Bwd URG Flags',
               'CWR Flag Count', 'Down/Up Ratio', 'Dst IP', 'Dst Port', 'ECE Flag Count', 'FIN Flag Count',
               'FWD Init Win Bytes', 'Flow Bytes/s', 'Flow Duration', 'Flow IAT Max', 'Flow IAT Mean', 'Flow IAT Min', 'Flow IAT Std',
               'Flow ID', 'Flow Packets/s', 'Fwd Act Data Pkts', 'Fwd Bulk Rate Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Header Length',
               'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min', 'Fwd IAT Std', 'Fwd IAT Total', 'Fwd PSH Flags',
               'Fwd Packet Length Max', 'Fwd Packet Length Mean', 'Fwd Packet Length Min', 'Fwd Packet Length Std', 'Fwd Packet/Bulk Avg',
               'Fwd Packets/s', 'Fwd Seg Size Min', 'Fwd Segment Size Avg', 'Fwd URG Flags', 'Idle Max', 'Idle Mean',
               'Idle Min', 'Idle Std', 'Label', 'PSH Flag Count',
               'Packet Length Max', 'Packet Length Mean', 'Packet Length Min', 'Packet Length Std', 'Packet Length Variance',
               'Protocol', 'RST Flag Count', 'SYN Flag Count', 'Src IP', 'Src Port', 'Subflow Bwd Bytes',
               'Subflow Bwd Packets', 'Subflow Fwd Bytes', 'Subflow Fwd Packets', 'Timestamp', 'Total Bwd packets',
               'Total Fwd Packet', 'Total Length of Bwd Packet', 'Total Length of Fwd Packet', 'URG Flag Count']

#~~~~~~~~~~~~~~~~~~~~***********************~~~~~~~~~~~~~~~~~~~~~
originals = FM.replace_these
to_replace = FM.columns


for n, o in enumerate(originals):
    idx = CIC_ToN_IoT.index(o)
    CIC_ToN_IoT[idx] = to_replace[n]

test2 = [1 if CIC_ToN_IoT[n] in CIC_IDS_2018 else CIC_ToN_IoT[n] for n in range(len(CIC_ToN_IoT))]
print(f'test2: \n{test2}')