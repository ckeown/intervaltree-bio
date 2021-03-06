'''
Test module for GenomeIntervalTree

Copyright 2014, Konstantin Tretyakov

Licensed under MIT license.
'''
import os
try:
    from urllib import urlretrieve
except ImportError: # Python 3?
    from urllib.request import urlretrieve

from intervaltree_bio import GenomeIntervalTree, UCSCTable

def test_knownGene(base_url):
    # To speed up testing, we'll download the file and reuse the downloaded copy
    knownGene_url = base_url + 'knownGene.txt.gz'

    # To speed up testing, we'll download the file and reuse the downloaded copy
    knownGene_file, headers = urlretrieve(knownGene_url)

    knownGene_localurl = 'file:///%s' % os.path.abspath(knownGene_file)
    knownGene = GenomeIntervalTree.from_table(url=knownGene_localurl, decompress=True) # Py3 downloads .gz files to local files with names not ending with .gz
    assert len(knownGene) == 82960
    result = knownGene[b'chr1'].search(100000, 138529)
    assert len(result) == 1
    assert list(result)[0].data['name'] == b'uc021oeg.2'

    knownGene = GenomeIntervalTree.from_table(url=knownGene_localurl, mode='cds', decompress=True)
    assert len(knownGene) == 82960
    assert not knownGene[b'chr1'].overlaps(100000, 138529)

    knownGene = GenomeIntervalTree.from_table(url=knownGene_localurl, mode='exons', decompress=True)
    assert len(knownGene) == 742493
    result = list(knownGene[b'chr1'].search(134772, 140566))
    assert len(result) == 3
    assert result[0].data == result[1].data and result[0].data == result[2].data

def test_ensGene(base_url):
    # Smoke-test we can at least read ensGene.
    ensGene_url = base_url + 'ensGene.txt.gz'
    ensGene = GenomeIntervalTree.from_table(url=ensGene_url, mode='cds', parser=UCSCTable.ENS_GENE)
    assert len(ensGene) == 204940

def test_refGene(base_url):
    # Smoke-test for refGene
    refGene_url = base_url + 'refGene.txt.gz'
    refGene = GenomeIntervalTree.from_table(url=refGene_url, mode='tx', parser=UCSCTable.REF_GENE)
    assert len(refGene) == 52350  # NB: Some time ago it was 50919, hence it seems the table data changes on UCSC and eventually the mirror and UCSC won't be the same.

def test_genepred():
    # Smoke-test for output from gtfToGenePred
    testdir = os.path.join(os.path.dirname(__file__), 'test_data')
    kg = open(os.path.abspath(os.path.join(testdir, "test_genepred.txt")))
    gtree = GenomeIntervalTree.from_table(fileobj=kg, mode='cds', parser=UCSCTable.GENEPRED)
    assert len(gtree) == 100
