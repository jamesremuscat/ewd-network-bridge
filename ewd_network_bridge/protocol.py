# # Set of cyclic parameters for receivers
# DEMO_DATA_RX = {
#     'Name': ['Test EWD'],
#     'Frequency': ['169175', '21', 1],
#     'Mute': [0],
#     'RF1': [25, 50, 0],
#     'RF2': [33, 66, 1],
#     'States': [3, 2],
#     'RF': [70, 1, 1],
#     'AF': [48, 55, 3],
#     'Bat': [40],
#     'Msg': ['OK'],
#     'Config': [234]
# }


# # Set of cyclic parameters for IEM transmitters
# DEMO_DATA_TX = {
#     'Name': ['IEM X   '],
#     'Frequency': ['169175', '21', 1],
#     'Sensitivity': [-21],
#     'Mode': [1],
#     'Equalizer': [0, 0, 0, 0, 0, 0],
#     'Mute': [0],
# }


def encode_attribute(name, params):
    return f'{name} {" ".join(map(str, params))}'


class MediaControlProtocol:

    def __init__(self, device) -> None:
        self.device = device

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        parts = message.strip().split(' ')
        command = parts[0]
        params = parts[1:]

        if command == 'Push':
            # print('Replying to Push from', addr)
            response = encode_attribute('Push', params) + '\x0d'
            for key, value in self.device.to_params_data().items():
                response += encode_attribute(key, value) + '\x0d'

            self.transport.sendto(response.encode(), addr)
        else:
            print(f'Received command {command} with parameters: {params} from {addr}')
