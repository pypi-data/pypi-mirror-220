import dis

# Метакласс для проверки корректности клиентов:


class ClientVerifier(type):
    '''
    Metaclass to check client class.
    Checks if there is no calls of accept() and listen()
    and socket objet is not created inside class.
    '''

    def __init__(self, clsname, bases, clsdict):
        # Список методов, которые используются в функциях класса:
        methods = []
        for func in clsdict:
            # Пробуем
            try:
                instructions = dis.get_instructions(clsdict[func])
                # Если не функция то ловим исключение
            except TypeError:
                pass
            else:
                # Раз функция разбираем код, получая используемые методы.
                for i in instructions:
                    if i.opname == 'LOAD_GLOBAL':
                        if i.argval not in methods:
                            methods.append(i.argval)
        # Если обнаружено использование недопустимого метода accept, listen,
        # socket бросаем исключение:
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError(
                    'Methods accept(), listen() or socket() are not allowed in this class')
        super().__init__(clsname, bases, clsdict)
