import os
import sys
import kodo

class KodoEncoder():

    def __init__(self):
        self.field = None
        self.factory = None
        self.encoder = None
        self.data = None

    def init_encoder(self, symbols, symbol_size):
        if self.encoder is None:
            self.field = kodo.field.binary8
            self.factory = kodo.RLNCEncoderFactory(self.field, symbols, symbol_size)
            self.encoder = self.factory.build()
        return self.encoder
        
    def encode(self, bytes):
        self.encoder.set_const_symbols(bytes)
        packets = []
        print("executing encoder")
        packets.append(self.encoder.write_payload())
        print(packets)
        return packets