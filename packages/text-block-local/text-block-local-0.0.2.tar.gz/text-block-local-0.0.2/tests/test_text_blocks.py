import pytest
from circles_text_block_local.text_blocks import TextBlocks

def test_valid_regex():
    blocks = [(3, 
    '''Sydney Lauer
    sydlauer@umich.edu
    9252853371
    0553083627
    Ann Arbor, Michigan
    '''),  (4,
    '''Sydney Lauer
    0301/2003
    9252853371
    srlauer3103@gmail.com
    March 1 2003
    ''')]
    classifier = TextBlocks(blocks)
    
    fields = classifier.extract_fields()
    expected = {'Email': [' sydlauer@umich.edu', ' srlauer3103@gmail.com'], 'Phone Number': [' 9252853371']}
    assert fields == expected

def test_invalid_regex():
    blocks = [
        (4, '''InvalidRegexTest
                invalidemail@adress
                9252853371
                '''),
    ]
    classifier = TextBlocks(blocks)

    fields = classifier.extract_fields()
    expected = {'Phone Number': [' 9252853371']}
    assert fields == expected

def test_no_matches():
    blocks = [
        (6, '''NoMatchTest
                no@email
                No phone number
                '''),
    ]
    classifier = TextBlocks(blocks)
    fields = classifier.extract_fields()
    assert fields == {}

def test_empty_block():
    blocks = [
        (7, ''),
    ]
    classifier = TextBlocks(blocks)
    fields = classifier.extract_fields()
    assert fields == {}

def test_newline_handling():
    blocks = [
        (8, '''TestNewlineHandling
                test@example.com
                12345\n67890
                Line1\nLine2
                '''),
    ]
    classifier = TextBlocks(blocks)
    fields = classifier.extract_fields()
    expected = {'Email': [' test@example.com']}
    assert fields == expected

def test_other_block_types():
    blocks = [
            (1, '''BlockType1Test
                    test1@example.com
                    111-111-1111
                    www.websiteexample.com
                 '''),
            (2, '''BlockType2Test
                    test2@example.com
                    222-222-2222
                    website.com
                 '''),
        ]
    classifier = TextBlocks(blocks)
    fields = classifier.extract_fields()
    expected = {'Email': [' test1@example.com', ' test2@example.com']}
    assert fields == expected




