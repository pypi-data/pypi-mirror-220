import datetime
from numpy import byte
import serial
import serial.tools.list_ports
import time
from wiliot_deployment_tools.ag.wlt_types_ag import CHANNEL_37, CHANNEL_38, CHANNEL_39
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.interface.if_defines import CANCEL, DEFAULT_ADVA, DEFAULT_DELAY, DEFAULT_OUTPUT_POWER, GW_APP_RX_ONLY, GW_APP_VERSION_HEADER, RESET_GW, SEND_ALL_ADV_CHANNELS, SEP, SERIAL_TIMEOUT, VERSION
from wiliot_deployment_tools.gw_certificate.interface.pkt_generator import PktGenerator

class BLESimulator:
    def __init__(self, comport):
        self.serial = serial.Serial(port=comport, baudrate=921600, timeout=SERIAL_TIMEOUT)
        self.serial.flushInput()
        self.write_ble_command('!reset')

        self.sim_mode = False
        debug_print(f'Serial Connection {comport} Initialized')

    @staticmethod
    def get_comports():
        ports = serial.tools.list_ports.comports()
        debug_print(SEP + "\nAvailable ports:")
        for port, desc, hwid in sorted(ports):
            debug_print("{}: {} [{}]".format(port, desc, hwid))
        debug_print(SEP + "\n")
        return ports
    
    def rx_only_gw(self):
        self.write_ble_command(GW_APP_RX_ONLY)
        
    def write_ble_command(self, cmd, read=False): 
        # This function writes a command (cmd) to the ble using a serial connection (ble_ser) that are provided to it beforehand.. and returns the answer from the device as string
        debug_print("Write to BLE: {}".format(cmd)) 
        # Shows on terminal what command is about to be printed to the BLE device
        bytes_to_write = bytes(cmd.encode("utf-8")) + b'\r\n'
        self.serial.write(bytes_to_write)
        answer = None
        if read:
            # The "bytes" function converts the command from string to bytes by the specified "utf-8" protocol then we use .write to send the byte sequence to the ble device using the serial connection that we have for this port (ble_ser)
            # Pauses the program for execution for 0.01sec. This is done to allow the device to process the command and provide a response before reading the response.
            time.sleep(1)
            self.serial.flush()
            answer = self.serial.readline().strip().decode("utf-8", "ignore") 
            # This reads a line from the ble device (from the serial connection using ble_ser), strips it from white spaces and then decodes to string from byts using the "utf-8" protocol.
            debug_print(answer)
        return answer
    
    def reset_gw(self):
        self.serial.flushInput()
        self.write_ble_command(RESET_GW)
        time.sleep(3)
                    
    def set_sim_mode(self, sim_mode):
        self.serial.flushInput()
        self.serial.close()
        self.serial.open()
        mode_dict = {True: 1, False: 0}
        self.sim_mode = sim_mode
        self.reset_gw()
        self.write_ble_command(f"!ble_sim_init {mode_dict[sim_mode]}")
        if not sim_mode:
            self.write_ble_command(CANCEL)
        time.sleep(3)
    
    def get_version(self):
        self.serial.close()
        self.serial.open()
        self.reset_gw()
        time.sleep(3)
        raw_version = self.write_ble_command(VERSION, read=True)
        if GW_APP_VERSION_HEADER not in raw_version:
            return None
        return raw_version.split(' ')[0].split('=')[1]

        return raw_version
    
    def check_version_for_sim(self):
        retries = 5
        for i in range(retries):
            version = self.get_version()
            if version is None:
                continue
            version = version.split('.')
            if ((int(version[0]) > 3) or (int(version[0]) > 2 and int(version[1]) > 15) or \
                    (int(version[0]) > 2 and int(version[1]) > 14 and int(version[2]) > 43)):
                return True
        return False

    def send_packet(self, raw_packet, duplicates, output_power, channel, delay):
        assert self.sim_mode is True, 'BLE Sim not initialized!'
        if len(raw_packet) == 62:
            # Add ADVA
            raw_packet = DEFAULT_ADVA + raw_packet
        if len(raw_packet) != 74:
            raise ValueError('Raw Packet must be 62/74 chars long!')
        self.write_ble_command(f"!ble_sim {str(raw_packet)} {str(duplicates)} {str(output_power)} {str(channel)} {str(delay)}")
    
    def send_data_si_pair(self, data_packet, si_packet, duplicates, output_power=DEFAULT_OUTPUT_POWER, delay=DEFAULT_DELAY, packet_error=None):
        if packet_error is None:
            packet_error = [True for i in range (duplicates * 2)]
        # debug_print(packet_error)
        # print(f'delay {delay}')
        packet_to_send = data_packet
        def switch_packet(packet_to_send):
            if packet_to_send == data_packet:
                return si_packet
            else:
                return data_packet
        for dup in range(duplicates * 2):
            diff = time.perf_counter()
            if packet_error[dup]:
                debug_print(f'Sending Packet {dup}')
                self.send_packet(packet_to_send, duplicates=1, output_power=output_power, channel=SEND_ALL_ADV_CHANNELS, delay=0)
            else:
                debug_print(f'Dropping Packet {dup}')
            time.sleep(delay/1000)
            diff = time.perf_counter() - diff
            debug_print(f'Desired Delay: {delay/1000} Actual Delay {diff}')
            packet_to_send = switch_packet(packet_to_send)
    
    def send_brg_array_pkts(self, pkts, duplicates, output_power=DEFAULT_OUTPUT_POWER):
        num_brgs = len(pkts)
        total_pkts_to_send = num_brgs * 2 * duplicates
        for pkt_idx in range(total_pkts_to_send):
            brg_idx = pkt_idx % 3
            pkt = pkts[brg_idx]
            pkt_idx_per_brg = pkt_idx // num_brgs
            if not bool(pkt_idx % 2):
                packet_to_send = pkt['data_packet']
            else:
                packet_to_send = pkt['si_packet']
            packet_error = pkt['packet_error']
            if packet_error[pkt_idx_per_brg]:
                debug_print(f'BRG {pkt["bridge_id"]}: Sending Packet {pkt_idx_per_brg}')
                self.send_packet(packet_to_send, duplicates=1, output_power=output_power,
                                 channel=SEND_ALL_ADV_CHANNELS, delay=0)
            else:
                debug_print(f'BRG {pkt["bridge_id"]}: Dropping Packet {pkt_idx_per_brg}')
            diff = time.perf_counter()
            delay = pkt['time_delay']
            time.sleep(delay/1000)
            diff = time.perf_counter() - diff
            debug_print(f'Desired Delay: {delay/1000} Actual Delay {diff}')

        

            
        ### TODO: Sequence List