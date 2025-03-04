import pytest
from fullcontrol.base import BaseModelPlus
from pydantic import Field, ValidationError, ConfigDict
from typing import Any

# Create a test model class - moved init properties to Field() to avoid warning
class TestBaseModel(BaseModelPlus):
    model_config = ConfigDict(extra='forbid')
    
    name: str = Field(default=None)
    age: int = Field(default=None)
    email: str = Field(default=None)
    attr1: float = Field(default=None)
    attr2: str = Field(default=None)
    attr3: int = Field(default=None)

def test_base_model_plus_creation():
    """Test basic model creation"""
    model = TestBaseModel(name="test")
    assert model.name == "test"
    assert model.age is None
    assert model.email is None

def test_base_model_plus_getitem():
    """Test __getitem__ functionality"""
    model = TestBaseModel(name="test", age=25)
    assert model["name"] == "test"
    assert model["age"] == 25

def test_base_model_plus_setitem():
    """Test __setitem__ functionality"""
    model = TestBaseModel(name="test")
    model["age"] = 30
    assert model.age == 30

def test_base_model_plus_update_from():
    """Test update_from method"""
    model1 = TestBaseModel(name="test1", age=25)
    model2 = TestBaseModel(name="test2", email="test@example.com")
    model1.update_from(model2)
    assert model1.name == "test2"
    assert model1.age == 25  # Should keep original value
    assert model1.email == "test@example.com"

def test_base_model_plus_invalid_attribute():
    """Test validation of invalid attributes"""
    with pytest.raises(ValidationError) as exc_info:
        TestBaseModel(name="test", invalid_field="value")
    error_msg = str(exc_info.value)
    assert "Extra inputs are not permitted" in error_msg

def test_base_model_plus_getset():
    model = TestBaseModel()
    
    # Test setting and getting via dict-style access
    model["attr1"] = 1.5
    assert model["attr1"] == 1.5
    
    # Test normal attribute access
    model.attr2 = "test"
    assert model.attr2 == "test"
    assert model["attr2"] == "test"

def test_update_from():
    model1 = TestBaseModel(attr1=1.0, attr2="original")
    model2 = TestBaseModel(attr2="updated", attr3=42)
    
    model1.update_from(model2)
    assert model1.attr1 == 1.0  # Should keep original value
    assert model1.attr2 == "updated"  # Should be updated
    assert model1.attr3 == 42  # Should be updated

def test_validation():
    # Test valid attributes
    valid_model = TestBaseModel(attr1=1.0, attr2="test", attr3=42)
    assert valid_model.attr1 == 1.0
    
    # Test invalid attribute
    with pytest.raises(Exception) as exc_info:
        TestBaseModel(**{"invalid_attr": "value"})
    assert "Extra inputs are not permitted" in str(exc_info.value)

def test_none_values():
    model = TestBaseModel()
    assert model.attr1 is None
    assert model.attr2 is None
    assert model.attr3 is None