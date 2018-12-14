import os
import sys
import kodo

class KodoDecoder():

    def __init__(self):
        self.field = None
        self.factory = None
        self.decoder = None

    def init_decoder(self, symbols, symbol_size):
        if self.decoder is None:
            self.field = kodo.field.binary8
            self.factory = kodo.RLNCDecoderFactory(self.field, symbols, symbol_size)
            self.decoder = self.factory.build()
        return self.decoder


    def decode(self, packets):
        print(1)
        data_out = bytearray(self.decoder.block_size())
        self.decoder.set_mutable_symbols(data_out)
        packet_number = 0
        for f in packets:
            print(f)
            if self.decoder.is_complete() == True:
                break
            self.decoder.read_payload(packets[packet_number])
            print()
            packet_number += 1
        return data_out