from nose.tools import *
import rdfspace
from rdfspace.space import Space

def test_init():
    space = Space('tests/example.n3')
    assert_equal(space._path_to_rdf, 'file:tests/example.n3')
    assert_equal(space._format, 'ntriples')
    assert_equal(space._property, 'http://www.w3.org/2004/02/skos/core#broader')
    assert_equal(space._direct_parents, {
        'http://dbpedia.org/resource/Category:Categories_named_after_television_series': ['http://dbpedia.org/resource/Category:Foo'],
        'http://dbpedia.org/resource/Category:Star_Trek': [
            'http://dbpedia.org/resource/Category:Categories_named_after_television_series',
        ],
        'http://dbpedia.org/resource/Category:Futurama': [
            'http://dbpedia.org/resource/Category:Categories_named_after_television_series',
            'http://dbpedia.org/resource/Category:New_York_City_in_fiction', 
        ],
    })

def test_parents():
    space = Space('tests/example.n3')
    assert_equal(space.parents('http://dbpedia.org/resource/Category:Futurama'), [
        'http://dbpedia.org/resource/Category:New_York_City_in_fiction',
        'http://dbpedia.org/resource/Category:Foo',
        'http://dbpedia.org/resource/Category:Categories_named_after_television_series',
    ])
    assert_equal(space.parents('http://dbpedia.org/resource/Category:Foo'), [])

def test_distance():
    space = Space('tests/example.n3')
    assert_equal(space.distance('http://dbpedia.org/resource/Category:Futurama', 'http://dbpedia.org/resource/Category:Star_Trek'), 0.81649658092772592)
