import os
import sys
import kodo

class KodoDecoder:
    def __init__(self, symbols, symbol_size):
        self.__decoder = kodo.RLNCDecoderFactory(kodo.field.binary8, symbols,
                                               symbol_size).build()

    def decode(self, packets):
        print(1)
        data_out = bytearray(self.__decoder.block_size())
        self.__decoder.set_mutable_symbols(data_out)
        for packet in packets:
            print(packet)
            self.decoder.read_payload(packet)
            if self.__decoder.is_complete():
                break
            self.decoder.read_payload(packet)
            print()
        return data_out