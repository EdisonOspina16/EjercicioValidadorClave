from abc import ABC, abstractmethod
import re
from errores import NoCumpleLongitudMinimaError, NoTieneLetraMayusculaError, NoTieneLetraMinusculaError, \
    NoTieneNumeroError, NoTieneCaracterEspecialError, NoTienePalabraSecretaError


class ReglaValidacion(ABC):
    def __init__(self, longitud_esperada):
        self._longitud_esperada = longitud_esperada

    def _validar_longitud(self, clave):
        return len(clave) > self._longitud_esperada

    def _contiene_mayuscula(self, clave):
        return any(c.isupper() for c in clave)

    def _contiene_minuscula(self, clave):
        return any(c.islower() for c in clave)

    def _contiene_numero(self, clave):
        return any(c.isdigit() for c in clave)

    @abstractmethod
    def es_valida(self, clave):
        pass


class ReglaValidacionGanimedes(ReglaValidacion):
    def __init__(self):
        super().__init__(8)

    @staticmethod
    def contiene_caracter_especial(clave):
        return any(c in '@_#$%' for c in clave)

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La longitud debe ser mayor a 8 caracteres")
        if not self._contiene_mayuscula(clave):
            raise NoTieneLetraMayusculaError("Debe contener al menos una letra mayúscula")
        if not self._contiene_minuscula(clave):
            raise NoTieneLetraMinusculaError("Debe contener al menos una letra minúscula")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("Debe contener al menos un número")
        if not self.contiene_caracter_especial(clave):
            raise NoTieneCaracterEspecialError("Debe contener al menos un caracter especial (@, _, #, $, %)")
        return True


class ReglaValidacionCalisto(ReglaValidacion):
    def __init__(self):
        super().__init__(6)

    @staticmethod
    def contiene_calisto(clave):
        matches = re.finditer(r'c.*a.*l.*i.*s.*t.*o', clave, re.IGNORECASE)
        for match in matches:
            substring = match.group()
            if sum(1 for c in substring if c.isupper()) >= 2 and not substring.isupper():
                return True
        return False

    def es_valida(self, clave):
        if not self._validar_longitud(clave):
            raise NoCumpleLongitudMinimaError("La longitud debe ser mayor a 6 caracteres")
        if not self._contiene_numero(clave):
            raise NoTieneNumeroError("Debe contener al menos un número")
        if not self.contiene_calisto(clave):
            raise NoTienePalabraSecretaError(
                "Debe contener la palabra 'calisto' con al menos dos letras en mayúscula y no todas en mayúscula")
        return True


class Validador:
    def __init__(self, regla):
        self._regla = regla

    def es_valida(self, clave):
        return self._regla.es_valida(clave)


