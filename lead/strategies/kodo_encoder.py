import os
import sys
import kodo

class KodoEncoder:
    def __init__(self, symbols, symbol_size, redundancy=2):
        self.symbols = symbols
        self.n_nodes = 4
        self.redundancy = redundancy
        self.__encoder = kodo.RLNCEncoderFactory(kodo.field.binary8, symbols,
                                                 symbol_size).build()

    def encode(self, data):
        self.__encoder.set_const_symbols(data)

        encoded_packets = []
        remainder = (self.symbols + self.redundancy) % self.n_nodes
        payloads_per_node = int((self.symbols + self.redundancy) - remainder) / self.n_nodes

        for i in range(payloads_per_node * self.n_nodes):
            # Send the payload to a node
            encoded_packets.append(self.encoder.write_payload())

        for i in range(remainder):
            encoded_packets.append(self.encoder.write_payload())

        return packets
