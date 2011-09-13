from nose.tools import *
import numpy as np
import rdfspace
from rdfsim.space import Space

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
        ('http://dbpedia.org/resource/Category:Categories_named_after_television_series', 1),
        ('http://dbpedia.org/resource/Category:New_York_City_in_fiction', 1),
        ('http://dbpedia.org/resource/Category:Foo', 0.9),
    ])
    assert_equal(space.parents('http://dbpedia.org/resource/Category:Star_Trek'), [
        ('http://dbpedia.org/resource/Category:Categories_named_after_television_series', 1),
        ('http://dbpedia.org/resource/Category:Foo', 0.9),
    ])
    assert_equal(space.parents('http://dbpedia.org/resource/Category:Foo'), [])

def test_distance_uri():
    space = Space('tests/example.n3')
    assert_equal(space.distance_uri('http://dbpedia.org/resource/Category:Futurama', 'http://dbpedia.org/resource/Category:Star_Trek'), (1 + 0.9 * 0.9) / (np.sqrt(2 + 0.9**2) * np.sqrt(1 + 0.9**2)))

def test_centroid():
    space = Space('tests/example.n3')
    centroid = space.centroid({'http://dbpedia.org/resource/Category:Futurama': 2, 'http://dbpedia.org/resource/Category:Star_Trek': 1})
    assert_equal(centroid, {
        'http://dbpedia.org/resource/Category:New_York_City_in_fiction': 2.0/3,
        'http://dbpedia.org/resource/Category:Foo': 2*0.9 / 3 + 0.9 / 3,
        'http://dbpedia.org/resource/Category:Categories_named_after_television_series' : 1.0,
    })
