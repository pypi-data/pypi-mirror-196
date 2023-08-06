class SystemBaseError(Exception):
    pass

class NumericSystems:
    """
    Class with methods, that allow to work with uncomfortable numeric systems. (base > 36)
    Better to use UPPERCASE LETTERS!!!
    """
    __SYMBOLS = {10: 'A', 11: 'B',
                 12: 'C', 13: 'D',
                 14: 'E', 15: 'F',
                 16: 'G', 17: 'H',
                 18: 'I', 19: 'J',
                 20: 'K', 21: 'L',
                 22: 'M', 23: 'N',
                 24: 'O', 25: 'P',
                 26: 'Q', 27: 'R',
                 28: 'S', 29: 'T',
                 30: 'U', 31: 'V',
                 32: 'W', 33: 'X',
                 34: 'Y', 35: 'Z'}

    @classmethod
    def create_advanced_dictionary(cls, system_base=37) -> dict:
        """
        Creates a dict with advanced symbols for unusual systems using Unicode.
        """ 
        if 11 <= system_base <= 36:
            return cls.__SYMBOLS
        elif system_base <= 10:
            raise SystemBaseError("This func is used for system bases more than 10,\nYou do not need andvanced symbols for system with base <= 10.") 
        advanced_symbols = {}
        start_n, start_c = 90, 36
        i = 1
        while i < system_base - 35:
            if chr(start_n + i).isprintable():
                advanced_symbols[start_c] = chr(start_n + i)
                start_c += 1
                i += 1
            start_n += 1
        return cls.__SYMBOLS | advanced_symbols

    @classmethod
    def convert_to_decimal(cls, number_in_current_sys: str, base: int) -> int:
        """
        Converts a number in system with specified base into decimal number.
        """
        if 2 <= base <= 10:
            return int(number_in_current_sys, base)
        
        result = 0
        advanced = cls.create_advanced_dictionary(base) if base > 10 else None
        for i in number_in_current_sys:
            if i.upper() not in list(advanced.keys()):
                raise SystemBaseError(f"Ivalid literal for system with base {base}")       
            
        reversed_number = number_in_current_sys[::-1]
        for i in range(len(number_in_current_sys)):
            if reversed_number[i] not in list('0123456789'):
                result += (list(advanced.values()).index(reversed_number[i]) + 10) * base ** i
            else:
                result += int(reversed_number[i]) * base ** i
        return result

    @classmethod
    def from_decimal_to(cls, base: int, decimal_number: int) -> str:
        """
        Converts a decimal number into number in system with specified base.
        """
        for i in str(decimal_number):
            if i not in '0123456789':
                raise SystemBaseError("Invalid literal for sysyem with base 10")
            
        result = ''
        advanced = cls.create_advanced_dictionary(base) if base > 10 else None
        while decimal_number:
            rest = decimal_number % base
            if str(rest) not in list('0123456789'):
                result += advanced[rest]
            else:
                result += str(decimal_number % base)
            decimal_number //= base
        return result[::-1]