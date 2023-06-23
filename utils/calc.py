import decimal
from decimal import Decimal
from functools import wraps

from .error_code_msg import CodeError
from utils.logger import setup_log


logger = setup_log("utils_calc")
context = decimal.getcontext()
context.prec = 36
context.rounding = decimal.ROUND_HALF_UP
decimal.setcontext(context)


class CalcDecorator(object):

    def __init__(self):
        pass

    def __call__(self, func):
        @wraps(func)
        def decorated(*args, **kwargs):
            try:
                (obj, obj2) = ('', '')
                if len(args) == 1:
                    (obj,) = args
                if len(args) == 2:
                    (obj, obj2) = args
                # print(type(obj), type(obj2))
                prec = context.prec
                rounding = context.rounding
                if func.__name__ != '__truediv__':
                    place = obj.numeric_places(obj2, func.__name__)
                    context.prec = place

                if func.__name__ == 'numeric':
                    if obj2 is False:
                        context.rounding = decimal.ROUND_DOWN
                # print(func.__name__, place)
                result = func(*args, **kwargs)
                context.prec = prec
                context.rounding = rounding

                return result
            except Exception as e:
                logger.exception(e)
                raise CodeError.CALC_ERROR

        return decorated


class Calc(object):
    calc_place = None

    def __init__(self, value, place=None):
        self.value = Decimal(str(value).replace(",", ""))
        self.calc_place = place
        pass

    def no_zero_str(self):
        place = str(self.value).split('.')[-1]
        if place:
            if int(place) == 0:
                return str(self.value).split('.')[0]
        return str(self.value)

    def evalue(self, value):
        e_value = str(value).lower()
        if 'e-' in e_value:
            v1 = e_value
            item = int(v1[v1.find('e-') + 2: len(v1)]) + int(
                len(v1[0:v1.find('e-') - (len(v1.split('.')[0]) if '.' in v1 else 0) - 1]))
            e_value = f"%.{item}f" % (float(v1))

        if 'e+' in e_value:
            v1 = e_value
            item = int(v1[v1.find('e+') + 2: len(v1)]) + (len(v1.split('.')[0]) if ('.' in v1) else 1)
            e_value = f"%{item}f" % (float(v1))
        return e_value

    def places(self, value):

        if type(value) == int:
            return len(str(value))

        e_value = self.evalue(value)

        if '.' not in str(e_value):
            return len(str(e_value))

        values = str(e_value).split('.')
        slen = len(str(values[0]))
        ilen = len(values[1])
        if ilen <= 8:
            return ilen + slen

        lvalue = values[1][0:(ilen - 1)]

        if lvalue.endswith('00000') and (ilen + slen) > 15:
            ilen = len(lvalue.rstrip('0'))
            ilen = ilen if (ilen) > 0 else 1
            return ilen + slen

        if lvalue.endswith('99999') and (ilen + slen) > 15:
            ilen = len(lvalue.rstrip('9'))
            ilen = ilen if (ilen) > 0 else 1
            return ilen + slen

        return ilen + slen

    def numeric_places(self, value, fname=None):
        if isinstance(value, Calc):
            if (self.calc_place is not None) or (value.calc_place is not None):
                return self.calc_place if (value.calc_place is None) else (
                    value.calc_place if (self.calc_place is None) else max(self.calc_place, value.calc_place))
            if fname == '__mul__':
                return self.places(self.value) + self.places(value.value)
            else:
                return max(self.places(self.value), self.places(value.value))
        else:
            if self.calc_place is not None:
                return self.calc_place

            if fname == '__mul__':
                return self.places(self.value) + self.places(value)
            else:
                return max(self.places(self.value), self.places(value))

    @CalcDecorator()
    def __str__(self):
        return self.evalue(self.value)  # f"%.{self.places(self.value)}f"%(float(self.value))

    @CalcDecorator()
    def numeric(self, up=True):
        values = str(self.value).split('.')
        if len(values) <= 1:
            return float(values[0])
        else:
            if context.rounding == decimal.ROUND_HALF_UP:
                return float(f"%.{context.prec}f" % (float(self.evalue(self.value))))
            else:
                ilen = len(values[1])
                ilen = min(ilen, context.prec)
                ilen0 = max(len(values[0]), 1)
                ilen = min(17 - ilen0 - 1, ilen)
                exvalue = ""
                ex = ","
                if 'e' in values[1]:
                    ex = "e"
                    exvalue = 'e' + values[1].split('e')[1]
                if 'E' in values[1]:
                    ex = "E"
                    exvalue = 'E' + values[1].split('E')[1]

                value = f"{values[0]}.{values[1][0:ilen]}"
                value = value.split(ex)[0]
                value = value + f"{exvalue}"
                value = value.replace('ee', 'e')
                value = value.replace('EE', 'E')
                return float(f"{value}")

    @staticmethod
    def get_num_by_prec(f_str, prec):
        """
        :param f_str: 传入的数字
        :param prec: 精度
        :return:
        """
        f_str = str(f_str)
        a, b, c = f_str.partition('.')
        c = (c + "0" * prec)[:prec]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
        return ".".join([a, c])

    # 加
    @CalcDecorator()
    def __add__(self, other):

        if isinstance(other, Calc):
            # print(context.prec,self.value , other.value)
            value = self.value + other.value
        else:
            # print(context.prec,self.value , other)
            value = self.value + Decimal(str(other))
        '''
        if(isinstance(other, Calc)):
            value = (self.value*place*10 + other.value*place*10)/(place*10)
        else:
            value = (self.value*place*10 +  other*place*10)/(place*10)
        '''
        return value

    # 减
    @CalcDecorator()
    def __sub__(self, other):

        if isinstance(other, Calc):
            # print(context.prec,self.value , other.value)
            value = self.value - other.value
        else:
            # print(context.prec,self.value , other)
            value = self.value - Decimal(str(other))

        return value

    # 乘
    @CalcDecorator()
    def __mul__(self, other):

        if isinstance(other, Calc):
            # print(context.prec,self.value , other.value)
            value = (self.value * other.value)
        else:
            # print(context.prec, self.value , other)
            value = (self.value * Decimal(str(other)))

        return value

    # 除
    @CalcDecorator()
    def __truediv__(self, other):

        if isinstance(other, Calc):
            # print(context.prec,self.value , other.value)
            value = (self.value / other.value)
        else:
            # print(context.prec,self.value * other)
            value = (self.value / Decimal(str(other)))

        return value

    # 模
    @CalcDecorator()
    def __mod__(self, other):

        if isinstance(other, Calc):
            # print(context.prec,self.value , other.value)
            value = self.value % other.value
        else:
            # print(context.prec,self.value * other)
            value = self.value % Decimal(str(other))
        return value
