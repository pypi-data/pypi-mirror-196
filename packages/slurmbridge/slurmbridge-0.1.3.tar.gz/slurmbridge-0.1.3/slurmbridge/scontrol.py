from __future__ import annotations

import asyncio
import dataclasses
import shutil
from typing import (
    ClassVar,
    Dict,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
)

from slurmbridge.cliobject import SlurmCLIObject, SlurmObjectException
from slurmbridge.common import camel_to_snake_case, snake_to_camel_case

SCONTROL_PATH = shutil.which("scontrol")


class SlurmControlError(SlurmObjectException):
    def __str__(self) -> str:
        return f"{self.args[1]}"


SlurmControlObjectType = TypeVar("SlurmControlObjectType", bound="SlurmControlObject")


class SlurmControlObject(SlurmCLIObject[SlurmControlObjectType]):
    query_options: ClassVar[Sequence[str]] = tuple()
    query_type: ClassVar[Literal["Normal", "ValueOnly"]] = "Normal"

    @classmethod
    async def _run_scontrol_command(
        cls,
        verb: str,
        *arguments: str,
        error_ok=False,
    ) -> Tuple[int | None, str]:
        if SCONTROL_PATH is None:
            raise ImportError("scontrol could not be found in path.")

        process = await asyncio.create_subprocess_exec(
            SCONTROL_PATH,
            verb,
            *arguments,
            "--oneline",
            "--detail",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        process_output = (stderr if len(stderr) > 0 else stdout).decode("ascii")

        if not error_ok and process.returncode != 0:
            raise SlurmControlError(cls, process_output)

        return process.returncode, process_output

    @classmethod
    async def _scontrol_show(
        cls,
        fields: Sequence[str],
        filters: Dict[str, str],
    ) -> Sequence[Dict[str, str]]:
        filter_args: list[str] = []

        # in scontrol you pass the object type to get all entries of an object
        # OR you pass a primary key to filter for specific instances but you can't do both
        if len(filters) > 0:
            if cls.query_type == Literal["ValueOnly"]:
                filter_args.append(cls.__name__)
                filter_args.append(f"{list(filters.values())[0]}")
            else:
                for column, value in filters.items():
                    filter_args.append(f"{column}={value}")
        else:
            filter_args.append(cls.__name__)

        exit_code, process_output = await cls._run_scontrol_command(
            "show", *filter_args, *cls.query_options
        )
        if exit_code != 0:
            raise SlurmControlError(cls, process_output)

        all_objects = []
        case_insensitive_fields = [field_name.lower() for field_name in fields]
        # we use --oneline to make sure we have exactly 1 object per line
        for object_reponse in process_output.splitlines():
            # attributes are seperated by any whitespace
            object_attributes = {}
            for attribute_string in object_reponse.split():
                # sometimes an attribute is not followed by a value (e.g. "Name=")
                # so we pack second argument to a list but thanks to maxsplit=1
                # this list is either empty or has exactly one entry
                attribute_name, *attribute_value = attribute_string.split(
                    "=", maxsplit=1
                )
                # we need to use case insensitive matching here since slurm
                # uses SREAMINGCASE for abbrevations (e.g. TRES instead of Tres)
                if attribute_name.lower() in case_insensitive_fields:
                    object_attributes[attribute_name] = (
                        attribute_value[0] if len(attribute_value) == 1 else ""
                    )
            if len(object_attributes) > 0:
                all_objects.append(object_attributes)

        return all_objects

    @classmethod
    async def _scontrol_execute(
        cls, verb: str, filter: str, extra_args: Optional[List[str]] = None
    ):
        if extra_args is None:
            extra_args = []
        exit_code, process_output = await cls._run_scontrol_command(
            verb,
            *extra_args,
            filter,
            error_ok=True,
        )

        if exit_code != 0:
            raise SlurmControlError(cls, process_output)

    @classmethod
    async def _scontrol_update(
        cls,
        new_values: Mapping[str, str],
        filters: Mapping[str, str],
    ):
        update_args: list[str] = []
        for field_name, new_value in new_values.items():
            update_args.append(f"{field_name}={new_value}")

        filter_args = []
        for column, value in filters.items():
            filter_args.append(f"{column}={value}")

        exit_code, process_output = await cls._run_scontrol_command(
            "update",
            *filter_args,
            *update_args,
            error_ok=True,
        )

        if exit_code != 0:
            raise SlurmControlError(cls, process_output)

    @classmethod
    def _response_to_attributes(
        cls: Type[SlurmControlObjectType], response_data: Dict[str, str]
    ) -> Dict[str, str | None]:
        empty_variants = ("(null)", "N/A", "None")
        return {
            # some values will always return a value although they are empty
            # we need to ignore them here to make sure not to set these values
            # when saving the object again
            camel_to_snake_case(key): value if value not in empty_variants else None
            for key, value in response_data.items()
        }

    @classmethod
    def _response_to_instances(
        cls: Type[SlurmControlObjectType], response: Sequence[Dict[str, str]]
    ) -> Sequence[SlurmControlObjectType]:
        instances: list[SlurmControlObjectType] = []
        for data in response:
            attributes = cls._response_to_attributes(data)
            instance = cls(**attributes)
            instances.append(instance)
        return instances

    def _to_query(self) -> Tuple[Dict[str, str], Dict[str, str]]:
        update_fields: Dict[str, str] = {}
        filter_values = {}

        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if field.name in self._primary_key_fields:
                filter_values[snake_to_camel_case(field.name)] = value
            elif (
                field.name not in (self._read_only_fields + self._synthetic_fields)
                and value
            ):
                update_fields[snake_to_camel_case(field.name)] = value

        return update_fields, filter_values

    @classmethod
    async def filter(
        cls: Type[SlurmControlObjectType], **filters: str
    ) -> Sequence[SlurmControlObjectType]:
        object_fields = [
            snake_to_camel_case(field.name)
            for field in dataclasses.fields(cls)
            if field.name not in (cls._synthetic_fields + cls._write_only_fields)
        ]
        object_data = await cls._scontrol_show(object_fields, filters)
        instances = cls._response_to_instances(object_data)
        # only return the queried type of instance
        return [instance for instance in instances if isinstance(instance, cls)]

    async def save(self):
        updates, filters = self._to_query()

        await self._scontrol_update(updates, filters)
        await self.refresh_from_db()
