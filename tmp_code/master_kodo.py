import os
import kodo


class MasterKodo:

    def __init__(self):
        self.field = None
        self.factory_encoder = None
        self.encoder = None
        self.data = None
        self.factory_decoder = None
        self.decoder = None

    def init_encoder(self, symbols, symbol_size):
        if self.encoder is None:
            self.field = kodo.field.binary8
            self.factory_encoder = kodo.RLNCEncoderFactory(self.field, symbols, symbol_size)
            self.encoder = self.factory_encoder.build()
        return self.encoder

    def init_decoder(self, symbols, symbol_size):
        if self.decoder is None:
            self.field = kodo.field.binary8
            self.factory_decoder = kodo.RLNCDecoderFactory(self.field, symbols, symbol_size)
            self.decoder = self.factory_decoder.build()
        return self.decoder


    def encode(self, symbol_size):
        print("Encoder starting")
        # Generate some random data to encode and assign it to the encoder
        # This bytearray must not go out of scope while the encoder exists!
        data_in = bytearray(os.urandom(self.encoder.block_size()))
        self.encoder.set_const_symbols(data_in)

        encoded_packets = []
        packets_count = symbol_size + 1
        for i in range(packets_count):
            encoded_packets.append(self.encoder.write_payload())

        return [data_in, encoded_packets]


    def decode(self, encoded_packets):
        print("Decoder starting")
        # Define the data_out bytearray where the symbols should be decoded
        # This bytearray must not go out of scope while the decoder exists!
        data_out = bytearray(self.encoder.block_size())
        self.decoder.set_mutable_symbols(data_out)

        for i in range(len(encoded_packets)):
            if self.decoder.is_complete():
                break
            self.decoder.read_payload(encoded_packets[i])

        return data_out