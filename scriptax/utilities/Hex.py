def instance_to_hexid(instance):
    return '0x' + hex(id(instance)).upper()[2:]
