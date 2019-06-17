import pytest
from lomosplit.utils import get_grouped_images


def test_get_grouped_images_empty(tmpdir):
    assert get_grouped_images(tmpdir.dirpath()) == []


def test_get_grouped_images(tmpdir):
    tmpdir.join('dog.png').write_binary(b'test content')
    tmpdir.mkdir('a')
    tmpdir.mkdir('b')
    tmpdir.join('a').mkdir('aa')
    tmpdir.join('a').mkdir('ab')
    tmpdir.join('a').join('test.txt').write('test content')
    tmpdir.join('a').join('test.png').write_binary(b'test content')
    tmpdir.join('a').join('test.jpg').write_binary(b'test content')
    tmpdir.join('a').join('test.jpeg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('test_1.jpg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('test_2.jpg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('test_3.jpg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('test_4.jpg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('test_5.jpg').write_binary(b'test content')
    tmpdir.join('a').join('aa').join('.DS_Store').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('000.bmp').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('001.bmp').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('002.png').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('003.jpg').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('004.tiff').write_binary(b'test content')
    tmpdir.join('a').join('ab').join('thumbs.db').write_binary(b'test content')
    tmpdir.join('b').join('test.txt').write('test content')
    tmpdir.join('b').join('test.npy').write_binary(b'test content')
    tmpdir.join('b').join('test.bin').write_binary(b'test content')

    assert get_grouped_images(tmpdir.realpath()) == [
        ('.', ['dog.png']),
        ('a', [
            'test.jpeg',
            'test.jpg',
            'test.png'
        ]),
        ('a/aa', [
            'test_1.jpg',
            'test_2.jpg',
            'test_3.jpg',
            'test_4.jpg',
            'test_5.jpg',
        ]),
        ('a/ab', [
            '000.bmp',
            '001.bmp',
            '002.png',
            '003.jpg',
            '004.tiff',
        ])
    ]
