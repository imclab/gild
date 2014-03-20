#coding: utf-8

from os.path import join, dirname, isfile, exists
import shutil

from cubicweb.devtools.testlib import CubicWebTC

from cubicweb import ValidationError, NoSelectableObject, Binary, Unauthorized

from cubes.file.entities import thumb_cache_dir

class FileTC(CubicWebTC):

    def setup_database(self):
        create = self.request().create_entity
        self.fobj = create('File', data_name=u"foo.pdf",
                                   data=Binary("xxx"),
                                   data_format=self.mime_type)
        self.ufobj = create('File', data_name=u"Bâbâr.pdf",
                                    data=Binary("yyy"),
                                    data_format=self.mime_type)

    icon = 'text.ico'
    mime_type = u"text/plain"


    def test_idownloadable(self):
        idownloadable = self.fobj.cw_adapt_to('IDownloadable')
        self.assertEqual(idownloadable.download_data(), 'xxx')
        self.assertEqual(idownloadable.download_url(),
                          u'http://testing.fr/cubicweb/%s/%s/raw/%s' % (
            self.fobj.__regid__.lower(), self.fobj.eid, self.fobj.data_name))
        self.assertEqual(idownloadable.download_content_type(), self.mime_type)

    def test_idownloadable_unicode(self):
        idownloadable = self.ufobj.cw_adapt_to('IDownloadable')
        self.assertEqual(idownloadable.download_url(),
                          u'http://testing.fr/cubicweb/%s/%s/raw/%s'
                          % (self.ufobj.__regid__.lower(),
                             self.ufobj.eid,
                             self.ufobj.data_name.replace(u'â', '%C3%A2')))

    def test_base(self):
        self.assertEqual(self.fobj.size(), 3)
        self.assertEqual(self.fobj.icon_url(),
                          'http://testing.fr/cubicweb/data/icons/'+self.icon)

    def test_views(self):
        self.vreg['views'].select('download', self.fobj._cw, rset=self.fobj.cw_rset)
        self.fobj.view('gallery')
        self.assertRaises(NoSelectableObject, self.fobj.view, 'image')
        self.assertRaises(NoSelectableObject, self.fobj.view, 'album')

    def test_sha1hex(self):
        self.create_user(self.request(), login='simpleuser')
        self.commit()
        with self.login('simpleuser'):
            req = self.request()
            req.vreg.config['compute-sha1hex'] = 1
            obj = req.create_entity('File', data_name=u"myfile.pdf",
                                    data=Binary("xxx"),
                                    data_format=self.mime_type)
            self.commit()
            self.assertEqual('b60d121b438a380c343d5ec3c2037564b82ffef3', obj.compute_sha1hex())
            self.assertEqual('b60d121b438a380c343d5ec3c2037564b82ffef3', obj.data_sha1hex) # can read
            with self.assertRaises(Unauthorized):
                # write is forbiden
                obj.cw_set(data_sha1hex=u'1234')
                self.commit()
            obj.cw_set(data=Binary('zzz'))
            self.assertEqual('40fa37ec00c761c7dbb6ebdee6d4a260b922f5f4', obj.data_sha1hex)
            with self.assertRaises(Unauthorized):
                req.create_entity('File', data_name=u'anotherfile.pdf',
                                  data=Binary('yyy'),
                                  data_format=self.mime_type,
                                  data_sha1hex=u'deadbeef')
                self.commit()

    def test_sha1hex_nodata(self):
        with self.session.deny_all_hooks_but('metadata'):
            req = self.request()
            req.vreg.config['compute-sha1hex'] = 1
            obj = req.create_entity('File')
            self.commit()
        self.assertEqual(None, obj.data)
        self.assertEqual(None, obj.data_sha1hex)
        self.assertEqual(None, obj.compute_sha1hex())

class ImageTC(CubicWebTC):
    icon = 'image_png.ico'
    mime_type = u"image/png"

    @property
    def data(self):
        return file(join(dirname(__file__), 'data', '20x20.gif')).read()

    def setUp(self):
        super(ImageTC, self).setUp()
        cachedir = thumb_cache_dir(self.session.vreg.config)
        if exists(cachedir):
            shutil.rmtree(cachedir)
        self.cachedir = cachedir

    def tearDown(self):
        super(ImageTC, self).tearDown()
        if exists(self.cachedir):
            shutil.rmtree(self.cachedir)

    def setup_database(self):
        create = self.request().create_entity
        self.fobj = create('File', data_name=u"foo.gif", data=Binary("xxx"),
                                    data_format=self.mime_type)
        self.ufobj = create('File', data_name=u"Bâbâr.png",
                                    data=Binary("yyy"),
                                    data_format=self.mime_type)

    def test_views(self):
        self.vreg['views'].select('download', self.fobj._cw, rset=self.fobj.cw_rset)
        self.fobj.view('gallery')
        self.fobj.view('image')
        self.fobj.view('album')

    def test_thumbnail_generation_fails(self):
        ithumb = self.fobj.cw_adapt_to('IThumbnail')
        # the actual thumbnail generation fails because the actual
        # file content is (literally) "xxx"
        self.assertEqual(ithumb.thumbnail_data(), '')
        self.assertEqual(u'http://testing.fr/cubicweb/%s/%s/thumb/foo_75x75.png' %
                         (self.fobj.__regid__.lower(), self.fobj.eid),
                         ithumb.thumbnail_url())

    def test_thumbnail(self):
        cachedir = self.cachedir
        img = self.request().create_entity('File', data=Binary(self.data), data_name=u'20x20.gif')
        self.commit()
        thumbadapter = img.cw_adapt_to('IThumbnail')
        self.assertEqual('20x20_75x75.png', thumbadapter.thumbnail_file_name())
        self.assertEqual('http://testing.fr/cubicweb/file/%s/thumb/20x20_75x75.png' % img.eid,
                         thumbadapter.thumbnail_url())
        cachepath = thumbadapter._thumbnail_path()
        self.assertNone(thumbadapter.thumbnail_path())
        self.assertFalse(isfile(cachepath))

        req = self.request()
        img = req.execute('File F WHERE F data_name="20x20.gif"').get_entity(0,0)
        thumbadapter = img.cw_adapt_to('IThumbnail')
        self.assertTrue(thumbadapter.thumbnail_data())
        cachepath = thumbadapter.thumbnail_path()
        self.assertTrue(isfile(cachepath))
        self.assertEqual(open(cachepath, 'rb').read(), thumbadapter.thumbnail_data())


class MimeTypeDetectionTC(CubicWebTC):

    def test_extra_dot(self):
        fobj = self.request().create_entity('File', data_name=u"foo.toto.pdf",
                                                 data=Binary("xxx"))
        self.assertEqual(fobj.data_format, 'application/pdf')

    def test_file_name_priority(self):
        req = self.request()
        req.form = {'eid': ['X'], '__maineid' : 'X',

                    '__type:X': 'File',
                    '_cw_entity_fields:X': 'data-subject,data_name-subject',
                    'data-subject:X': (u'coucou.txt', Binary('coucou')),
                    'data_name-subject:X': u'coco.txt',
                    }
        path, params = self.expect_redirect_handle_request(req, 'edit')
        self.assertTrue(path.startswith('file/'), path)
        eid = path.split('/')[1]
        efile = req.entity_from_eid(eid)
        self.assertEqual(efile.data_name, 'coco.txt')


if __name__ == '__main__':
    from logilab.common.testlib import unittest_main
    unittest_main()
