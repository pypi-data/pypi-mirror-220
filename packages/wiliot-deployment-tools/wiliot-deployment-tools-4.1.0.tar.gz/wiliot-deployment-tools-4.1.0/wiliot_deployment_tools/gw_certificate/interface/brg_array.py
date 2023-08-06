from wiliot_deployment_tools.gw_certificate.interface.pkt_generator import PktGenerator
import random
import numpy as np

class BrgArray:
    def __init__(self, num_brgs=3):
        assert num_brgs > 1, 'BrgArray cannot be smaller than 1!'
        self.brg_list = [PktGenerator() for brg in range(num_brgs)]
        self.primary_brg = self.brg_list[0]
        self.secondary_brgs = self.brg_list[1:]
    
    def get_new_pkt_pairs(self) -> list:
        pkts = []
        new_pkt_primary = self.primary_brg.get_new_packet_pair()
        pkts.append(new_pkt_primary)
        for brg in self.secondary_brgs:
            brg.generate_si_from_pkt_id(self.primary_brg.pkt_id_int)
            brg.randomize_rssi_nfpkt()
            brg.data_packet = new_pkt_primary['data_packet']
            pkts.append(brg.get_existing_packet_pair())
        for idx, pkt in enumerate(pkts):
            pkt.update({'bridge_id': self.brg_list[idx].bridge_id})
        return pkts
    
    def get_scattered_pkt_pairs(self, delay):
        assert delay / len(self.brg_list) >= 10, 'Cannos get scattered PKT pairs for parameters! decrease num of brgs or increase delay'
        start_times = sorted(random.sample(list(np.arange(0, delay-10+1, 10)), k=len(self.brg_list)))
        start_times.append((start_times[0] + delay))
        pkts = self.get_new_pkt_pairs()
        
        for idx, pkt in enumerate(pkts):
            # minimum time between UART packet commands = 10ms
            pkt['time_delay'] = max(start_times[idx+1] - start_times[idx], 10)
        return pkts