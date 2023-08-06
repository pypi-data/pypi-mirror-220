
from kraken_schema_org import kraken_schema_org as k

import uuid

def test_normalize_type():

    record_type = 'person'
    assert k.normalize_type(record_type) =='schema:Person'



def test_normalize_key():

    key = 'givenname'
    assert k.normalize_key(key) =='schema:givenName'

def test_get_keys():

    record_type = 'person'
    assert 'schema:worksFor' in k.get_keys(record_type)

def test_get_datatype():

    record_type = 'person'
    key = 'schema:givenName'
    assert k.get_datatype(record_type, key) == ['schema:Text']

def test_get_id_url():
    record = {
    "@type": "schema:WebPage",
    "schema:url": "https://www.test.com/"
    }
    
    assert k.get_record_id(record) == 'bdfb84c2-6531-3478-95bd-32d644bbf6ed'

def test_get_id_email():
    record = {
    "@type": "schema:WebPage",
    "schema:url": "https://www.test.com/"
    }
    
    assert k.get_record_id(record) == 'bdfb84c2-6531-3478-95bd-32d644bbf6ed'

def test_get_id_generic():
    record = {
    "@type": "schema:Message",
    "schema:url": "https://www.test.com/"
    }
    
    assert uuid.UUID(k.get_record_id(record))



def test_normalize_record():
    record = {
    "@type": "schema:webpage",
    "schema:url": "www.test.com/"
    }

    record2 = {
    '@id': 'bdfb84c2-6531-3478-95bd-32d644bbf6ed',
    '@type': 'schema:WebPage',
    'schema:url': 'https://www.test.com/',
    }

    
    assert k.normalize_record(record) == record2

def test_normalize_record_complex():

    record_id = str(uuid.uuid4())
    record = {
    "@type": "schema:webpage",
    "schema:url": "www.test.com/",
    "schema:creator": {
        "@type": "schema:person",
        "@id": record_id,
        "schema:givenName": "Bob"
        }
    }

    record2 = {
    '@id': 'bdfb84c2-6531-3478-95bd-32d644bbf6ed',
    '@type': 'schema:WebPage',
    'schema:url': 'https://www.test.com/',
    'schema:creator': {
        '@id': record_id,
        '@type': 'schema:Person',
        'schema:givenName': 'Bob'
        }
    }

    
    assert k.normalize_record(record) == record2

def test_normalize_non_standard_record():

    record_id = str(uuid.uuid4())
    
    record = {
    "@type": "schema:webpage",
    "schema:url": "www.test.com/",
    "kraken:test": "bob"
    }

    record2 = {
    "@type": "schema:WebPage",
    '@id': 'bdfb84c2-6531-3478-95bd-32d644bbf6ed',
    "schema:url": "https://www.test.com/",
    "kraken:test": "bob"
    }
    record3 = {
    "@type": "schema:WebPage",
    '@id': 'bdfb84c2-6531-3478-95bd-32d644bbf6ed',
    "schema:url": "https://www.test.com/"
    }
    
    assert k.normalize_record(record) == record2
    assert k.normalize_record(record, True) == record3

def test_normalize_value_list():
    record1 = {
        "@type": "schema:webpage",
        "schema:url": [
            "www.test.com/",
            "www.test2.com"
        ]
        }
    record2 = {
        "@type": "schema:WebPage",
        "schema:url": [
            "https://www.test.com/",
            "https://www.test2.com/"
        ]
        }

    
    assert k.normalize_record(record1) == record2



def test_normalize_list():

    record_id = str(uuid.uuid4())
    
    records1 = [
        {
        "@type": "schema:webpage",
        "schema:url": "www.test.com/",
        },
        {
        "@type": "schema:WebPage",
        "schema:url": "https://www.test2.com/",
        }
        ]
    
    
    records2 = [
        {
        "@type": "schema:WebPage",
        '@id': 'bdfb84c2-6531-3478-95bd-32d644bbf6ed',
        "schema:url": "https://www.test.com/"
        },
        {
        "@type": "schema:WebPage",
        '@id': '56a82793-65f6-336d-b092-85f78ad27ecc',
        "schema:url": "https://www.test2.com/"
        }
    ]
    
    
    assert k.normalize_record(records1) == records2




def test_normalize_empty():

    record_id = str(uuid.uuid4())
    
    record = None

    
    assert k.normalize_record(record) == None
