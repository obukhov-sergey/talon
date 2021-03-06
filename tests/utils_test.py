# coding:utf-8

from . import *

from talon import utils as u
import cchardet


def test_get_delimiter():
    eq_('\r\n', u.get_delimiter('abc\r\n123'))
    eq_('\n', u.get_delimiter('abc\n123'))
    eq_('\n', u.get_delimiter('abc'))


def test_unicode():
    eq_ (u'hi', u.to_unicode('hi'))
    eq_ (type(u.to_unicode('hi')), unicode )
    eq_ (type(u.to_unicode(u'hi')), unicode )
    eq_ (type(u.to_unicode('привет')), unicode )
    eq_ (type(u.to_unicode(u'привет')), unicode )
    eq_ (u"привет", u.to_unicode('привет'))
    eq_ (u"привет", u.to_unicode(u'привет'))
    # some latin1 stuff
    eq_ (u"Versión", u.to_unicode('Versi\xf3n', precise=True))


def test_detect_encoding():
    eq_ ('ascii', u.detect_encoding('qwe').lower())
    eq_ ('iso-8859-2', u.detect_encoding('Versi\xf3n').lower())
    eq_ ('utf-8', u.detect_encoding('привет').lower())
    # fallback to utf-8
    with patch.object(u.chardet, 'detect') as detect:
        detect.side_effect = Exception
        eq_ ('utf-8', u.detect_encoding('qwe').lower())


def test_quick_detect_encoding():
    eq_ ('ascii', u.quick_detect_encoding('qwe').lower())
    eq_ ('windows-1252', u.quick_detect_encoding('Versi\xf3n').lower())
    eq_ ('utf-8', u.quick_detect_encoding('привет').lower())


@patch.object(cchardet, 'detect')
@patch.object(u, 'detect_encoding')
def test_quick_detect_encoding_edge_cases(detect_encoding, cchardet_detect):
    cchardet_detect.return_value = {'encoding': 'ascii'}
    eq_('ascii', u.quick_detect_encoding("qwe"))
    cchardet_detect.assert_called_once_with("qwe")

    # fallback to detect_encoding
    cchardet_detect.return_value = {}
    detect_encoding.return_value = 'utf-8'
    eq_('utf-8', u.quick_detect_encoding("qwe"))

    # exception
    detect_encoding.reset_mock()
    cchardet_detect.side_effect = Exception()
    detect_encoding.return_value = 'utf-8'
    eq_('utf-8', u.quick_detect_encoding("qwe"))
    ok_(detect_encoding.called)
