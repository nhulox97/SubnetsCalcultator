# TODO: Hacer input la ip inicial y los hos solicitados, estos ultimos deben 
# ser un input donde los valores estaran separados por espacio para poder hacer
# el split.


# logica para seprar octets de la ip
# input ip inicial
ip_inicial = '174.40.6.0'
last_octet_position = 3
octets = ip_inicial.split('.')
octets = [int(octet) for octet in octets]
host_solicitados = [300, 200, 110, 60, 10, 2, 2, 2]
host_len = len(host_solicitados)
pesos = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
host_encontrados = 0


def get_network_mask(bit_weight: int = 1):
    """
    Get the network mask based on the bits weight
    :position bit_weight: int
    :return network_mask: list
    """
    mask_string = ''
    mask_bits = 32 - bit_weight
    for bit in range(0, 32, 1):
        if bit >= mask_bits:
            mask_string += '0'
        else:
            mask_string += '1'
        if (bit + 1) % 8 == 0 and bit < 31:
            mask_string += '.'

    # convert binary mask octets to decimal
    mask_octetos = mask_string.split('.')
    mask_decimal = ''
    position_mask = 0
    for mask_octeto in mask_octetos:
        digit_decimal = 0
        for position, digit_string in enumerate(mask_octeto[::-1]):
            digit_decimal += int(digit_string) * 2 ** position
        # concat decimal value to decimal mask
        mask_decimal += f'{digit_decimal}'
        if position_mask < 3:
            mask_decimal += '.'
        position_mask += 1

    # concat network bits
    mask_decimal += f'/{mask_bits}'

    return [mask_string, mask_decimal]


def concat_octets(c_octet: list, position: str = ''):
    last_octet = c_octet[3]
    if position == 'p':
        last_octet += 1
    if position == 'u':
        last_octet -= 1

    return f'{c_octet[0]}.{c_octet[1]}.{c_octet[2]}.{last_octet}'


def print_subnets(lsubnet):
    print('\hline %18s & %15s & %15s & %15s & %15s \\\\' %
          ('Mascara de red', 'Ip de red', 'Primera IP', 'Ultima IP', 'Ip Broadcast'))
    for subnet in subnets:
        mask, red, primera, ultima, broadcast_ip = subnet
        print('\hline %18s & %15s & %15s & %15s & %15s \\\\' % (mask, red, primera, ultima, broadcast_ip))


subnets = [[]]

for requested_host_index, host_solicitado in enumerate(host_solicitados):
    # declare binary and decimal mask
    mask_b, mask_d = '', ''
    # find requested hosts
    for peso_i, peso in enumerate(pesos):
        peso_encontrado = peso - 2
        if peso_encontrado >= host_solicitado:
            host_encontrados = peso_encontrado
            # get network mask
            mask_b, mask_d = get_network_mask(peso_i)
            break

    # append the mask ip
    subnets[requested_host_index].append(mask_d)
    # append the network ip
    subnets[requested_host_index].append(concat_octets(octets))
    # append first available ip
    subnets[requested_host_index].append(concat_octets(octets, 'p'))

    # add last_octet_position bits to ip
    was_added = False
    host_added_counter = 0
    while not was_added:
        octet = octets[last_octet_position]
        octeto_host = octet + host_encontrados
        host_aux = True
        is_added = False
        # check if octet is greater than 255
        if octeto_host > 255:
            octets[last_octet_position - 1] = octets[last_octet_position - 1] + 1
            octets[last_octet_position] = 0
            host_encontrados = 255 - octet
            host_aux = False
            is_added = True

        if host_aux:
            if host_added_counter < 1:
                octets[last_octet_position] = octeto_host + 1
            else:
                octets[last_octet_position] = octeto_host

            # append last available ip
            subnets[requested_host_index].append(concat_octets(octets, 'u'))
            # append broadcast ip
            subnets[requested_host_index].append(concat_octets(octets))
            was_added = True
        host_added_counter += 1

    # add 1 to last octet to mark previous broadcast ip as unavailable
    broadcast = octets[last_octet_position] + 1

    # check if the next network ip is greater than 255
    if broadcast > 255:
        octets[last_octet_position - 1] = octets[last_octet_position - 1] + 1
        octets[last_octet_position] = 0
    else:
        octets[last_octet_position] = broadcast

    if requested_host_index < (host_len - 1):
        subnets.append([])


if __name__ == '__main__':
    print_subnets(subnets)
