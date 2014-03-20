# -*- coding: utf-8 -*-

import locale

from os.path import join, dirname
from PIL.Image import open as pilopen

from cubicweb import Binary, Unauthorized
from cubicweb.devtools.testlib import CubicWebTC


class FileTC(CubicWebTC):

    def test_set_mime_and_encoding(self):
        fobj = self.request().create_entity('File', data_name=u"foo.txt", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'text/plain')
        self.assertEqual(fobj.data_encoding, self.request().encoding)

    def test_set_mime_and_encoding_gz_file(self):
        fobj = self.request().create_entity('File', data_name=u"foo.txt.gz", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'text/plain')
        self.assertEqual(fobj.data_encoding, u'gzip')
        fobj = self.request().create_entity('File', data_name=u"foo.txt.gz", data=Binary("xxx"),
                               data_format='application/gzip')
        self.assertEqual(fobj.data_format, u'text/plain')
        self.assertEqual(fobj.data_encoding, u'gzip')
        fobj = self.request().create_entity('File', data_name=u"foo.gz", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'application/gzip')
        self.assertEqual(fobj.data_encoding, None)


    def test_set_mime_and_encoding_bz2_file(self):
        fobj = self.request().create_entity('File', data_name=u"foo.txt.bz2", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'text/plain')
        self.assertEqual(fobj.data_encoding, u'bzip2')
        fobj = self.request().create_entity('File', data_name=u"foo.txt.bz2", data=Binary("xxx"),
                               data_format='application/bzip2')
        self.assertEqual(fobj.data_format, u'text/plain')
        self.assertEqual(fobj.data_encoding, u'bzip2')
        fobj = self.request().create_entity('File', data_name=u"foo.bz2", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'application/bzip2')
        self.assertEqual(fobj.data_encoding, None)

    def test_set_mime_and_encoding_unknwon_ext(self):
        fobj = self.request().create_entity('File', data_name=u"foo.123", data=Binary("xxx"))
        self.assertEqual(fobj.data_format, u'application/octet-stream')
        self.assertEqual(fobj.data_encoding, None)


class ImageTC(CubicWebTC):

    @property
    def data(self):
        return file(join(dirname(__file__), 'data', '20x20.gif')).read()

    def test_resize_image(self):
        # check no resize
        img = self.request().create_entity('File', data=Binary(self.data), data_name=u'20x20.gif')
        self.assertEqual(img.data_format, u'image/gif')
        self.assertEqual(img.data.getvalue(), self.data)
        # check thumb
        self.set_option('image-thumb-size', '5x5')
        pilthumb = pilopen(img.cw_adapt_to('IImage').thumbnail(shadow=False))
        self.assertEqual(pilthumb.size, (5, 5))
        self.assertEqual('PNG', pilthumb.format)
        # check resize 10x5
        self.set_option('image-max-size', '10x5')
        img = self.request().create_entity('File', data=Binary(self.data), data_name=u'20x20.gif')
        self.assertEqual(img.data_format, u'image/gif')
        pilimg = pilopen(img.data)
        self.assertEqual(pilimg.size, (5, 5))
        # also on update
        img.set_attributes(data=Binary(self.data))
        img.cw_clear_all_caches()
        pilimg = pilopen(img.data)
        self.assertEqual(pilimg.size, (5, 5))
        # test image smaller than max size
        self.set_option('image-max-size', '40x40')
        img.set_attributes(data=Binary(self.data))
        pilimg = pilopen(img.data)
        self.assertEqual(pilimg.size, (20, 20))

class Sha1TC(CubicWebTC):

    def test_init_sha1(self):
        req = self.request()

        req.vreg.config['compute-sha1hex'] = 0
        fobj = req.create_entity('File', data_name=u"foo.txt", data=Binary("xxx"))
        self.assertEqual(None, fobj.data_sha1hex)

        req.vreg.config['compute-sha1hex'] = 1
        fobj = req.create_entity('File', data_name=u"foo.txt", data=Binary("xxx"))
        self.assertEqual(u'b60d121b438a380c343d5ec3c2037564b82ffef3', fobj.data_sha1hex)

    def test_modify_data(self):
        req = self.request()
        req.vreg.config['compute-sha1hex'] = 1
        fobj = req.create_entity('File', data_name=u"foo.txt", data=Binary("xxx"))
        fobj.cw_set(data=Binary('yyy'))
        self.assertEqual(u'186154712b2d5f6791d85b9a0987b98fa231779c', fobj.data_sha1hex)

    def test_manual_set_sha1_forbidden(self):
        self.skip('Enable me when we can forbid to set an attribute at entity creation')
        with self.assertRaises(Unauthorized):
            self.request().create_entity('File', data_name=u"foo.txt", data=Binary("xxx"),
                                         data_sha1hex='0'*40)

if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
