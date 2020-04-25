import os
from files import prepare_directory
from dictionaries import create_dict, lazy_load_dict

resource_path = "test/resources"
texts_path = "test/resources/texts"
dictionary_name = "test.dict"
dictionary_path = os.path.join(resource_path, dictionary_name)


def setup_module(module):
    prepare_directory(resource_path)
    if os.path.exists(dictionary_path):
        os.remove(dictionary_path)


def test_lazy_load():
    create_result = lazy_load_dict(resource_path, dictionary_name, texts_path)
    lazy_result = lazy_load_dict(resource_path, dictionary_name, texts_path)

    assert {"dummy": 1, "text": 2} == create_result
    assert {"dummy": 1, "text": 2} == lazy_result
