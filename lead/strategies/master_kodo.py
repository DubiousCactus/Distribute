import kodo


class MasterKodo:

    def __init__(self):
        self.field = None
        self.factory_encoder = None
        self.encoder = None
        self.data = None
        self.factory_decoder = None
        self.decoder = None
        self.nodeCount = 4

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


    def encode(self, data_in, symbols, loses):
        print("Encoder starting")
        self.encoder.set_const_symbols(data_in)
        print("[1]")
        self.encoder.set_systematic_off()
        print("[2]")
        encoded_packets = []
        print("[3]")
        overhead = (int(symbols)*int(loses))/(int(self.nodeCount)-int(loses))
        print("[4]")
        packets_count = symbols + overhead
        print("symbold: {}".format(symbols))
        print("loses: {}".format(loses))
        print("Calulcated overhead: {}".format(overhead))
        print("Encoded packages created: {}".format(packets_count))
        for i in range(packets_count):
            encoded_packets.append(self.encoder.write_payload())
        print("Encoder end")
        return [data_in, encoded_packets]


    def decode(self, encoded_packets):
        print("Decoder starting")
        # Define the data_out bytearray where the symbols should be decoded
        # This bytearray must not go out of scope while the decoder exists!
        data_out = bytearray(self.decoder.block_size())
        self.decoder.set_mutable_symbols(data_out)
        for i in range(len(encoded_packets)):
            #print("Decoder rank: {}".format(self.decoder.rank()))
            if self.decoder.is_complete():
                print("Decoder end")
                return data_out
            self.decoder.read_payload(bytearray(encoded_packets[i].decode('hex')))
        return None


    def lose_encoded_packets(self, encoded_packets, number):
        for i in range(number):
            encoded_packets.pop()
        return encoded_packets

    def print_encoder_state(self):
        print("------START: State of the encoder------")
        print(
            "block_size: {}\n"
            "is_systematic_on: {}\n"
            "in_systematic_phase: {}\n"
            "payload_size: {}\n"
            "rank: {}\n"
            "symbol_size: {}\n"
            "symbols: {}".format(
                self.encoder.block_size(),
                self.encoder.is_systematic_on(),
                self.encoder.in_systematic_phase(),
                self.encoder.payload_size(),
                self.encoder.rank(),
                self.encoder.symbol_size(),
                self.encoder.symbols())
        )
        print("------END: State of the encoder------")



