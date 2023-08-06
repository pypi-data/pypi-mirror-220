# dataclass_codec

dataclass_codec is a Python library that provides encoding and decoding functions for dictionaries. It allows you to easily convert Python dictionaries to JSON-compatible data structures and vice versa.

## Installation

You can install dataclass_codec using pip:

```
pip install dataclass-codec
```

## Usage

dataclass_codec is designed to work with dictionaries, which are a common way to represent structured data in Python. You can use dataclass_codec to decode dictionaries into Python dataclasses.

Here is an example of how to use dataclass_codec with dataclasses:

```python
from dataclasses import dataclass
from dataclass_codec import decode

# Define a dataclass
@dataclass
class Person:
    name: str
    age: int
    city: str

# Define a dictionary representing a person
person_dict = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Decode the dictionary into a Person object
person = decode(person_dict, Person)

# Access the attributes of the Person object
print(person.name)  # Output: John
print(person.age)   # Output: 30
print(person.city)  # Output: New York
```

In the above example, we define a dataclass `Person` using the `@dataclass` decorator. The `Person` dataclass has three attributes: `name`, `age`, and `city`. We then have a dictionary `person_dict` representing a person. By using the `decode` function from dataclass_codec, we can easily convert the dictionary into a Person object. Finally, we access the attributes of the Person object and print their values.

## Advanced Features

### Nested Dictionaries

You can use dataclass_codec to decode dictionaries that have nested dictionaries as values. The nested dictionaries will be decoded into nested dataclass objects.

```python
from dataclasses import dataclass
from dataclass_codec import decode

# Define a nested dataclass
@dataclass
class Address:
    street: str
    city: str
    zip_code: str

# Define a dataclass with a nested dataclass
@dataclass
class Person:
    name: str
    age: int
    address: Address

# Define a dictionary with a nested address dictionary
person_dict = {
    "name": "John",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "zip_code": "10001"
    }
}

# Decode the dictionary into a Person object
person = decode(person_dict, Person)

# Access the attributes of the Person object and its nested Address object
print(person.name)                      # Output: John
print(person.age)                       # Output: 30
print(person.address.street)            # Output: 123 Main St
print(person.address.city)              # Output: New York
print(person.address.zip_code)          # Output: 10001
```

In this example, we define a dataclass `Address` representing an address with attributes `street`, `city`, and `zip_code`. We also define a dataclass `Person` with attributes `name`, `age`, and `address`, where `address` is an instance of the `Address` dataclass. The dictionary `person_dict` contains a nested dictionary for the address. By using the `decode` function, we can easily convert the dictionary into a Person object with a nested Address object. Finally, we access the attributes of the Person object and its nested Address object and print their values.

Remember to define all your dataclasses using the `@dataclass` decorator for dataclass_codec to work correctly.

### Decoding a Dictionary with Generic List

```python
from dataclasses import dataclass
from dataclass_codec import decode
from typing import List, TypeVar

# Define a TypeVar
T = TypeVar('T')

# Define a generic dataclass
@dataclass
class Container:
    items: List[T]

# Define a dictionary with a list of items
container_dict = {
    "items": [1, 2, 3, 4, 5]
}

# Decode the dictionary into a Container object
container = decode(container_dict, Container[int])

# Access the attributes of the Container object
print(container.items)  # Output: [1, 2, 3, 4, 5]
```

In this example, we showcase how to decode a dictionary containing a list of generic types. We define a generic dataclass `Container` with a single attribute `items`, which is a list of generic type `T`. The dictionary `container_dict` contains a list of items `[1, 2, 3, 4, 5]`. By using the `decode` function with the type `Container[int]`, we can convert the dictionary into a `Container` object, where the list of items is preserved.

Feel free to include this example in your readme to demonstrate how to decode a dictionary with a generic list into a corresponding dataclass object.

## Decode Context and Context Scope (ID: `decode-context`)

The `dataclass_codec` library provides a `DecodeContext` class and a context-based approach to manage the decoding behavior using the `decode_context_scope` context manager.

### DecodeContext

```python
@dataclass
class DecodeContext:
    strict: bool = False
    primitive_cast_values: bool = True
    dataclass_unset_as_none: bool = True
    collect_errors: bool = False
```

The `DecodeContext` class represents the decoding context with the following configurable options:

- `strict` (bool): If set to `True`, the decoder raises an exception when encountering unknown fields. Defaults to `False`.
- `primitive_cast_values` (bool): If set to `True`, the decoder attempts to cast values to their declared types. Defaults to `True`.
- `dataclass_unset_as_none` (bool): If set to `True`, the decoder treats unset fields in dataclasses as `None`. Defaults to `True`.
- `collect_errors` (bool): If set to `True`, the decoder collects decoding errors as a list of `(error_path, error)` tuples. Defaults to `False`.

### decode_context_scope

```python
@contextmanager
def decode_context_scope(
    decode_context: DecodeContext,
) -> Generator[None, Any, None]:
    # Code for the context manager
```

The `decode_context_scope` is a context manager that allows you to temporarily set a specific `DecodeContext` within a context block. This context manager ensures that the desired decoding behavior is applied within the block and reverts to the previous context afterward.

Usage:

```python
with decode_context_scope(DecodeContext(strict=True, primitive_cast_values=False)):
    # Perform decoding operations within this block
    # The specified decoding context will be in effect
```

By using the `decode_context_scope` context manager, you can easily control the decoding behavior within a specific scope, allowing you to customize options such as strict decoding, casting values, handling unset fields, and collecting errors.

Feel free to include this section in your readme to explain the usage of `DecodeContext` and `decode_context_scope` for managing the decoding behavior within different contexts.

Certainly! Here's an updated version of the section that includes a dataclass with a bytes property:

## Bytes Encoding and Decoding (ID: `bytes-encoding-decoding`)

The `dataclass_codec` library provides built-in support for encoding and decoding byte data, including working with bytes properties within dataclasses. You can easily encode byte data into a string representation and decode it back into its original byte form. This is useful when working with binary data or when serializing and deserializing byte data in your applications.

### Encoding Bytes

To encode byte data, you can use the `encode` function provided by the `dataclass_codec` library. The `encode` function takes a byte object as input and returns its string representation.

Example:

```python
import base64
from dataclasses import dataclass
from dataclass_codec import encode

@dataclass
class MyData:
    binary_data: bytes

# Create an instance of the dataclass
my_data = MyData(binary_data=b"Hello, world!")

# Encode the byte data
encoded_data = encode(my_data)

# Print the encoded data
print(encoded_data)  # Output: '{"binary_data": "SGVsbG8sIHdvcmxkIQ=="}'
```

In this example, we define a dataclass `MyData` with a `binary_data` property of type `bytes`. We create an instance of the dataclass and set the `binary_data` property to `b"Hello, world!"`. We then use the `encode` function to encode the dataclass instance, including the byte data. The resulting encoded data is `{"binary_data": "SGVsbG8sIHdvcmxkIQ=="}`. The byte data is encoded using Base64 encoding within the JSON representation of the dataclass instance.

### Decoding Bytes

To decode byte data back into its original form, you can use the `decode` function provided by the `dataclass_codec` library. The `decode` function takes the encoded data as a string and the target dataclass type and returns the decoded dataclass instance.

Example:

```python
import base64
from dataclasses import dataclass
from dataclass_codec import decode

@dataclass
class MyData:
    binary_data: bytes

# Decode the encoded data
decoded_data = decode({"binary_data": "SGVsbG8sIHdvcmxkIQ=="}, MyData)

# Access the byte data
print(decoded_data.binary_data)  # Output: b"Hello, world!"
```

In this example, we define the same `MyData` dataclass with a `binary_data` property of type `bytes`. We use the `decode` function to decode the encoded data `{"binary_data": "SGVsbG8sIHdvcmxkIQ=="}` back into its original dataclass form. The resulting decoded dataclass instance contains the byte data `b"Hello, world!"`.

By leveraging the encoding and decoding capabilities provided by the `dataclass_codec` library, you can seamlessly work with byte data within dataclasses, ensuring efficient serialization and deserialization of binary data.

Feel free to include this section in your readme to explain the process of encoding and decoding byte data, including working with bytes properties within dataclasses using the `dataclass_codec` library.

## Conclusion

dataclass_codec is a powerful library for decoding dictionaries into dataclasses in Python. It provides an easy and efficient way to convert data between Python objects and JSON-compatible formats. Whether you need to deserialize data for processing or manipulation purposes, dataclass_codec can simplify the process and save you time. Give it a try and see how it can enhance your data manipulation workflow.
