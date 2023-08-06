import pandas as pd
import os
import _pickle as pickle

# save_fldr = '/home/nids1/Desktop/ZSL_visualizations/NetFlow/alternate_feature_wasserstein/'
save_fldr = '/home/nids1/Desktop/ZSL_visualizations/original_ds/'

name = 'UNSW_NB15_unity_feature_importance_weight.pickle'

rows = ['Analysis', 'Backdoor', 'DoS', 'Exploits', 'Fuzzers',
        'Generic', 'Reconnaissance', 'Shellcode', 'Worms',
        'all_classes']

NF_columns = ['CLIENT_TCP_FLAGS', 'DNS_QUERY_ID', 'DNS_QUERY_TYPE', 'DNS_TTL_ANSWER', 'DST_TO_SRC_AVG_THROUGHPUT',
              'DST_TO_SRC_SECOND_BYTES', 'DURATION_IN', 'DURATION_OUT', 'FLOW_DURATION_MILLISECONDS',
              'FTP_COMMAND_RET_CODE', 'ICMP_IPV4_TYPE', 'ICMP_TYPE', 'IN_BYTES', 'IN_PKTS', 'L7_PROTO',
              'LONGEST_FLOW_PKT', 'MAX_IP_PKT_LEN', 'MAX_TTL', 'MIN_IP_PKT_LEN', 'MIN_TTL',
              'NUM_PKTS_1024_TO_1514_BYTES', 'NUM_PKTS_128_TO_256_BYTES', 'NUM_PKTS_256_TO_512_BYTES',
              'NUM_PKTS_512_TO_1024_BYTES', 'NUM_PKTS_UP_TO_128_BYTES', 'OUT_BYTES', 'OUT_PKTS', 'PROTOCOL',
              'RETRANSMITTED_IN_BYTES', 'RETRANSMITTED_IN_PKTS', 'RETRANSMITTED_OUT_BYTES', 'RETRANSMITTED_OUT_PKTS',
              'SERVER_TCP_FLAGS', 'SHORTEST_FLOW_PKT', 'SRC_TO_DST_AVG_THROUGHPUT', 'SRC_TO_DST_SECOND_BYTES',
              'TCP_FLAGS', 'TCP_WIN_MAX_IN', 'TCP_WIN_MAX_OUT']


UNSW_NB15_columns = ['Dintpkt', 'Djit', 'Dload', 'Dpkts', 'Ltime', 'Sintpkt', 'Sjit',
       'Sload', 'Spkts', 'Stime', 'ackdat', 'c_proto', 'c_service', 'c_state',
       'ct_dst_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'ct_flw_http_mthd',
       'ct_ftp_cmd', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_srv_dst',
       'ct_srv_src', 'ct_state_ttl', 'dbytes', 'dloss', 'dmeansz', 'dtcpb',
       'dttl', 'dur', 'dwin', 'is_ftp_login', 'is_sm_ips_ports', 'res_bdy_len',
       'sbytes', 'sloss', 'smeansz', 'stcpb', 'sttl', 'swin', 'synack',
       'tcprtt', 'trans_depth']



df = pd.DataFrame(1, columns=UNSW_NB15_columns, index=rows)
addr = os.path.join(save_fldr, name)

with open(addr, 'wb') as f:
    pickle.dump(df, f, protocol=-1)


