
from master_kodo import MasterKodo

if __name__ == '__main__':
    masterkodo = MasterKodo()
    symbols = 3
    symbol_size = 160
    size = 16

    masterkodo.init_encoder(symbols, symbol_size)
    masterkodo.init_decoder(symbols, symbol_size)

    [data_in, encoded_packets] = masterkodo.encode(symbol_size)
    data_out = masterkodo.decode(encoded_packets)

    if data_out == data_in:
        print("Data decoded correctly")
    else:
        print("Unable to decode please try again :)")