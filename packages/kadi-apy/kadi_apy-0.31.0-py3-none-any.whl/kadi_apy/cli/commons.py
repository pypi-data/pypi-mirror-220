# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
import sys

import click

from kadi_apy.lib.exceptions import KadiAPYInputError
from kadi_apy.lib.exceptions import KadiAPYRequestError
from kadi_apy.lib.resources.collections import Collection
from kadi_apy.lib.resources.records import Record


class BasicCLIMixin:
    """Mixin for basic functionalities within the CLI."""

    def _update_attribute(self, attribute, value, pipe=False):
        """Edit a basic attribute of an item."""

        meta = self.meta
        if attribute not in meta:
            if not pipe:
                self.info(f"Attribute {attribute} does not exist.")
            return

        value_old = meta[attribute]

        if value_old == value:
            if not pipe:
                self.info(f"The {attribute} is already '{value_old}'. Nothing to do.")
        else:
            response = super().set_attribute(attribute=attribute, value=value)
            if response.status_code == 200:
                if not pipe:
                    self.info(
                        f"Successfully updated the {attribute} of {self} from "
                        f"'{value_old}' to '{value}'."
                    )
            else:
                self.raise_request_error(response)

    def _print_item_created(
        self, title=None, pipe=False, create=False, exit_not_created=False
    ):
        """Utility function to print information about items created via the CLI."""

        if title is not None and self.meta["title"] != title:
            self._update_attribute(attribute="title", value=title, pipe=pipe)

        if pipe:
            click.echo(self.id)

        elif create:
            if self.created:
                self.info(f"Successfully created {self}.")
            else:
                self.info(f"The {self} already exists.")

        if create and exit_not_created and not self.created:
            sys.exit(1)

    def _item_set_attribute(self, **kwargs):
        """Utility function to edit the metadata of an item."""

        for attr, value in kwargs.items():
            if value is not None:
                self._update_attribute(attribute=attr, value=value)

    def _item_print_info(self, pipe=False, **kwargs):
        """Print basic information of an item."""

        meta = self.meta

        if not pipe:
            self.info(f"Information of {self}:")
        if kwargs["description"]:
            click.echo(f"Description: {meta['plain_description']}")

        if kwargs["visibility"]:
            click.echo(f"Visibility: {meta['visibility']}")

        if isinstance(self, Record):
            if "filelist" in kwargs:
                if kwargs["filelist"]:
                    response = self.get_filelist(
                        page=kwargs["page"], per_page=kwargs["per_page"]
                    )
                    if response.status_code == 200:
                        payload = response.json()
                        click.echo(
                            f"Found {payload['_pagination']['total_items']} file(s) on "
                            f"{payload['_pagination']['total_pages']} page(s).\n"
                            f"Showing results of page {kwargs['page']}:"
                        )
                        for results in payload["items"]:
                            click.echo(
                                f"Found file '{results['name']}' with id"
                                f" '{results['id']}'."
                            )
                    else:
                        self.raise_request_error(response)

                if "metadata" in kwargs:
                    if kwargs["metadata"]:
                        if not pipe:
                            self.info("Metadata:")

                            list_metadata = self.flatten_extras()

                            for metadata in list_metadata:
                                metadatum = metadata["key"]
                                value = metadata["value"]
                                if "unit" in metadata:
                                    unit = f" and unit '{metadata['unit']}.'"
                                else:
                                    unit = "."

                                self.info(
                                    f"Found metadatum '{metadatum}' with value"
                                    f"' {value}'{unit}'"
                                )
                        else:
                            self.info(
                                json.dumps(
                                    self.meta["extras"],
                                    indent=2,
                                    sort_keys=True,
                                    ensure_ascii=False,
                                )
                            )

        if isinstance(self, Collection):
            if "records" in kwargs:
                response = self.get_records(
                    page=kwargs["page"], per_page=kwargs["per_page"]
                )
                if response.status_code == 200:
                    payload = response.json()
                    for results in payload["items"]:
                        self.info(
                            f"Found record '{results['title']}' with id"
                            f" '{results['id']}' and identifier"
                            f" '{results['identifier']}'."
                        )
                else:
                    self.raise_request_error(response)


class RaiseRequestErrorMixin:
    """Mixin to raise a exception."""

    def raise_request_error(self, response):
        """Raise exception.

        :param response: The response.
        :raises KadiAPYRequestError: Error is raised since request was not successful.
        """
        payload = response.json()

        self.debug(
            "---------------- Error Info -------------------\n"
            f"{json.dumps(payload, indent=4)}\n"
            "-----------------------------------------------\n"
        )

        description = payload.get("description", "Unknown error.")
        raise KadiAPYRequestError(f"{description} ({response.status_code})")


class UserCLIMixin:
    """Mixin for adding or removing a user within the CLI."""

    def _item_add_user(self, user, permission_new):
        """Add a user to an item."""

        response = super().add_user(user_id=user.id, role_name=permission_new)
        if response.status_code == 201:
            self.info(f"Successfully added {user} as '{permission_new}' to {self}.")
        elif response.status_code == 409:
            response_change = super().change_user_role(
                user_id=user.id, role_name=permission_new
            )
            if response_change.ok:
                self.info(f"The {user} is '{permission_new}' of {self}.")
            else:
                self.raise_request_error(response_change)
        else:
            self.raise_request_error(response)

    def _item_remove_user(self, user):
        """Remove a user from an item."""

        response = super().remove_user(user_id=user.id)
        if response.status_code == 204:
            self.info(f"The {user} was removed from {self}.")
        else:
            self.raise_request_error(response)


class GroupRoleCLIMixin:
    """Mixin for adding or removing a group within the CLI."""

    def _item_add_group_role(self, group, permission_new):
        """Add a group role to an item."""

        response = super().add_group_role(group.id, role_name=permission_new)
        if response.status_code == 201:
            self.info(f"Successfully added {group} as '{permission_new}' to {self}.")
        elif response.status_code == 409:
            response_change = self.change_group_role(
                group_id=group.id, role_name=permission_new
            )
            if response_change.ok:
                self.info(f"The {group} is '{permission_new}' of {self}.")
            else:
                self.raise_request_error(response_change)
        else:
            self.raise_request_error(response)

    def _item_remove_group_role(self, group):
        """Remove a group role from an item."""

        response = super().remove_group_role(group.id)
        if response.status_code == 204:
            self.info(f"The {group} was removed from {self}.")
        else:
            self.raise_request_error(response)


class DeleteItemCLIMixin:
    """Mixin for deleting an item within the CLI."""

    def _item_delete(self, i_am_sure):
        """Delete an item."""

        if not i_am_sure:
            raise KadiAPYInputError(
                f"If you are sure you want to delete {self}, use the flag --i-am-sure."
            )

        response = super().delete()
        if response.status_code == 204:
            self.info("Deleting was successful.")
        else:
            self.error(f"Deleting {self} was not successful.")
            self.raise_request_error(response)


class TagCLIMixin:
    """Mixin for adding or removing a tag within the CLI."""

    def _item_add_tag(self, tag):
        """Add a tag to an item."""
        if super().check_tag(tag):
            self.info(f"Tag '{tag}' already present in {self}.")
            return

        response = super().add_tag(tag)

        if response.status_code == 200:
            self.info(f"Successfully added tag '{tag}' to {self}.")
        else:
            self.error(f"Adding tag '{tag}' to {self} was not successful.")
            self.raise_request_error(response)

    def _item_remove_tag(self, tag):
        """Remove a tag from an item."""
        if not super().check_tag(tag):
            self.info(f"Tag '{tag}' not present in {self}.")
            return

        response = super().remove_tag(tag)

        if response.status_code == 200:
            self.info(f"Successfully removed tag '{tag}' from {self}.")
        else:
            self.error(f"Removing tag '{tag}' from {self} was not successful.")
            self.raise_request_error(response)


class ExportCLIMixin:
    """Mixin for exporting a resource with the CLI."""

    def export(
        self,
        export_type,
        path=".",
        name=None,
        force=False,
        pipe=False,
        use_folder=False,
        **kwargs,
    ):
        r"""Export the resource using a specific export type using the CLI.

        :param export_type: The export format.
        :type export_type: str
        :param path: The path to store.
        :type path: str, optional
        :param name: The name of the file. The identifier is uses as default.
        :type name: str, optional
        :param force: Whether to replace an existing file with identical name.
        :type force: bool, optional
        :param pipe: Flag to indicate if json should be piped.
        :type pipe: bool, optional
        :param use_folder: Flag indicating if the a folder with the name of the
            resource's identifier should be created within given *path*. The
            exported file is stored in this folder.
        :param \**kwargs: Additional parameters.
        :type \**kwargs: dict
        :raises KadiAPYInputError: If export type is invalid or if not json is used as
            input type togehter with pipe.
        :raises KadiAPYRequestError: If request was not successful.
        """

        # pylint: disable=arguments-differ

        if not pipe:
            if name is None:
                name = self.meta["identifier"]

            if use_folder:
                identifier = self.meta["identifier"]
                path = os.path.join(path, identifier)
                try:
                    os.mkdir(path)
                except FileExistsError:
                    pass

            path = os.path.join(path, name)

            file_extensions = {
                "json": ".json",
                "json-schema": ".json",
                "pdf": ".pdf",
                "qr": ".png",
                "rdf": ".ttl",
                "ro-crate": ".eln",
            }

            if export_type not in file_extensions:
                raise KadiAPYInputError(f"Export type '{export_type}' is invalid.")

            file_extension = file_extensions[export_type]

            if not path.endswith(file_extension):
                path = f"{path}{file_extension}"

            if os.path.isfile(path) and not force:
                self.error(
                    f"A file with the name '{path}' already exists.\nFile"
                    f" '{path}' was not replaced. Use '-f' to force overwriting"
                    " existing file."
                )
                sys.exit(1)

        response = super().export(path, export_type, pipe, **kwargs)

        if response.status_code == 200:
            if pipe:
                if export_type in {"json", "json-schema"}:
                    self.info(response.content)
                    return
                raise KadiAPYInputError(
                    f"Export type '{export_type}' is not valid with 'pipe'."
                )

            self.info(
                f"Successfully exported {self} as {export_type} and stored in '{path}'."
            )
        else:
            self.error(f"Something went wrong when trying to export the {self}.")
            self.raise_request_error(response)


def validate_metadatum(metadatum, value, type, unit):
    """Check correct form for metadatum."""

    metadatum_type = type

    if metadatum_type is None:
        metadatum_type = "string"

    if metadatum_type not in ["string", "integer", "boolean", "float"]:
        raise KadiAPYInputError(
            f"The type {metadatum_type} is given. However, only 'string', 'integer', "
            "'boolean' or 'float' are allowed."
        )

    mapping_type = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "float": "float",
    }

    metadatum_type = mapping_type[metadatum_type]

    if metadatum_type not in ["int", "float"] and unit is not None:
        if unit.strip():
            raise KadiAPYInputError(
                "Specifying a unit is only allowed with 'integer' or 'float'."
            )
        unit = None

    if value is not None:
        if metadatum_type == "bool":
            mapping_value = {"true": True, "false": False}
            if value not in mapping_value:
                raise KadiAPYInputError(
                    "Choosing 'boolean', the value has to be either 'true' or 'false'"
                    f" not '{value}'."
                )
            value = mapping_value[value]

        if metadatum_type == "int":
            try:
                value = int(value)
            except ValueError as e:
                raise KadiAPYInputError(
                    f"Choosing 'integer', the value has to be an integer not '{value}'."
                ) from e

        if metadatum_type == "float":
            try:
                value = float(value)
            except ValueError as e:
                raise KadiAPYInputError(
                    f"Choosing 'float', the value has to be a float not '{value}'."
                ) from e

        if metadatum_type == "str":
            try:
                value = str(value)
            except ValueError as e:
                raise KadiAPYInputError(
                    f"Choosing 'string', the value has to be a string not '{value}'."
                ) from e

    metadatum_new = {
        "type": metadatum_type,
        "unit": unit,
        "key": metadatum,
        "value": value,
    }

    return metadatum_new
