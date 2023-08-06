# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                     #
#   Copyright (c) 2023, Patrick Hohenecker                                            #
#                                                                                     #
#   All rights reserved.                                                              #
#                                                                                     #
#   Redistribution and use in source and binary forms, with or without                #
#   modification, are permitted provided that the following conditions are met:       #
#                                                                                     #
#       * Redistributions of source code must retain the above copyright notice,      #
#         this list of conditions and the following disclaimer.                       #
#       * Redistributions in binary form must reproduce the above copyright notice,   #
#         this list of conditions and the following disclaimer in the documentation   #
#         and/or other materials provided with the distribution.                      #
#                                                                                     #
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS               #
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT                 #
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR             #
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER       #
#   OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          #
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,               #
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR                #
#   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF            #
#   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING              #
#   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS                #
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                      #
#                                                                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


"""A library that implements serialization of simple data objects as JSON data.

A common use case that Python's standard library does not provide a satisfying solution for yet is mapping data objects
to JSON data and vice versa. The package :mod:`anyjsonthing` implements an out-of-the-box solution for this task that
(with minor restrictions) allows for serializing/deserializing any simple data objects as/from JSON data and
reading/writing them from/to the disk.

This package is based on the assumption that data classes should **not** maintain any internal state, but only store a
collection of data points, exposed through public attributes and properties, respectively. Hence, :mod:`anyjsonthing`
considers all instances of any class that satisfies the following criteria as serializable data objects:

* the class is not a metaclass (i.e., a sub-type of :class:`type`), and
* for each required argument (without default value) of the class' ``__init__`` method, there exists an eponymous
  **public** attribute/property that allows for retrieving the value that was provided to the constructor.

Warning:
    Currently, :mod:`anyjsonthing` only supports classes with "simple" attributes/properties that are

    * of primitive type :class:`str`, :class:`int`, :class:`float`, or :class:`bool`,
    * a :class:`list` that contains only simple data, or a
    * a :class:`dict` that contains only :class:`str` keys and simple values.

    Data objects may expose array-like data as :class:`tuple`, but only if the constructor of the respective class is
    prepared to receive that specific piece of data as :class:`list`. (The reason for this is that a JSON object does
    not distinguish between mutable and immutable arrays, which is why we can only deserialize array data as
    :class:`list`\ s.

    More complex data types and nested data objects will be supported in future versions of the library.

With these assumptions in place, serializing data objects as JSON data is as simple as gathering all those values of the
considered instance (by means of the according attributes/properties) that are required by the ``__init__`` method of
its :class:`type`, and combining them into a single :class:`dict`. This is exactly what the class
:class:`~anyjsonthing.serializer.Serializer` does under the hood:

.. code-block:: python

   import anyjsonthing
   from dataclasses import dataclass

   @dataclass
   class MyDataClass(object):
       a: str
       b: str
       c: str = "C"

   some_instance = MyDataClass("A", "B")

   # Step 1: serialize the instance
   json_data = anyjsonthing.Serializer.to_json(some_instance)
   assert json_data == {"a": "A", "b": "B", "c": "C"}

   # Step 2: deserialize the JSON data
   reconstructed = anyjsonthing.Serializer.from_json(MyDataClass, json_data)
   assert reconstructed == some_instance

While :mod:`anyjsonthing` has been built with a focus on :mod:`dataclasses`, it can also be used with "normal" classes.
In this case, however, args of a class' ``__init__`` method do not necessary have an according public attribute or
property that allows for retrieving their values for serialization. Typically, :mod:`anyjsonthing` will raise an error
in any such case, with one exception. If the ``__init__`` method has a keyword-arg with default value that does not have
a matching public attribute/property, then you can tell the :class:`~anyjsonthing.serializer.Serializer` to be
**non-strict**, which means that it will simply ignore this arg. The rationale behind this is that we can still
reconstruct **some** instance from the resulting JSON representation (as the missing arg has a default value), but we
can no longer guarantee that it is identical to the original one. However, this functionality is intended to cover
corner cases, and typically should not be required. The following example illustrates the described behavior:

.. code-block:: python

   import anyjsonthing

   class AnotherDataClass(object):

       def __init__(self, a, b, c="c"):
           self.a = a   # -> Public attribute.
           self._b = b  # -> Protected attribute, exposed through a public property.
           self._c = c  # -> Protected attribute, not exposed at all.

       def __str__(self):  # -> NOTICE: this exposes everything.
           return f"AnotherDataClass(a = <{self.a}>, b = <{self._b}>, c = <{self._c}>)"

       @property
       def b(self):  # -> Public property.
           return self._b

   some_instance = AnotherDataClass("A", "B", "C")

   # Step 1: serialize the instance
   json_data = anyjsonthing.Serializer.to_json(some_instance)  # -> ERROR!
   json_data = anyjsonthing.Serializer.to_json(some_instance, strict=False)
   assert json_data == {"a": "A", "b": "B"}

   # Step 2: deserialize the JSON data
   reconstructed = anyjsonthing.Serializer.from_json(AnotherDataClass, json_data)
   assert str(reconstructed) != str(some_instance)
   assert str(reconstructed) == str(AnotherDataClass("A", "B"))
"""


from .serializer import Serializer
