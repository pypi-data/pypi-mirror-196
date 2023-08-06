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


import itertools

import anyjsonthing.utils as utils

from typing import Any
from typing import TypeVar


_T = TypeVar("_T")


class Serializer(object):
    """Implements the logic for serializing/deserializing any data objects as/from JSON data.

    Note:
        This class is more conveniently accessible via ``anyjsonthing.Serializer``.

    For details on which classes are considered as valid providers of serializable data objects (in strict and
    non-strict mode), see :mod:`anyjsonthing`.
    """

    #  METHODS  ########################################################################################################

    @staticmethod
    def is_serializable(anything: Any, strict: bool = True) -> bool:
        """Evaluates whether ``anything`` is serializable (by the :mod:`anyjsonthing` library).

        Warning:
            If you want to check whether a specific :class:`type` is serializable, then you have to provide ``anything``
            that is an **instance** of the same. The simple reason for this is that we cannot determine which attributes
            instances of the considered :class:`type` provide during runtime without having access to an actual instance
            of that :class:`type`.

        Note:
            If ``anything`` is a :class:`type` as opposed to an instance of a class, then this method returns ``False``,
            since :class:`type`\ s are not serializable.

        Args:
            anything: The evaluated instance.
            strict: Indicates whether strict mode is used.

        Returns:
            ``True`` if ``anything`` is serializable, and ``False`` otherwise.
        """

        # If the provided anything is a type as opposed to an instance of a class, which is never serializable.
        if isinstance(anything, type):

            return False

        # Next, we fetch the names of all args of the init method of anything's type as well as the names of all public
        # attributes and properties of anything.
        required_init_args, optional_args = utils.fetch_init_args(type(anything))
        attributes = utils.fetch_attributes(anything)
        properties = utils.fetch_properties(type(anything))

        # Before we can check if anything is serializable, we have to determine the args that need to have corresponding
        # attributes/properties. In strict mode, this is the case for all args. In non-strict mode, only required args
        # (i.e., those without default value) need to satisfy this criterion.
        args_to_check = required_init_args
        if strict:

            args_to_check.extend(optional_args)

        # Finally, we ensure that for every required arg of init there is an eponymous attribute/property that allows
        # for retrieving the value that is required for reconstructing instances.
        for arg in required_init_args:

            if arg not in attributes and arg not in properties:  # -> No attribute/property exists for the current arg.

                return False

        # If we arrive at this point, we successfully confirmed that there are attributes/properties for all args needed
        # to reconstruct anything.
        return True

    @staticmethod
    def from_json(cls: type[_T], json: dict[str, Any]) -> _T:
        """Deserializes the provided ``json`` data into an instance of the specified ``cls``.

        Args:
            cls: The :class:`type` of the instance that is described by the provided ``json`` data.
            json: The JSON representation of the instance that is deserialized.

        Returns:
            The deserialized instance of ``cls``.

        Raises:
            ValueError: If the ``json`` data is missing a required arg of the ``__init__`` method of the target ``cls``
                or if it specifies properties that are unknown to the latter.
        """

        # To be able to sanitize the provided JSON data, we first retrieve all args of the constructor of the given
        # type.
        required_args, optional_args = utils.fetch_init_args(cls)
        all_args = set(itertools.chain(required_args, optional_args))

        # Now, we first ensure that all required args are specified.
        for some_arg in required_args:

            if some_arg not in json:

                raise ValueError(f"Missing required arg <{some_arg}> in the given <json> data")

        # Next, we ensure that no unknown args are provided.
        for some_arg in json.keys():

            if some_arg not in all_args:

                raise ValueError(f"Encountered unknown arg <{some_arg}> in the given <json> data")

        # Finally, we are ready to create the needed instance using the given args.
        return cls(**json)

    @classmethod
    def to_json(cls, anything: Any, strict: bool = True) -> dict[str, Any]:
        """Serializes ``anything``, creating a JSON representation of the same.

        Args:
            anything: The data object that is serialized as JSON data.
            strict: Indicates whether strict mode is used.

        Returns:
            The created JSON representation of ``anything``.

        Raises:
            ValueError: If ``anything`` cannot be serialized, as it is an instance of a class that is not considered as
                a valid provider of data objects.
        """

        # First and foremost, we ensure that the given instance is actually serializable.
        if not cls.is_serializable(anything, strict=strict):

            raise ValueError("The given <anything> is not serializable")

        # Next, we fetch the names of all (public) attributes and properties of the provided instance.
        attrs_and_props = utils.fetch_attributes(anything) + utils.fetch_properties(type(anything))

        # Finally, we serialize the instance.
        init_args = itertools.chain.from_iterable(
                utils.fetch_init_args(type(anything))
        )
        return {
                arg: getattr(anything, arg)
                for arg in init_args
                if arg in attrs_and_props  # -> This is needed if optional args don't have a public attribute/property.
        }
