"""
Methods to nornalize schema.org records

Converts a record into a standardized record using proper schema.org terms.

"""





import os
import copy
import datetime
import uuid

from kraken_schema_org import kraken_schema_org as norm
import kraken_datatype as dt 



def get(original_record, strict = False):
    """
    Normalize keys and vlues of a record
    """
    
    # Deal with list
    if isinstance(original_record, list):
        records = []
        for i in original_record:
            records.append(get(i))
        return records

    # Deal with non-dict
    if not isinstance(original_record, dict):
        if strict:
            return None
        else:
            return original_record

        
    # Make copy of original
    record = copy.deepcopy(original_record)
    output_record = {}

    # Normalize record type
    record_type = norm.normalize_type(record.get('@type', None))
    output_record['@type'] = record_type

    # Normalize record_id
    record_id = record.get('@id', None)
    output_record['@id'] = record_id
    
    # Normalize values
    for k in record:
        output_record[k] = normalize_value(record_type, k, record[k], strict)

    
    # Normalize id
    output_record['@id'] = norm.get_record_id(output_record)

    
    return output_record




def normalize_value(record_type, key, value, strict=True):
    """Normalize value
    """


    if key in ['@type', '@id']:
        return None

    # Normalize key
    key = norm.normalize_key(key)

    if not key and strict:
        return None
        
    # Get datatypes
    datatypes = norm.get_datatype(record_type, key)

    # Intialize output_record value
    output_record = []
    
    # Cycle through possible datatypes
    for i in datatypes or []:
        result = _normalize_value(i, key, value, strict)
        if result and result not in output_record:
            output_record.append(result)
            
    # Convert back from list if one or None
    if len(output_record) == 1:
        output_record = output_record[0]
    elif len(output_record) == 0:
        output_record = None
    

    return output_record


def _normalize_value(datatype, key, value, strict=True):
    
    if isinstance(value, list):
        results = []
        for i in value:
            results.append(_normalize_value(datatype, key, i, strict))
        return results

    
    # Normalize value if also a record
    if isinstance(value, dict):
        # Normalize record if schema
        if '@type' in value.keys():
            value = get(value)

        # Return normalized record if same datatype
        if value.get('@type', None) == datatype:
            return value
        else:
            return None

    
    if not isinstance(value, (int, str, float)):
        return value

    # Try to normalize, if not working keep value
    try:
        result = dt.normalize(datatype, value)
    except:
        if strict:
            result = None
        
    
    return result

