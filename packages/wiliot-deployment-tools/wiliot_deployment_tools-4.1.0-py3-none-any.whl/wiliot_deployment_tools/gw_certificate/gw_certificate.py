import time
import os
from wiliot_deployment_tools.api.extended_api import ExtendedEdgeClient
from wiliot_deployment_tools.common.analysis_data_bricks import initialize_logger
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_core.utils.utils import WiliotDir
from wiliot_deployment_tools.gw_certificate.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.gw_certificate.interface.mqtt import MqttClient
from wiliot_deployment_tools.gw_certificate.tests.coupling import CouplingTest
from wiliot_deployment_tools.interface.uart_ports import get_uart_ports

class GWCertificateError(Exception):
    pass

class GWCertificate:
    def __init__(self, gw_id, api_key, owner_id, env='prod', random=False, legacy=False):
        self.env_dirs = WiliotDir()
        self.certificate_dir = os.path.join(self.env_dirs.get_wiliot_root_app_dir(), 'gw-certificate')
        self.env_dirs.create_dir(self.certificate_dir)
        self.logger_filename = initialize_logger(self.certificate_dir)
        self.gw_id = gw_id
        self.owner_id = owner_id
        self.edge = ExtendedEdgeClient(api_key, owner_id, env=env)
        self.mqttc = MqttClient(gw_id, owner_id, f'{self.certificate_dir}/{self.logger_filename}_mqtt.log')
        self.uart_comports = get_uart_ports()
        if random:
            debug_print('Randomizing Test!')
        self.randomize = random
        if legacy:
            debug_print('Working in LEGACY DevMode!')
        self.legacy = legacy
        debug_print(f'UART Ports:{self.uart_comports}')
        if len(self.uart_comports) < 1:
            raise GWCertificateError('A Wiliot GW needs to be connected to USB!')
        self.ble_sim = BLESimulator(self.uart_comports[0])
        if not self.ble_sim.check_version_for_sim():
            raise GWCertificateError('USB GW Version not compatible with BLE Simulator!')
        # self.sniffer = SnifferClass(self.uart_comports[1])
        self.tests = [CouplingTest(**self.__dict__)]
    
    def run_tests(self):
        for test in self.tests:
            test.run()

# TODO - send HB and CFG 
# TODO - UnCoupled Mode
