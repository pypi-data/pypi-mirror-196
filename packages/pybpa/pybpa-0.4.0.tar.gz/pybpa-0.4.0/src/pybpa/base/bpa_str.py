#!/usr/bin/python
# -*- coding: gbk -*-


BPA_LINE_LEN = 80  # �ȶ�5.3�汾��80��5.7�汾��86

def str_slice(str, field_obj):
    n1 = field_obj.sp - 1
    n2 = field_obj.ep
    try:
        rstr = str[n1:n2].strip()
    except:
        rstr = ''
    return rstr


# ���ַ���ת�ɸ����͵�ʱ�򣬰ѿո񿴳�0
def str2float(str):
    v = 0.
    try:
        v = float(str)
    except:
        pass
    return v


# ���ַ���ת�����͵�ʱ�򣬰ѿո񿴳�0
def str2int(str):
    v = 0
    try:
        v = int(str)
    except:
        pass
    return v


# �����µ��ַ�����ӳ���ݸ���
# field ���ڵ����ݿ���, name �µ����ݿ���ֵ
# ����ģʽm, ����PZʱ������λС��������һλ
# m=-1, ����ԭС����
def str_replace(str_data, value, field, m=-1):  # **args):
    """

    @param str_data:
    @param value:
    @param field:
    @param m:
    @return:
    """
    n1 = field.sp - 1
    n2 = field.ep
    n3 = n2 - n1

    # m = -1
    # if args.get('dec'):
    #    m = args.get('dec')

    if type(value) in [float, int]:  # ���������
        if m == 0:
            str_rep = str(int(round(value, 0)))
        elif m > 0:
            str_rep = str(round(value, m))
        else:
            str_rep = str(value)

        if len(str_rep) > n3:
            if str_rep[0:2] == '0.':
                if len(str_rep) == n3 + 1:
                    str_rep = str_rep[1:]
                elif round(float(str_rep), n3 - 1) == 1.0:
                    str_rep = '1.0'
                else:  # ��������
                    str_rep = str(round(float(str_rep), n3 - 1))[1:]
            elif str_rep[0:3] == '-0.':  # ��������
                str_rep = str(round(float(str_rep), n3 - 2))
                str_rep = '-.' + str_rep[3:]
        str_rep = str_rep[0:n3].rjust(n3)
    else:  # ������ַ���
        str_rep = value
        str_rep = str_rep[0:n3].ljust(n3)

    rev_data_str = str_data[0:n1].ljust(n1) + str_rep + str_data[n2:]
    return rev_data_str


# ��piece_str�ַ����滻str��Ӧλ��
# strԭ�����ִ�, piece_strҪд������
def str_join(line_str, piece_str, field):
    """
    ��piece_str�滻line_str��fieldλ��
    @param line_str: 
    @param piece_str: 
    @param field: 
    @return: 
    """
    n1 = field.sp - 1
    n2 = field.ep
    n3 = n2 - n1
    piece_str = piece_str[0:n3]
    piece_str = piece_str.ljust(n3)
    return line_str[0:n1].ljust(n1) + piece_str + line_str[n2:]


def bpa_str2float(s: str, f: int = None, default: float = 0):
    """
    F6.5����ʾҪ������һ����������ռ�е��������Ϊ6�У�ȱʡС������λ��Ϊ5λ��
    ������롮123456��������û��С���㣬�����ȱʡ����Ϊ1.23456��������롮10������������ȱʡ����ǰ���Զ����㣬С������ȡ5λ�����������0.00010��
    ������롮10.����������С���㣬��������Ϊ10.0�������д��.12345�������������Ϊ0.12345��
    �����д�ĸ�����û��ռ��ָ�����У�����ڸ�ʽF6.5���롮10.����3�У�����Կո���������пո�Ĵ�����һ�¡�
    @param default:
    @param f:
    @param s:
    @return:
    """
    length = len(s)
    s = s.strip()
    if s:
        return (float(s + '0')) if '.' in s else (float(s) / (10 ** f))
    else:
        if default is None:
            raise ValueError('���ڷ��գ�')
        return default


def bpa_str(s: str):
    return s.strip()


def bpa_str2int(s: str, default: int = None):
    s = s.strip()
    if len(s) > 0:
        return int(s)
    else:
        if default is None:
            raise ValueError('���ڷ��գ�')
        return default


def bpa_str2x(s: str, t: type, f: int = None, default = None):
    if t == str:
        return bpa_str(s)
    elif t == int:
        return bpa_str2int(s, default=default)
    elif t == float:
        return bpa_str2float(s, f, default)


def bpa_card_line(bline: str):
    """
    �淶��bpa�ļ��С�
    ���ڲ��Ǵ����е��У���������ļ��У�
    1. ȥ����ĩ�����������Ŀո�\r��\n, \t
    2. �ÿո��뵽BPA_LINE_LEN����
    """
    return bline.strip().ljust(BPA_LINE_LEN)


class FFFloat2Str:
    def __init__(self, w, d):
        self.w = w
        self.d = d
        self.max = 10 ** (w - (1 if d else 0))
        self.min = -1 * 10 ** (w - 1 - (1 if d else 0))
        self.pfull = 10 ** (w - d - 1)
        self.nfull = -1 * 10 ** (w - d - 2)

    def write(self, fl):
        f = fl[0]
        if not f:
            return ' ' * self.w
        assert self.min < f < self.max

        f += 0.0
        if self.pfull < f < self.pfull * 10 or 10 * self.nfull < f < self.nfull:
            f *= 10 ** (3 * self.d)
            return ('{:.' + str(self.w) + 'f}').format(f)[:self.w].ljust(self.w)

        s = ('{:.' + str(self.w) + 'f}').format(abs(f))
        if s[:2] == '0.':
            s = s[1:]
        if f < 0:
            s = '-' + s
        return s[:self.w].ljust(self.w)


if __name__ == '__main__':
    import fortranformat as ff
    class t:
        def __init__(self, w, b):
            self.a = ff.FortranRecordReader('F' + str(w) + '.' + str(b))
            self.b = FFFloat2Str(w, b)
        def w(self, f):
            h = self.b.write([f])
            g = self.a.read(h)[0]
            return g == f, '\t'.join([str(f), h, str(g)])

    a = FFFloat2Str(6, 5)  # todo F6.5  ��.00008,д����8.0000
    print(a.write([.00008]))
    print(a.write([-321.12345]))
    print(a.write([.12345]))
    print(a.write([-.12345]))
    #
    # b = t(5, 4)
    # for i in range(1000000):
    #     f, s = b.w(i / 10000)
    #     if not f:
    #         print(i, '\t' + s)
