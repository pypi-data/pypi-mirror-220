import datetime
import time
import pandas as pd
import tabulate
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI, TIMESTAMP
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.interface import packet_error
from wiliot_deployment_tools.gw_certificate.interface import mqtt
from wiliot_deployment_tools.gw_certificate.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.gw_certificate.interface.brg_array import BrgArray
from wiliot_deployment_tools.gw_certificate.interface.if_defines import BRIDGES, DEFAULT_DELAY, DEFAULT_OUTPUT_POWER, DUPLICATIONS, MAX_NFPKT, MAX_RSSI, SEP, TIME_DELAYS
from wiliot_deployment_tools.gw_certificate.interface.mqtt import MqttClient
from wiliot_deployment_tools.gw_certificate.interface.pkt_generator import PktGenerator
from wiliot_deployment_tools.gw_certificate.tests.generated_packet_table import CouplingRunData
from wiliot_deployment_tools.gw_certificate.tests.generic import PASS_STATUS, GenericTest
from wiliot_deployment_tools.gw_certificate.interface.packet_error import PacketError

RECEIVED = 'received'
SHARED_COLUMNS = [PAYLOAD, BRIDGE_ID, NFPKT, RSSI]
INT64_COLUMNS = [NFPKT, RSSI]
OBJECT_COLUMNS = [PAYLOAD, BRIDGE_ID]
INIT_STAGES_DUPLICATIONS = [i for i in range(3,7)]
REPORT_COLUMNS = ['pkt_id', 'bridgeId', 'duplication', 'time_delay']

# TEST STAGES

class CouplingTestError(Exception):
    pass

class GenericCouplingStage():
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, stage_name, **kwargs):
        #Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim
        #Stage Params
        self.stage_name = stage_name
        self.stage_pass = False
        self.report = ''
        self.start_time = None
        self.csv_path = f'{self.certificate_dir}/{self.logger_filename}_{self.stage_name}.csv'
        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        # Packet Error / Run data
        self.packet_error = PacketError()
        self.run_data = CouplingRunData
    
    def prepare_stage(self):
        debug_print(f'### Starting Stage: {self.stage_name}')
        self.mqttc.flash_pkts()
        self.ble_sim.set_sim_mode(True)
        
    def fetch_mqtt_from_stage(self):
        self.mqtt_pkts = self.mqttc.get_coupled_tags_pkts()
        
    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts)
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        if not set(SHARED_COLUMNS) <= set(mqtt_pkts_df.columns):
            missing_columns = list(set(SHARED_COLUMNS) - set(mqtt_pkts_df.columns))
            for missing_column in missing_columns:
                if missing_column in OBJECT_COLUMNS:
                    mqtt_pkts_df[missing_column] = ''
                if missing_column in INT64_COLUMNS:
                    mqtt_pkts_df[missing_column] = 0
        comparison = local_pkts_df
        received_pkts_df = pd.merge(local_pkts_df[SHARED_COLUMNS], mqtt_pkts_df[SHARED_COLUMNS], how='inner')
        received_pkts = set(received_pkts_df[PAYLOAD])
        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        comparison['pkt_id'] = comparison['payload'].apply(lambda x: x[-8:])
        self.comparison = comparison
        
    def add_to_stage_report(self, report):
        self.report += '\n' + report
        
    def generate_stage_report(self):
        self.compare_local_mqtt()
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_sent == num_pkts_received
        report.append((('Number of coupled packets sent'), num_pkts_sent))
        report.append((('Number of coupled packets received'), num_pkts_received))
        self.add_to_stage_report(f'---Stage {self.stage_name} {PASS_STATUS[self.stage_pass]}, Running time {datetime.datetime.now() - self.start_time}')
        self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(report), showindex=False))
        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received)>0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))
        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        return self.report
    
class InitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='init_stage')
        self.pkt_gen = PktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for idx, duplication in enumerate(INIT_STAGES_DUPLICATIONS):
            new_pkt = self.pkt_gen.get_new_packet_pair()
            # First 2 runs generate smallest RSSI/NFPKT
            # Last 2 runs generate biggest RSSI/NFPKT
            if idx < 2:
                self.pkt_gen.set_rssi_nfpkt(idx, idx)
            else:
                self.pkt_gen.set_rssi_nfpkt(MAX_RSSI-idx+2, MAX_NFPKT-idx+2)
            new_pkt = self.pkt_gen.get_existing_packet_pair()
            expected_pkt = self.pkt_gen.get_expected_mqtt()
            data = new_pkt['data_packet'].dump()
            si = new_pkt['si_packet'].dump()
            expected_pkt.update({'duplication': duplication, 'time_delay': DEFAULT_DELAY,
            'si_rawpacket': si, 'data_rawpacket': data})
            self.local_pkts.append(expected_pkt)
            self.ble_sim.send_data_si_pair(data, si, duplication, delay=DEFAULT_DELAY)
        time.sleep(5)

class OneBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='1brg_stage')
        self.pkt_gen = PktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in DUPLICATIONS: #tqdm(duplications, desc='Duplications', position=1, leave=True):
            debug_print(f'Duplication {duplication}')
            for time_delay in TIME_DELAYS: #tqdm(time_delays, desc='Time Delays', position=2, leave=True):
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    new_pkt = self.pkt_gen.get_new_packet_pair()
                    data = new_pkt['data_packet'].dump()
                    si = new_pkt['si_packet'].dump()
                    expected_pkt = self.pkt_gen.get_expected_mqtt()
                    packet_error = self.packet_error._generate_packet_error(duplication)
                    expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                        'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data})
                    self.local_pkts.append(expected_pkt)
                else:
                    run_data = self.run_data.get_data(duplication, time_delay, BRIDGES[0])
                    data = run_data.data
                    si = run_data.si
                    packet_error = run_data.packet_error
                    self.local_pkts.append(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
        time.sleep(5)

class ThreeBrgInitStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='3brg_init_stage')
        self.brg_array = BrgArray()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        duplication = DUPLICATIONS[3]
        time_delay = TIME_DELAYS[2]
        if self.randomize:
            # Generate new random packet
            pkts = self.brg_array.get_scattered_pkt_pairs(time_delay)
            for brg_idx, pkt in enumerate(pkts):
                packet_error = self.packet_error._generate_packet_error(duplication)
                # Dump packets
                data = pkt['data_packet'].dump()
                pkt['data_packet'] = data
                si = pkt['si_packet'].dump()
                pkt['si_packet'] = si
                pkt['packet_error'] = packet_error
                bridge_id = pkt['bridge_id']
                scattered_time_delay = pkt['time_delay']
                # log the sent packet with relevant info from run
                expected_pkt = self.brg_array.brg_list[brg_idx].get_expected_mqtt()
                expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                    'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': brg_idx,
                                    'bridge_id': bridge_id, 'scattered_time_delay': scattered_time_delay})
                self.local_pkts.append(expected_pkt)
            self.ble_sim.send_brg_array_pkts(pkts, duplication)
        else:
            # Construct packet list from data
            pkts = []
            for brg_idx in BRIDGES:
                pkt = {}
                run_data = self.run_data.get_data(duplication, time_delay, brg_idx)
                pkt['data_packet'] = run_data.data
                pkt['si_packet'] = run_data.si
                pkt['time_delay'] = run_data.scattered_time_delay
                pkt['packet_error'] = run_data.packet_error
                pkt['bridge_id'] = run_data.bridge_id
                self.local_pkts.append(run_data.expected_mqtt)
                pkts.append(pkt)
            # Send scattered packets
            self.ble_sim.send_brg_array_pkts(pkts, duplication)
        time.sleep(5)
        


class ThreeBrgStage(GenericCouplingStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name='3brg_stage')
        self.brg_array = BrgArray()

    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            # Time delays from 30 -> 255
            for time_delay in TIME_DELAYS[1:]:
                debug_print(f'Time Delay {time_delay}')
                if self.randomize:
                    # Generate new random packet
                    pkts = self.brg_array.get_scattered_pkt_pairs(time_delay)
                    for brg_idx, pkt in enumerate(pkts):
                        packet_error = self.packet_error._generate_packet_error(duplication)
                        # Dump packets
                        data = pkt['data_packet'].dump()
                        pkt['data_packet'] = data
                        si = pkt['si_packet'].dump()
                        pkt['si_packet'] = si
                        pkt['packet_error'] = packet_error
                        bridge_id = pkt['bridge_id']
                        scattered_time_delay = pkt['time_delay']
                        # log the sent packet with relevant info from run
                        expected_pkt = self.brg_array.brg_list[brg_idx].get_expected_mqtt()
                        expected_pkt.update({'duplication': duplication, 'time_delay': time_delay,
                                            'packet_error': packet_error, 'si_rawpacket': si, 'data_rawpacket': data, 'brg_idx': brg_idx,
                                            'bridge_id': bridge_id, 'scattered_time_delay': scattered_time_delay})
                        self.local_pkts.append(expected_pkt)
                    self.ble_sim.send_brg_array_pkts(pkts, duplication)
                else:
                    # Construct packet list from data
                    pkts = []
                    for brg_idx in BRIDGES:
                        pkt = {}
                        run_data = self.run_data.get_data(duplication, time_delay, brg_idx)
                        pkt['data_packet'] = run_data.data
                        pkt['si_packet'] = run_data.si
                        pkt['time_delay'] = run_data.scattered_time_delay
                        pkt['packet_error'] = run_data.packet_error
                        pkt['bridge_id'] = run_data.bridge_id
                        self.local_pkts.append(run_data.expected_mqtt)
                        pkts.append(pkt)
                    # Send scattered packets
                    self.ble_sim.send_brg_array_pkts(pkts, duplication)
        time.sleep(5)


# TEST CLASS

STAGES = [InitStage, OneBrgStage, ThreeBrgInitStage, ThreeBrgStage]
# STAGES = [InitStage]

class CouplingTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        self.randomize = True
        super().__init__(**self.__dict__)
        self.stages = [stage(**self.__dict__) for stage in STAGES]

    def enter_dev_mode(self):
        self.edge.enter_dev_mode(self.gw_id, legacy=self.legacy)
        gw_info = self.mqttc.get_gw_info()
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            debug_print('Waiting to see GW in DevMode...')
            gw_seen = self.mqttc.userdata['gw_seen']
            if gw_seen is True or gw_info is not False:
                debug_print(f'GW {self.gw_id} In DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot enter GW DevMode!')
    
    def run(self):
        self.start_time = datetime.datetime.now()
        self.enter_dev_mode()
        self.test_pass = True
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            if stage.stage_pass == False:
                self.test_pass = False
        run_time = datetime.datetime.now() - self.start_time
        debug_print(f'\n{SEP}')
        debug_print(f'Coupling Test {PASS_STATUS[self.test_pass]}, Running time {datetime.datetime.now() - self.start_time}')
        debug_print(self.report)
        self.exit_dev_mode()
    
    def exit_dev_mode(self):
        self.mqttc.exit_dev_mode(legacy=self.legacy)
        timeout = datetime.datetime.now() + datetime.timedelta(minutes=3)
        while datetime.datetime.now() < timeout:
            online_status = self.edge.check_gw_online([self.gw_id])
            if online_status is not False:
                debug_print(f'GW {self.gw_id} Out Of DevMode')
                return True
            time.sleep(10)
        raise CouplingTestError('Cannot exit GW DevMode!')
