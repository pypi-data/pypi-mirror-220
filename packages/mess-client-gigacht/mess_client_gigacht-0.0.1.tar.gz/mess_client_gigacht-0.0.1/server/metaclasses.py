import dis


# Метакласс для проверки соответствия сервера:
class ServerVerifier(type):
    '''
    Metaclass to check server class.
    Checks if connect() is not called and that TCP protocol is used
    '''

    def __init__(self, clsname, bases, clsdict):
        # clsname - экземпляр метакласса - Server
        # bases - кортеж базовых классов - ()
        # clsdict - словарь атрибутов и методов экземпляра метакласса

        # Список методов, которые используются в функциях класса:
        methods = []
        # Атрибуты, используемые в функциях классов
        attrs = []
        # перебираем ключи
        for func in clsdict:
            # Пробуем
            try:
                # Возвращает итератор по инструкциям в предоставленной функции
                # , методе, строке исходного кода или объекте кода.
                instructions = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
                # (если порт)
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы и
                # атрибуты.
                for i in instructions:
                    # opname - имя для операции
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            # заполняем список методами, использующимися в
                            # функциях класса
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        if i.argval not in attrs:
                            # заполняем список атрибутами, использующимися в
                            # функциях класса
                            attrs.append(i.argval)
        # Если обнаружено использование недопустимого метода connect, бросаем
        # исключение:
        if 'connect' in methods:
            raise TypeError('Method connect() is not allowed in server class')
        # Если сокет не инициализировался константами SOCK_STREAM(TCP)
        # AF_INET(IPv4), тоже исключение.
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError(
                'Socket has no SOCK_STREAM and AF_INET attributes.')
        # Обязательно вызываем конструктор предка:
        super().__init__(clsname, bases, clsdict)
