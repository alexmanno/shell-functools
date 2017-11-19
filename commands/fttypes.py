class TypeConversionError(Exception):
    def __init__(self, type_from, type_to):
        self.type_from = type_from
        self.type_to = type_to


class TypedValue:
    def __init__(self, value, fttype):
        self.value = value
        self.fttype = fttype


class FtType:
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__[2:]

    def create_from(self, inp):
        raise NotImplementedError


class FtString(FtType):
    def create_from(self, inp):
        if inp.fttype == T_STRING:
            return inp

        raise TypeConversionError(inp.fttype, T_STRING)


class FtArray(FtType):
    def create_from(self, inp):
        if inp.fttype == T_ARRAY:
            return inp
        elif inp.fttype == T_STRING:
            return TypedValue(inp.value.split("\t"), T_ARRAY)

        raise TypeConversionError(inp.fttype, T_ARRAY)


class FtPath(FtType):
    def create_from(self, inp):
        if inp.fttype == T_STRING or inp.fttype == T_PATH:
            return TypedValue(inp.value, T_PATH)

        raise TypeConversionError(inp.fttype, T_PATH)


class FtBool(FtType):
    def create_from(self, inp):
        if inp.fttype == T_BOOL:
            return inp
        elif inp.fttype == T_STRING:
            val = False
            if inp.value == "true" or inp.value == "True":
                val = True
            return TypedValue(val, T_BOOL)

        raise TypeConversionError(inp.fttype, T_BOOL)


class FtInt(FtType):
    def create_from(self, inp):
        if inp.fttype == T_INT:
            return inp
        elif inp.fttype == T_STRING:
            try:
                return TypedValue(int(inp.value), T_INT)
            except ValueError:
                raise TypeConversionError

        raise TypeConversionError(inp.fttype, T_INT)


T_STRING = FtString()
T_ARRAY = FtArray()
T_PATH = FtPath()
T_BOOL = FtBool()
T_INT = FtInt()
