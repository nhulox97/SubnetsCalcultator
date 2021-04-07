# TODO: Hacer input la ip inicial y los hos solicitados, estos ultimos deben 
# ser un input donde los valores estaran separados por espacio para poder hacer
# el split.


# logica para seprar octetos de la ip
# input ip inicial
ip_inicial = '174.40.6.0'
host = 3
octetos = ip_inicial.split('.')
octetos = [int(octeto) for octeto in octetos]
host_solicitados = [300, 200, 110, 60, 10, 2, 2, 2]
host_len = len(host_solicitados)
pesos = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
host_encontrados = 0


def get_mascara_de_red(peso):
    mask_string = ''
    mask_bits = 32 - peso
    for bit in range(0, 32, 1):
        if bit >= mask_bits:
            mask_string += '0'
        else:
            mask_string += '1'
        if (bit + 1) % 8 == 0 and bit < 31:
            mask_string += '.'

    # convertir octetos a decimal
    mask_octetos = mask_string.split('.')
    mask_decimal = ''
    position_mask = 0
    for mask_octeto in mask_octetos:
        digito_d = 0
        for position, digito_s in enumerate(mask_octeto[::-1]):
            digito_d += int(digito_s) * 2 ** position
        # concatenar el valor decimal del octeto
        mask_decimal += f'{digito_d}'
        if position_mask < 3:
            mask_decimal += '.'
        position_mask += 1

    #concatenar bits de red
    mask_decimal += f'/{mask_bits}'

    return [mask_string, mask_decimal]


def concat_octetos(c_octetos: list, type: str = ''):
    octeto_ultimo = c_octetos[3]
    if (type == 'p'):
        octeto_ultimo += 1
    if (type == 'u'):
        octeto_ultimo -= 1

    return f'{c_octetos[0]}.{c_octetos[1]}.{c_octetos[2]}.{octeto_ultimo}'


def print_subnets(lsubnet):
    print('\hline %18s & %15s & %15s & %15s & %15s \\\\' %
          ('Mascar de red','Ip de red', 'Primera IP', 'Ultima IP', 'Ip Broadcast'))
    for subnet in subnets:
        mask, red, primera, ultima, broadcast = subnet
        print('\hline %18s & %15s & %15s & %15s & %15s \\\\' % (mask, red, primera, ultima, broadcast))


counter = 0
subnets = [[]]

for host_solicitado in host_solicitados:
    # print('=' * 80)
    # encontrar los hosts solicitados
    peso_index = 0
    for peso in pesos:
        peso_encontrado = peso - 2
        if peso_encontrado >= host_solicitado:
            host_encontrados = peso_encontrado
            break
        peso_index += 1

    # obetener mascara de red
    mask_b, mask_d = get_mascara_de_red(peso_index)
    # agregar mascara de red
    subnets[counter].append(mask_d)
    # agregar ip de direccion red
    subnets[counter].append(concat_octetos(octetos))
    # aregar primera ip de
    subnets[counter].append(concat_octetos(octetos, 'p'))
    # sumar los bits de hosts a la ip
    was_added = False
    counter_interno = 0
    while not was_added:
        octeto = octetos[host]
        # saber si la suma del octeto y los hosts es mayor que 255
        octeto_host = octeto + host_encontrados
        host_aux = True
        is_added = False
        # verificar si los hosts encontrados son mayor que 255
        if octeto_host > 255:
            octetos[host - 1] = octetos[host - 1] + 1
            octetos[host] = 0
            host_encontrados = 255 - octeto
            host_aux = False
            is_added = True

        if host_aux:
            if counter_interno < 1:
                octetos[host] = octeto_host + 1
            else:
                octetos[host] = octeto_host

            # agregar ultima ip disponible
            subnets[counter].append(concat_octetos(octetos, 'u'))
            # agregar ip de broadcast
            subnets[counter].append(concat_octetos(octetos))
            # print('=' * 80)
            was_added = True
        counter_interno += 1

    # sumarle + 1 para que el broadcast salga ocupada
    broadcast = octetos[host] + 1
    if (broadcast > 255):
        octetos[host - 1] = octetos[host - 1] + 1
        octetos[host] = 0
    else:
        octetos[host] = broadcast

    counter += 1
    if (counter < host_len):
        subnets.append([])

print_subnets(subnets)
