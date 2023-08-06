# -*- coding: utf-8 -*-

# import conftest

from serprog import ihex
# from distutils import dir_util
# import pytest
# import os


# @pytest.fixture
# def datadir(tmpdir, request):
#     '''
#     Fixture responsible for searching a folder with the same name of test
#     module and, if available, moving all contents to a temporary directory so
#     tests can use them freely.
#     '''
#     filename = request.module.__file__
#     test_dir, _ = os.path.splitext(filename)

#     if os.path.isdir(test_dir):
#         dir_util.copy_tree(test_dir, str(tmpdir))

#     return tmpdir


def test_ihex_parse_1():
    """測試分析單一區段ihex檔案
    """
    predict = [
        {
            'address': 0x0000,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        }
    ]

    # test_ihex_file = datadir.join('ihex1.hex')
    real = ihex.parse('test/ihex1.hex')
    # print(real)
    assert(real == predict)


def test_ihex_parse_2():
    """測試分析雙區段ihex檔案
    """
    predict = [
        {
            'address': 0x0000,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        },
        {
            'address': 0x0100,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        }
    ]

    # test_ihex_file = datadir.join('ihex2.hex')
    real = ihex.parse('test/ihex2.hex')
    # print(real)
    assert(real == predict)


def test_ihex_parse_3():
    """測試分析有擴展位址ihex檔案
    第一段無擴展，高2位元組為0x0000
    第二段有擴展，高2位元組為0xABCD
    """
    predict = [
        {
            'address': 0x00000000,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        },
        {
            'address': 0xABCD0100,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        }
    ]

    # test_ihex_file = datadir.join('ihex3.hex')
    real = ihex.parse('test/ihex3.hex')
    # print(real)
    assert(real == predict)


def test_ihex_padding_1():
    """測試補其空白函式，補其單頁
    """
    input = [
        {
            'address': 0,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        },
        {
            'address': 0xABCD0010,
            'data': b'\x01\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        }
    ]
    space_data = bytes.fromhex('FF')
    page_size = 256

    space_padding = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
    predict = [
        {
            'address': 0,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F' + space_padding * 15
        },
        {
            'address': 0xABCD0000,
            'data': space_padding + b'\x01\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F' + space_padding * 14
        }
    ]

    real = ihex.padding_space(input, page_size, space_data)
    assert(real == predict)


def test_ihex_padding_2():
    """測試補其空白函式，補其多頁
    """
    input = [
        {
            'address': 3,
            'data': b'\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C'
        }
    ]
    space_data = bytes.fromhex('FF')
    page_size = 4

    predict = [
        {
            'address': 0,
            'data': b'\xFF\xFF\xFF\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\xFF\xFF\xFF'
        }
    ]

    real = ihex.padding_space(input, page_size, space_data)
    assert(real == predict)


def test_ihex_cut_1():
    """測試切割頁面函式
        NOTE: 此函式輸入資料須為經過padding之codeblock
              大小須符合 pgsz * N
    """

    input = [
        {
            'address': 0,
            'data': b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        },
        {
            'address': 0xABCD0010,
            'data': b'\x01\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F'
        }
    ]
    space_data = bytes.fromhex('FF')
    page_size = 4

    space_padding = b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'
    predict = [
        {
            'address': 0,
            'data': b'\x00\x01\x02\x03'
        },
        {
            'address': 4,
            'data': b'\x04\x05\x06\x07'
        },
        {
            'address': 8,
            'data': b'\x08\x09\x0A\x0B'
        },
        {
            'address': 12,
            'data': b'\x0C\x0D\x0E\x0F'
        },
        {
            'address': 0xABCD0010,
            'data': b'\x01\x01\x02\x03'
        },
        {
            'address': 0xABCD0014,
            'data': b'\x04\x05\x06\x07'
        },
        {
            'address': 0xABCD0018,
            'data': b'\x08\x09\x0A\x0B'
        },
        {
            'address': 0xABCD001C,
            'data': b'\x0C\x0D\x0E\x0F'
        }
    ]

    real = ihex.cut_to_pages(input, page_size)
    assert(real == predict)

if __name__ == '__main__':
    test_ihex_parse_1()
    test_ihex_parse_2()
    test_ihex_parse_3()
    test_ihex_padding_1()
    test_ihex_padding_2()
    test_ihex_cut_1()
