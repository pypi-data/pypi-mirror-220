
class NetFlow_v2:
    columns = ['IPV4_SRC_ADDR', 'L4_SRC_PORT', 'IPV4_DST_ADDR', 'L4_DST_PORT',
       'PROTOCOL', 'L7_PROTO', 'IN_BYTES', 'IN_PKTS', 'OUT_BYTES', 'OUT_PKTS',
       'TCP_FLAGS', 'CLIENT_TCP_FLAGS', 'SERVER_TCP_FLAGS',
       'FLOW_DURATION_MILLISECONDS', 'DURATION_IN', 'DURATION_OUT', 'MIN_TTL',
       'MAX_TTL', 'LONGEST_FLOW_PKT', 'SHORTEST_FLOW_PKT', 'MIN_IP_PKT_LEN',
       'MAX_IP_PKT_LEN', 'SRC_TO_DST_SECOND_BYTES', 'DST_TO_SRC_SECOND_BYTES',
       'RETRANSMITTED_IN_BYTES', 'RETRANSMITTED_IN_PKTS',
       'RETRANSMITTED_OUT_BYTES', 'RETRANSMITTED_OUT_PKTS',
       'SRC_TO_DST_AVG_THROUGHPUT', 'DST_TO_SRC_AVG_THROUGHPUT',
       'NUM_PKTS_UP_TO_128_BYTES', 'NUM_PKTS_128_TO_256_BYTES',
       'NUM_PKTS_256_TO_512_BYTES', 'NUM_PKTS_512_TO_1024_BYTES',
       'NUM_PKTS_1024_TO_1514_BYTES', 'TCP_WIN_MAX_IN', 'TCP_WIN_MAX_OUT',
       'ICMP_TYPE', 'ICMP_IPV4_TYPE', 'DNS_QUERY_ID', 'DNS_QUERY_TYPE',
       'DNS_TTL_ANSWER', 'FTP_COMMAND_RET_CODE', 'Attack', 'Label']

    flow_identifiers = ['IPV4_SRC_ADDR', 'IPV4_DST_ADDR', 'L4_SRC_PORT','L4_DST_PORT']

    top_features = ['DST_TO_SRC_AVG_THROUGHPUT', 'DURATION_IN', 'TCP_WIN_MAX_IN',
                    'MAX_TTL', 'L7_PROTO', 'MIN_IP_PKT_LEN']

    top_features_3class = ['DURATION_IN', 'DST_TO_SRC_AVG_THROUGHPUT', 'FLOW_DURATION_MILLISECONDS',
                           'MIN_IP_PKT_LEN', 'TCP_WIN_MAX_IN', 'OUT_PKTS',]


class FlowMeter:
    # these are columns or fields expected to be in all FlowMeter files
    columns = ['ACK Flag Cnt', 'Active Max', 'Active Mean', 'Active Min', 'Active Std', 'Attack', 'Pkt Size Avg',
               'Bwd Blk Rate Avg', 'Bwd Byts/b Avg', 'Bwd Header Len', 'Bwd IAT Max', 'Bwd IAT Mean', 'Bwd IAT Min',
               'Bwd IAT Std', 'Bwd IAT Tot', 'Init Bwd Win Byts', 'Bwd PSH Flags', 'Bwd Pkt Len Max',
               'Bwd Pkt Len Mean', 'Bwd Pkt Len Min', 'Bwd Pkt Len Std', 'Bwd Pkts/b Avg', 'Bwd Pkts/s',
               'Bwd Seg Size Avg', 'Bwd URG Flags', 'CWE Flag Count', 'Down/Up Ratio', 'Dst IP', 'Dst Port',
               'ECE Flag Cnt', 'FIN Flag Cnt', 'Init Fwd Win Byts', 'Flow Byts/s', 'Flow Duration', 'Flow IAT Max',
               'Flow IAT Mean', 'Flow IAT Min', 'Flow IAT Std', 'Flow ID', 'Flow Pkts/s', 'Fwd Act Data Pkts',
               'Fwd Blk Rate Avg', 'Fwd Byts/b Avg', 'Fwd Header Len', 'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min',
               'Fwd IAT Std', 'Fwd IAT Tot', 'Fwd PSH Flags', 'Fwd Pkt Len Max', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Min',
               'Fwd Pkt Len Std', 'Fwd Pkts/b Avg', 'Fwd Pkts/s', 'Fwd Seg Size Min', 'Fwd Seg Size Avg',
               'Fwd URG Flags', 'Idle Max', 'Idle Mean', 'Idle Min', 'Idle Std', 'Label', 'PSH Flag Cnt',
               'Pkt Len Max', 'Pkt Len Mean', 'Pkt Len Min', 'Pkt Len Std', 'Pkt Len Var', 'Protocol',
               'RST Flag Cnt', 'SYN Flag Cnt', 'Src IP', 'Src Port', 'Subflow Bwd Byts', 'Subflow Bwd Pkts',
               'Subflow Fwd Byts', 'Subflow Fwd Pkts', 'Timestamp', 'Tot Bwd Pkts', 'Tot Fwd Pkts',
               'TotLen Bwd Pkts', 'TotLen Fwd Pkts', 'URG Flag Cnt']

    # if these fields are in rw_ls dataset, they should be replaced with above fields i.e. columns
    replace_these = ['ACK Flag Count', 'Active Max', 'Active Mean', 'Active Min', 'Active Std', 'Attack',
                     'Average Packet Size', 'Bwd Bulk Rate Avg', 'Bwd Bytes/Bulk Avg', 'Bwd Header Length',
                     'Bwd IAT Max', 'Bwd IAT Mean', 'Bwd IAT Min', 'Bwd IAT Std', 'Bwd IAT Total',
                     'Bwd Init Win Bytes', 'Bwd PSH Flags', 'Bwd Packet Length Max', 'Bwd Packet Length Mean',
                     'Bwd Packet Length Min', 'Bwd Packet Length Std', 'Bwd Packet/Bulk Avg', 'Bwd Packets/s',
                     'Bwd Segment Size Avg', 'Bwd URG Flags', 'CWR Flag Count', 'Down/Up Ratio', 'Dst IP', 'Dst Port',
                     'ECE Flag Count', 'FIN Flag Count', 'FWD Init Win Bytes', 'Flow Bytes/s', 'Flow Duration',
                     'Flow IAT Max', 'Flow IAT Mean', 'Flow IAT Min', 'Flow IAT Std', 'Flow ID', 'Flow Packets/s',
                     'Fwd Act Data Pkts', 'Fwd Bulk Rate Avg', 'Fwd Bytes/Bulk Avg', 'Fwd Header Length',
                     'Fwd IAT Max', 'Fwd IAT Mean', 'Fwd IAT Min', 'Fwd IAT Std', 'Fwd IAT Total', 'Fwd PSH Flags',
                     'Fwd Packet Length Max', 'Fwd Packet Length Mean', 'Fwd Packet Length Min',
                     'Fwd Packet Length Std', 'Fwd Packet/Bulk Avg', 'Fwd Packets/s', 'Fwd Seg Size Min',
                     'Fwd Segment Size Avg', 'Fwd URG Flags', 'Idle Max', 'Idle Mean', 'Idle Min', 'Idle Std', 'Label',
                     'PSH Flag Count', 'Packet Length Max', 'Packet Length Mean', 'Packet Length Min',
                     'Packet Length Std', 'Packet Length Variance', 'Protocol', 'RST Flag Count', 'SYN Flag Count',
                     'Src IP', 'Src Port', 'Subflow Bwd Bytes', 'Subflow Bwd Packets', 'Subflow Fwd Bytes',
                     'Subflow Fwd Packets', 'Timestamp', 'Total Bwd packets', 'Total Fwd Packet',
                     'Total Length of Bwd Packet', 'Total Length of Fwd Packet', 'URG Flag Count']

    flow_identifiers = ['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Src Port', 'Dst Port']

    top_features = ['Init Fwd Win Byts', 'Fwd Header Len', 'Fwd Seg Size Min',
                    'Init Bwd Win Byts', 'Bwd Header Len', 'Subflow Fwd Pkts']

    top_features_3class = ['Init Fwd Win Byts', 'Fwd Seg Size Min', 'Idle Max',
                    'Subflow Fwd Pkts', 'Fwd Header Len', 'Idle Mean']

class NN:
    n_nodes = 10
    n_layers = 5
    n_epochs = 100
    seeds = 0
    batch_size = 1000
    N_fold = 5
    learning_rate = 0.00001
    dropout_value = 0.2
    validation_split = 0.3
    frac = 1_000_000

    body_colors = ["#0000ff", "#0f0f0f"]
    hatch = ['//', '\\']



class color_params:
    dataset_color_hatch = {'NFv2-BoT_IoT': ['#9A6324', '|..|'], 'NFv2-CIC_2018': ['#e6194B', 'x+'],
                           'NFv2-ToN_IoT': ['#bfef45', '.---..'], 'NFv2-UNSW_NB15': ['#800000', 'xx'],
                           'FWM-BoT_IoT': ["#9A6324", 'x-'], 'FWM-CIC_2018': ["#e6194B", '++'],
                           'FWM-ToN_IoT': ["#bfef45", '|xx|'], 'NFv2-BoT_IoT-CIC_2018': ['#911eb4', '.x..'],
                           'NFv2-BoT_IoT-ToN_IoT': ['#00aa00', '|*|'], 'NFv2-BoT_IoT-UNSW_NB15': ['#4363d8', '.+'],
                           'NFv2-CIC_2018-ToN_IoT': ['#000075', '*'], 'NFv2-CIC_2018-UNSW_NB15': ['#808000', '...o'],
                           'NFv2-ToN_IoT-UNSW_NB15': ['#111111', '-//-'], 'FWM-BoT_IoT-CIC_2018': ["#911eb4", 'x|'],
                           'FWM-BoT_IoT-ToN_IoT': ["#00aa00", '....'], 'FWM-CIC_2018-ToN_IoT': ["#000075", 'O'],
                           'NFv2-BoT_IoT-CIC_2018-ToN_IoT': ['#ffd8b1', 'oo'],
                           'NFv2-BoT_IoT-CIC_2018-UNSW_NB15': ['#42d4f4', 'Oo'],
                           'NFv2-BoT_IoT-ToN_IoT-UNSW_NB15': ['#f032e6', 'xxx'],
                           'NFv2-CIC_2018-ToN_IoT-UNSW_NB15': ['#c98369', '+++'],
                           'NFv2-CIC_2018-UNSW-NB15': ['#808000', '...o']
                           }

    reserved_colors = ["#3cb44b", '#f58231', '#fffac8'
                       '#469990', '#fabed4', '#aaffc3',
                       '#ffe119', '#dcbeff', '#42d4f4']




class ElasticServer:
    ip = '192.168.20.18'
    port = 5609
    index = 'nprobe-2017.07.29'
    index_type = '_doc'
    url = f'http://{ip}:{port}'


class CSV:
    selected_columns = ['FIRST_SWITCHED', 'LAST_SWITCHED', 'FLOW_ID', 'IN_BYTES', 'IN_PKTS',
                        'IPV4_DST_ADDR', 'IPV4_SRC_ADDR', 'L4_DST_PORT',
                        'L4_SRC_PORT', 'L7_PROTO', 'OUT_BYTES',
                        'OUT_PKTS', 'PROTOCOL', 'SRC_TOS', 'SRC_VLAN', 'L7_PROTO_NAME']



class features:
    groupby_features = ['nL7_per_srcPORT', 'nL7_per_dstPORT', 'nL7_per_srcIP', 'nL7_per_dstIP',
                        'ndstIP_per_dstPORT', 'ndstIP_per_srcPORT', 'ndstIP_per_srcIP',
                        'nsrcIP_per_dstPORT', 'nsrcIP_per_srcPORT', 'nsrcIP_per_dstIP',
                        'ndstPORT_per_dstIP', 'ndstPORT_per_srcIP', 'ndstPORT_per_srcPORT',
                        'nsrcPORT_per_dstIP', 'nsrcPORT_per_srcIP', 'nsrcPORT_per_dstPORT',
                        ]

    non_groupby_features = [
        'flow_duration',
        'Total_packet',
        'IN_packet_size',
        'OUT_packet_size',
        'Total_packet_size',
        'avg_Total_packet_duration',
        'Total_flow_size',
        'packet_symmetry'
    ]

    def feature_fields(self, feature_):
        f0 = f1 = 0
        if feature_ == 'nL7_per_srcPORT':
            f0 = 6
            f1 = 7
        elif feature_ == 'nL7_per_dstPORT':
            f0 = 5
            f1 = 7
        elif feature_ == 'nL7_per_srcIP':
            f0 = 4
            f1 = 7
        elif feature_ == 'nL7_per_dstIP':
            f0 = 3
            f1 = 7
        elif feature_ == 'ndstIP_per_dstPORT':
            f0 = 5
            f1 = 3
        elif feature_ == 'ndstIP_per_srcPORT':
            f0 = 6
            f1 = 3
        elif feature_ == 'ndstIP_per_srcIP':
            f0 = 4
            f1 = 3
        elif feature_ == 'nsrcIP_per_dstPORT':
            f0 = 5
            f1 = 4
        elif feature_ == 'nsrcIP_per_srcPORT':
            f0 = 6
            f1 = 4
        elif feature_ == 'nsrcIP_per_dstIP':
            f0 = 3
            f1 = 4
        elif feature_ == 'ndstPORT_per_dstIP':
            f0 = 3
            f1 = 5
        elif feature_ == 'ndstPORT_per_srcIP':
            f0 = 4
            f1 = 5
        elif feature_ == 'ndstPORT_per_srcPORT':
            f0 = 6
            f1 = 5
        elif feature_ == 'nsrcPORT_per_dstIP':
            f0 = 3
            f1 = 6
        elif feature_ == 'nsrcPORT_per_srcIP':
            f0 = 4
            f1 = 6
        elif feature_ == 'nsrcPORT_per_dstPORT':
            f0 = 5
            f1 = 6
        elif feature_ == 'flow_duration':
            f0 = 0
            f1 = 8
        elif feature_ == 'Total_packet':
            f0 = 2
            f1 = 10
        elif feature_ == 'IN_packet_size':
            f0 = 2
            f1 = 1
        elif feature_ == 'OUT_packet_size':
            f0 = 10
            f1 = 9
        elif feature_ == 'Total_packet_size':
            f0 = [2, 10]
            f1 = [1, 9]
        elif feature_ == 'avg_Total_packet_duration':
            f0 = [2, 10]
            f1 = [0, 8]
        elif feature_ == 'Total_flow_size':
            f0 = 1
            f1 = 9
        elif feature_ == 'packet_symmetry':
            f0 = 10
            f1 = 2

        return f0, f1




class NetFlow_fields:
    fields = ['FIRST_SWITCHED',
              'IN_BYTES',
              'IN_PKTS',
              'IPV4_DST_ADDR',
              'IPV4_SRC_ADDR',
              'L4_DST_PORT',
              'L4_SRC_PORT',
              'L7_PROTO_NAME',
              'LAST_SWITCHED',
              'OUT_BYTES',
              'OUT_PKTS',
              'PROTOCOL']

    def field_numbers(self):
        self.nob = self.fields.index('OUT_BYTES')
        self.nop = self.fields.index('OUT_PKTS')
        self.nib = self.fields.index('IN_BYTES')
        self.nip = self.fields.index('IN_PKTS')
        self.nfs = self.fields.index('FIRST_SWITCHED')
        self.nls = self.fields.index('LAST_SWITCHED')
        self.nl7 = self.fields.index('L7_PROTO_NAME')
        self.nsi = self.fields.index('IPV4_SRC_ADDR')
        self.ndi = self.fields.index('IPV4_DST_ADDR')
        self.nsp = self.fields.index('L4_SRC_PORT')
        self.ndp = self.fields.index('L4_DST_PORT')
        self.npo = self.fields.index('PROTOCOL')
        return self.nob, self.nop, self.nib, self.nip, self.nfs, self.nls, \
               self.nl7, self.nsi, self.ndi, self.nsp, self.ndp, self.npo

    def selected_cols(self, feature_name):
        if feature_name == 'Total_flow_size':
            return [self.nib, self.nob, self.nip, self.nop]
        if feature_name == 'flow_duration':
            return [self.nfs, self.nls]
        if feature_name == 'Total_packet_size':
            return [self.nib, self.nob, self.nip, self.nop]
        if feature_name == 'flow_size_symmetry':
            return [self.nib, self.nob, self.nip, self.nop]
        if feature_name == 'avg_Total_packet_duration':
            return [self.nfs, self.nls, self.nip, self.nop]
        if feature_name == 'packet_symmetry':
            return [self.nib, self.nob, self.nip, self.nop]
        if feature_name == 'nsrcIP_per_dstIP':
            return [self.nsi, self.ndi]
        if feature_name == 'ndstPORT_per_srcIP':
            return [self.nsi, self.ndp]
        if feature_name == 'ndstPORT_per_dstIP':
            return [self.ndp, self.ndi]
        if feature_name == 'nsrcPORT_per_srcIP':
            return [self.nsp, self.nsi]
        if feature_name == 'nsrcPORT_per_dstIP':
            return [self.nsp, self.ndi]
        if feature_name == 'ndstPORT_per_srcPORT':
            return [self.ndp, self.nsp]
        if feature_name == 'nsrcPORT_per_dstPORT':
            return [self.nsp, self.ndp]
        if feature_name == 'ndstIP_per_srcIP':
            return [self.ndi, self.nsi]
        if feature_name == 'nsrcIP_per_dstIP':
            return [self.nsi, self.ndi]
        if feature_name == 'ndstIP_per_srcPORT':
            return [self.ndi, self.nsp]
        if feature_name == 'ndstIP_per_dstPORT':
            return [self.ndi, self.ndp]
        if feature_name == 'nsrcIP_per_srcPORT':
            return [self.nsi, self.nsp]
        if feature_name == 'nsrcIP_per_dstPORT':
            return [self.nsi, self.ndp]
        if feature_name == 'nL7_per_srcIP':
            return [self.nl7, self.nsi]
        if feature_name == 'nL7_per_dstIP':
            return [self.nl7, self.ndi]
        if feature_name == 'nL7_per_srcPORT':
            return [self.nl7, self.nsp]
        if feature_name == 'nL7_per_dstPORT':
            return [self.nl7, self.ndp]






class UNSW_NB15:
    fields = ['Stime', 'dbytes', 'Dpkts', 'dstip', 'srcip', 'dsport', 'sport',
              'service', 'Ltime', 'sbytes', 'Spkts', 'proto', 'dur']
    dtype_dic = {'Stime':int, 'dbytes':int, 'Dpkts':int, 'dstip':str, 'srcip':str,
                 'dsport':int, 'sport':int, 'service':str, 'Ltime':int, 'sbytes':int,
                 'Spkts':int,  'proto':str,  'dur':float}

    def field_numbers(self):
        nob = self.fields.index('sbytes')
        nop = self.fields.index('Spkts')
        nib = self.fields.index('dbytes')
        nip = self.fields.index('Dpkts')
        nfs = self.fields.index('Stime')
        nls = self.fields.index('Ltime')
        nl7 = self.fields.index('service')
        nsi = self.fields.index('srcip')
        ndi = self.fields.index('dstip')
        nsp = self.fields.index('sport')
        ndp = self.fields.index('dsport')
        npo = self.fields.index('proto')
        ndu = self.fields.index('dur')
        return nob, nop, nib, nip, nfs, nls, nl7, nsi, ndi, nsp, ndp, npo, ndu

    remaining_fields = ['state', 'dur','sttl', 'dttl', 'sloss', 'dloss',
    'Spkts', 'Dpkts', 'swin', 'dwin', 'stcpb', 'dtcpb', 'smeansz','Dload',
    'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'service',
    'Ltime', 'Sintpkt', 'Dintpkt', 'tcprtt', 'synack', 'ackdat','Sload',
    'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login',
    'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm',
    'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'attack_cat',
    'Label']

class plot_parameters:
    distinct_colors_22 = ['#4363d8', '#e6194b', '#3cb44b', '#ffe119', '#f58231',
                          '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe',
                          '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000',
                          '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080',
                          '#ffffff', '#000000']
    dataset_colors = {
        'CIC': '#ff0040',
        'ton_iot': '#ff8000',
        'UNSW_NB15': '#ff4000',
        'Comscentre2017': '#0080ff',
        'UQ_2019_03_13': '#00bfff'
    }

    dataset_facecolors = {
        'CIC': '#ff0040',
        'ton_iot': '#ff8000',
        'UNSW_NB15': '#ff4000',
        'Comscentre2017': 'none',
        'UQ_2019_03_13': 'none'
    }

    dataset_edgecolors = {
        'CIC': 'none',
        'ton_iot': '#ff8000',
        'UNSW_NB15': 'none',
        'Comscentre2017': '#0080ff',
        'UQ_2019_03_13': '#00bfff'
    }


    dataset_shorts = {
        'CIC': 'CIC_IDS',
        'ton_iot': 'TON_IOT',
        'UNSW_NB15': 'UNSW_NB15',
        'Comscentre2017': 'ISP',
        'UQ_2019_03_13': 'UQ'
    }

    dataset_markers = {
        'CIC': '+',
        'ton_iot': '.',
        'UNSW_NB15': 'x',
        'Comscentre2017': 'o',
        'UQ_2019_03_13': 'P'
    }

    bxplot_params_dic = {
        'Total_flow_size': {
            'title_text': 'Total Flow Size',
            'ylabel': 'Flow Size (Byte)'
        },
        'OUT_flow_size': {
            'title_text': 'Outward Flow Size',
            'ylabel': 'Flow Size (Byte)'
        },
        'IN_flow_size': {
            'title_text': 'INward Flow Size',
            'ylabel': 'Flow Size (Byte)'
        },
        'flow_duration': {
            'title_text': 'Flow Duration Distribution',
            'ylabel': 'Flow Duration (Sec)'
        },
        'flow_size_symmetry': {
            'title_text': 'Flow Size Symmetry ',
            'ylabel': 'log((in_byte+1)/(out_bytes+1))'
        },
        'IN_packet_size': {
            'title_text': 'In-ward Packet Size',
            'ylabel': 'Packet Size (Byte)'
        },
        'OUT_packet_size': {
            'title_text': 'Out-ward Packet Size',
            'ylabel': 'Packet Size (Byte)'
        },
        'Total_packet_size': {
            'title_text': 'Total Packet Size',
            'ylabel': 'Packet Size (Byte)'
        },
        'ndstIP_per_srcIP':{
            'title_text': 'Number of '
                          'dest IPs per source IP',
            'ylabel': 'Number dest IPs per Source IP'
        },
        'ndstPORT_per_srcIP': {
            'title_text': 'Number of '
                          'destination Ports per source IP',
            'ylabel': 'Number of dest Ports per Source IP'
        },
        'nL7_per_srcIP': {
            'title_text': 'Number of '
                          'L7-Protocols used by rw_ls Source IP Address ',
            'ylabel': 'Number of L7-Protos per Source IP'
        },
        'nL7_per_dstIP': {
            'title_text': 'Number of '
                          'L7-Protocols used by rw_ls Destination IP Address ',
            'ylabel': 'Number of L7-Protos per Dest IP'
        },
        'nL7_per_srcPORT': {
            'title_text': 'Number of '
                          'L7-Protocols with rw_ls Source PORT ',
            'ylabel': 'Number of L7-Protocols'
        },
        'nL7_per_dstPORT': {
            'title_text': 'Number of '
                          'L7-Protocols with rw_ls Destination PORT ',
            'ylabel': 'Number of L7-Protos Dest Port'
        },
        'nsrcPORT_per_srcIP': {
            'title_text': 'Number of '
                          'source Ports per source IP',
            'ylabel': 'Number of Source Ports per Source IP'
        },
        'nsrcPORT_per_dstIP': {
            'title_text': 'Number of '
                          'source Ports per destination IP',
            'ylabel': 'Number of source Ports per Dest IP'
        },
        'ndstPORT_per_dstIP': {
            'title_text': 'Number of '
                          'destination Ports per destination IP',
            'ylabel': 'Number of dest Ports per Dest IP'
        },
        'nTpackets_per_flow': {
            'title_text': 'Number of Total'
                          'Packets per flow',
            'ylabel': 'Number of Packets per Flow'
        },
        'nOpackets_per_flow': {
            'title_text': 'Number of Outward'
                          'Packets per flow',
            'ylabel': 'Number of Packets per Flow'
        },
        'nIpackets_per_flow': {
            'title_text': 'Number of INward'
                          'Packets per flow',
            'ylabel': 'Number of Packets per Flow'
        },
        'avg_Total_packet_duration': {
            'title_text': 'Averaged Total Packet Duration (time)',
            'ylabel': 'Packet Duration (Sec)'
        },
        'packet_symmetry': {
            'title_text': 'Packet Symmetry',
            'ylabel': 'log(IN_PKTS+1/OUT_PKTS+1)'
        },
        'nsrcIP_per_dstIP': {
            'title_text': 'Number of '
                          'Source IPs per destination IP',
            'ylabel': 'Number of Source Ips per Dest IP'
        },
        'nsrcIP_per_srcPORT': {
            'title_text': 'Number of '
                          'Source IPs using rw_ls Source Port',
            'ylabel': 'Number of Source Ips per Source Port'
        },
        'nsrcIP_per_dstPORT': {
            'title_text': 'Number of '
                          'Source IPs using rw_ls Destination Port',
            'ylabel': 'Number of Source Ips per Dest Port'
        },
        'ndstIP_per_srcPORT': {
            'title_text': 'Number of '
                          'Destination IPs using rw_ls Source Port',
            'ylabel': 'Number of Dest Ips per Source Port'
        },
        'ndstIP_per_dstPORT': {
            'title_text': 'Number of '
                          'Destination IPs using rw_ls Destination Port',
            'ylabel': 'Number of dest Ips per Dest Port'
        },
        'nsrcPORT_per_dstPORT': {
            'title_text': 'Number of '
                          'Source Ports Contacted rw_ls Destination Port',
            'ylabel': 'Number of Source Ports per Dest Port'
        },
        'ndstPORT_per_srcPORT': {
            'title_text': 'Number of '
                          'Destination Ports Contacted by rw_ls Source Port',
            'ylabel': 'Number of Dest Ports per Source Port'
        },
    }

    CDFplot_params_dic = {
        'Total_flow_size': {
            'xlabel': 'Flow Size (Byte)'
        },
        'OUT_BYTES': {
            'xlabel': 'Flow Size (Byte)'
        },
        'IN_BYTES': {
            'xlabel': 'Flow Size (Byte)'
        },
        'sbytes': {
            'xlabel': 'Flow Size (Byte)'
        },
        'dbytes': {
            'xlabel': 'Flow Size (Byte)'
        },
        'flow_duration': {
            'xlabel': 'Flow Duration (Sec)'
        },
        'flow_size_symmetry': {
            'xlabel': 'log(in_byte+1/out_bytes+1)'
        },
        'packet_symmetry': {
            'xlabel': 'log(IN_PKTS+1/OUT_PKTS+1)'
        },
        'IN_packet_size': {
            'xlabel': 'Packet Size (Byte)'
        },
        'OUT_packet_size': {
            'xlabel': 'Packet Size (Byte)'
        },
        'Total_packet_size': {
            'xlabel': 'Packet Size (Byte)'
        },
        'Total_packet': {
            'xlabel': 'Number of Total Packets in Flow'
        },
        'ndstIP_per_srcIP':{
            'xlabel': 'Number of Dest Ips per Source IP'
        },
        'ndstPORT_per_srcIP': {
            'xlabel': 'Number of Dest Ports per Source IP'
        },
        'nL7_per_srcIP': {
            'xlabel': 'Number of L7-Protos per Source IP'
        },
        'nL7_per_dstIP': {
            'xlabel': 'Number of L7-Protos per Dest IP'
        },
        'nL7_per_srcPORT': {
            'xlabel': 'Number of L7-Protos per Source Port'
        },
        'nL7_per_dstPORT': {
            'xlabel': 'Number of L7-Protos per Dest Port'
        },
        'nsrcPORT_per_srcIP': {
            'xlabel': 'Number of Source Ports per Source IP'
        },
        'nsrcPORT_per_dstIP': {
            'xlabel': 'Number of Source Ports per Dest IP'
        },
        'ndstPORT_per_dstIP': {
            'xlabel': 'Number of Dest Ports per Dest IP'
        },
        'nTpackets_per_flow': {
            'xlabel': 'Number of Total Packets per Flow'
        },
        'nOpackets_per_flow': {
            'xlabel': 'Number of Out Packets per Flow'
        },
        'avg_Total_packet_duration': {
            'xlabel': '(average) Packet Time (sec)'
        },
        'nsrcIP_per_dstIP': {
            'xlabel': 'Number of Source IPs per Dest IP'
        },
        'nsrcIP_per_srcPORT': {
            'xlabel': 'Number of Source IPs per Source Port'
        },
        'nsrcIP_per_dstPORT': {
            'xlabel': 'Number of Source IPs per Dest Port'
        },
        'ndstIP_per_srcPORT': {
            'xlabel': 'Number of Dest IPs per Source Port'
        },
        'ndstIP_per_dstPORT': {
            'xlabel': 'Number of Dest IPs per Dest Port'
        },
        'nsrcPORT_per_dstPORT': {
            'xlabel': 'Number of Source Ports per Dest Port'
        },
        'ndstPORT_per_srcPORT': {
            'xlabel': 'Number of Dest Ports per Source Port'
        },
    }


class dataset_info:
    dataset_fields = {
        'BoT_IoT': ['DoS', 'DDoS', 'Reconnaissance', 'Benign', 'Theft'],
        'CIC_2018': ['SSH-Bruteforce', 'Benign', 'DDoS attacks-LOIC-HTTP', 'DDOS attack-HOIC',
                                  'DoS attacks-Slowloris', 'DoS attacks-Hulk', 'FTP-BruteForce',
                                  'Infilteration', 'Bot', 'DoS attacks-GoldenEye', 'Brute Force -Web',
                                  'DoS attacks-SlowHTTPTest', 'SQL Injection', 'DDOS attack-LOIC-UDP',
                                  'Brute Force -XSS'],
        'UNSW_NB15': ['Benign', 'Exploits', 'Generic', 'Fuzzers', 'Backdoor', 'DoS',
                                  'Reconnaissance', 'Shellcode', 'Worms', 'Analysis'],
        'ToN_IoT': ['ransomware', 'Benign', 'xss', 'scanning', 'password', 'dos', 'ddos',
                                'injection', 'mitm', 'backdoor']
    }

