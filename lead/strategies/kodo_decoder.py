import os
import sys
import kodo

class KodoDecoder():
    def __init__(self):

    def init_decoder(symbols, symbol_size):
        if self.decoder is None:
            field = kodo.field.binary8
            decoder_factory = kodo.RLNCDecoderFactory(field, symbols, symbol_size)
            self.decoder = decoder_factory.build()    
        return self.decoder

    def decode(packets):
        #self.decoder = init_decoder(symbols,symbol_size)
        data_out = bytearray(decoder.block_size())
        self.decoder.set_mutable_symbols(data_out)
        packet_number = 0
        for f in packets:
            if self.__decoder.is_complete() == true:
                break
            self.decoder.read_payload(packet[packet_number])
            packet_number += 1
        return data_out