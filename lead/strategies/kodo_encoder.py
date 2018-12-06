import os
import sys
import kodo

class KodoEncoder():

    def init_encoder(symbols, symbol_size):
        if self.encoder is None:
            field = kodo.field.binary8
            encoder_factory = kodo.RLNCEncoderFactory(field, symbols, symbol_size)
            self.encoder = encoder_factory.build()  
        return self.encoder
        
    def encode(bytes):
        #self.encoder = init_decoder(symbols,symbol_size)
        self.encoder.set_const_symbols(bytes)
        packets = []
        while not self.encoder.is_complete():
            packets.append(self.encoder.write_payload())
        return packets