import re
from rest_framework import serializers


def validate_rut(value: str):
    rut = value.replace('.', '').replace('-', '').upper()
    if not re.match(r'^\d{7,8}[0-9K]$', rut):
        raise serializers.ValidationError('RUT inválido: formato incorrecto')
    
    body, dv = rut[:-1], rut[-1]
    s, m = 0, 2
    for d in reversed(body):
        s += int(d) * m
        m = 2 if m == 7 else m + 1
    
    calc = 11 - (s % 11)
    expected = '0' if calc == 11 else 'K' if calc == 10 else str(calc)
    
    if dv != expected:
        raise serializers.ValidationError('RUT inválido: dígito verificador incorrecto')


def validate_plate(value: str):
    plate = value.strip().upper()
    if not re.match(r'^[A-Z]{2,4}\d{2,4}$', plate):
        raise serializers.ValidationError('Patente inválida (ej: AB1234, ABCD12)')
