import math
import mcschematic
schem = mcschematic.MCSchematic()

def add_bit(data, offset_x, offset_y, offset_z):
    if data == '1' :
        data = "true"
    else: data = "false"
    schem.setBlock((offset_x, offset_y -1, offset_z), "minecraft:purple_wool")
    schem.setBlock((offset_x, offset_y, offset_z), f"minecraft:repeater[powered={data},facing=south]")



def inst_to_bits(inst):
    for i in range(0, len(str(inst))):
        add_bit(list(str(inst))[i], 0, (i%25) * 3, (math.trunc(i/25) * 2))
    print(list(str(inst)))


def register_to_binary(register):
    register_number = int(register[1:])
    return f"{register_number:05b}"[::-1]



def const_to_binary(const):
    if const[0] == 'b':
        return const[1:]
    else: return f"{int(const):016b}"[::-1]



def assemble_instructions(instruction):
    opcode_map = {
        "NOP" : "0000",
        "HLT" : "1000",
        "ADD" : "0100",
        "SUB" : "1100",
        "NOR" : "0010",
        "AND" : "1010",
        "XOR" : "0110",
        "RSH" : "1110",
        "LDI" : "0001",
        "DIS" : "0001",
        "ADI" : "1001"
    }

    parts = instruction.split()
    opcode = opcode_map[parts[0]]
    match parts[0]:
        case "NOP" : return f"{0:025b}"
        case "HLT" : return f"{opcode}{0:021b}"
        case "ADD" : return f"{opcode}{register_to_binary(parts[1])}{register_to_binary(parts[2])}{register_to_binary(parts[3])}{0:06b}"
        case "SUB" : return f"{opcode}{register_to_binary(parts[1])}{register_to_binary(parts[2])}{register_to_binary(parts[3])}{0:06b}"
        case "NOR" : return f"{opcode}{register_to_binary(parts[1])}{register_to_binary(parts[2])}{register_to_binary(parts[3])}{0:06b}"
        case "AND" : return f"{opcode}{register_to_binary(parts[1])}{register_to_binary(parts[2])}{register_to_binary(parts[3])}{0:06b}"
        case "XOR" : return f"{opcode}{register_to_binary(parts[1])}{register_to_binary(parts[2])}{register_to_binary(parts[3])}{0:06b}"
        case "RSH" : return f"{opcode}{register_to_binary(parts[1])}{0:05b} {register_to_binary(parts[2])}{0:07b}"
        case "LDI" : return f"{opcode}{register_to_binary(parts[1])}{const_to_binary(parts[2])}"
        case "DIS" : return f"{opcode}{register_to_binary('r31')}{f'{int(parts[1]):06b}'[::-1]}{f'{int(parts[2]):06b}'[::-1]}{parts[3]}{parts[4]}00"
        case "ADI" : return f"{opcode}{register_to_binary(parts[1])}{const_to_binary(parts[2])}"



def read_files_into_list(filename):
    result = []
    with open(filename, 'r') as file:
        for line in file:
            machine_code = assemble_instructions(line.strip())
            result.append(machine_code)
    return result



def machine_code_to_schematic(machine_code_file, schematic_file):

    with open(machine_code_file, 'r') as machine_code:
        for line in machine_code:
            result =  f"{(str(line.replace(' ', '')))}"
        inst_to_bits(result)



machine_code_result = read_files_into_list("test assembler.txt")



with open("result.txt", 'w') as file:
    for line in machine_code_result:
        file.write(line)



machine_code_to_schematic("result.txt", "myschems/my_cool_schematic.schem")



schem.save("myschems", "my_cool_schematic", mcschematic.Version.JE_1_18_2)
