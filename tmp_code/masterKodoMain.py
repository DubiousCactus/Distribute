
from master_kodo import MasterKodo
import os

if __name__ == '__main__':
    masterkodo = MasterKodo()
    size = 8
    # A large message is split into several chunks (also called generations)
    # Set the number of symbols (i.e. the generation size in RLNC terminology)
    # and the size of a symbol in bytes
    symbols = 10
    symbol_size = 10

    overhead = 2
    # Simulate lost packages
    lost_package = 2

    # Generate some random data to encode and assign it to the encoder
    # This bytearray must not go out of scope while the encoder exists!
    data_in = bytearray(os.urandom(symbols*symbol_size))

    masterkodo.init_encoder(symbols, symbol_size)
    masterkodo.init_decoder(symbols, symbol_size)

    masterkodo.print_encoder_state()
    [data_in, encoded_packets] = masterkodo.encode(data_in, symbols, overhead)
    masterkodo.lose_encoded_packets(encoded_packets, lost_package)
    data_out = masterkodo.decode(encoded_packets)

    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unable to decode please try again :)")

    masterkodo.print_encoder_state()