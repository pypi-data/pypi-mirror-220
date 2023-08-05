from __future__ import annotations

import datetime
import json
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from ... import helpers, models
from ...catalog import Catalog, Dataset
from ...exception import FrictionlessException
from ...package import Package
from ...platform import platform
from ...resource import Resource
from ...system import Adapter
from .control import ZenodoControl

if TYPE_CHECKING:
    from pyzenodo3 import Record  # type: ignore


class ZenodoAdapter(Adapter):
    """Read and write data from/to Zenodo"""

    def __init__(self, control: ZenodoControl):
        self.control = control

    # Read

    def read_package(self) -> Package:
        client = platform.pyzenodo3.Zenodo(api_key=self.control.apikey)  # type: ignore
        if not self.control.record:
            note = "Record is required."
            raise FrictionlessException(note)
        assert self.control.formats
        package = Package()
        try:
            dataset = client.get_record(self.control.record)
            if dataset:
                name = self.control.name or dataset.data["metadata"]["title"]
                package = get_package(dataset, name, self.control.formats)
        except Exception as exception:
            note = "Zenodo API error" + repr(exception)
            raise FrictionlessException(note)
        if isinstance(package, Package) and package.resources:  # type: ignore
            return package
        note = "Package/s not found"
        raise FrictionlessException(note)

    # Write

    def write_package(self, package: Package):
        client = platform.pyzenodo3_upload

        assert self.control.base_url
        assert self.control.apikey
        client.BASE_URL = self.control.base_url  # type: ignore
        metafn = self.control.metafn

        if not metafn:
            meta_data = generate_metadata(package)
            with tempfile.NamedTemporaryFile("wt", delete=False) as file:
                json.dump(meta_data, file, indent=2)
                metafn = file.name

        if metafn:
            # Check if metadata is a JSON Object
            if isinstance(metafn, dict):
                meta_data = generate_metadata(metadata=metafn)
                with tempfile.NamedTemporaryFile("wt", delete=False) as file:
                    json.dump(meta_data, file, indent=2)
                    metafn = file.name

        try:
            deposition_id = self.control.deposition_id
            if not deposition_id:
                # Create a deposition resource
                deposition_id = client.create(  # type: ignore
                    token=self.control.apikey, base_url=self.control.base_url
                )
            metafn = Path(metafn).expanduser()
            client.upload_meta(  # type: ignore
                token=self.control.apikey,
                metafn=metafn,
                depid=deposition_id,  # type: ignore
            )

            # Process resources
            resources: List[Path] = []
            for key, resource in enumerate(package.resources):
                if resource.data:
                    resource_file_name = f"{resource.name}.json" or f"resource{key}.json"
                    resource_path = os.path.join(
                        self.control.tmp_path or "", resource_file_name
                    )
                    resource.to_json(resource_path)
                    resources.append(Path(resource_path).expanduser())
                    continue

                resource_path = resource.path or ""
                if resource_path.startswith(("http://", "https://")):
                    continue

                if resource.basepath:
                    resource_path = os.path.join(
                        str(resource.basepath), str(resource.path)
                    )
                resources.append(Path(resource_path).expanduser())
            package_path = os.path.join(self.control.tmp_path or "", "datapackage.json")
            package.to_json(package_path)

            # Upload package and resources
            client.upload_data(  # type: ignore
                token=self.control.apikey,
                datafn=Path(package_path).expanduser(),
                depid=deposition_id,  # type: ignore
                base_url=self.control.base_url,
            )
            for resource_path in resources:
                resource_path = Path(resource_path).expanduser()
                client.upload_data(  # type: ignore
                    token=self.control.apikey,
                    datafn=resource_path,
                    depid=deposition_id,  # type: ignore
                    base_url=self.control.base_url,
                )
            return models.PublishResult(
                url=f"https://zenodo.org/record/{deposition_id}",
                context=dict(deposition_id=deposition_id),
            )
        except Exception as exception:
            note = "Zenodo API error" + repr(exception)
            raise FrictionlessException(note)

    # Experimental

    def read_catalog(self) -> Catalog:
        packages: List[Union[Package, str]] = []
        options: Dict[str, Any] = {}

        # Single record
        if self.control.record:
            packages.append(self.read_package())
            return Catalog(
                datasets=[
                    Dataset(name=package.name, package=package)  # type: ignore
                    for package in packages
                ]
            )

        # DOI
        assert self.control.formats
        client = platform.pyzenodo3.Zenodo(api_key=self.control.apikey)  # type: ignore
        if self.control.doi:
            dataset = client.find_record_by_doi(self.control.doi)
            name = self.control.name or dataset.data["metadata"]["title"]
            package = get_package(dataset, name, self.control.formats)
            if isinstance(package, Package) and package.resources:  # type: ignore
                packages.append(package)
            return Catalog(
                datasets=[
                    Dataset(name=package.name, package=package)  # type: ignore
                    for package in packages
                ]
            )

        # Search
        if self.control.search:
            search = self.control.search.replace(
                "/", " "
            )  # zenodo can't handle '/' in search query
            options["q"] = search
        options["status"] = self.control.status
        options["sort"] = self.control.sort
        options["page"] = self.control.page
        options["size"] = self.control.size
        options["all_versions"] = self.control.all_versions
        options["communities"] = self.control.communities
        options["type"] = self.control.rtype
        options["subtype"] = self.control.subtype
        options["bounds"] = self.control.bounds
        options["custom"] = self.control.rcustom
        options = {key: value for key, value in options.items() if value}
        try:
            records = client._get_records(options)
            for dataset in records:
                name = self.control.name or dataset.data["metadata"]["title"]
                package = get_package(dataset, name, self.control.formats)
                if isinstance(package, Package) and package.resources:  # type: ignore
                    packages.append(package)
        except Exception as exception:
            note = "Zenodo API error" + repr(exception)
            raise FrictionlessException(note)
        if packages:
            return Catalog(
                datasets=[
                    Dataset(name=package.name, package=package)  # type: ignore
                    for package in packages
                ]
            )
        note = "Package/s not found"
        raise FrictionlessException(note)


def get_package(record: Record, title: str, formats: List[str]) -> Package:  # type: ignore
    package = Package(title=title)
    package.title = title
    for file in record.data["files"]:  # type: ignore
        path = file["links"]["self"]  # type: ignore
        is_resource_file = any(path.endswith(ext) for ext in formats)  # type: ignore
        if path.endswith(("datapackage.json")):  # type: ignore
            return Package.from_descriptor(path, title=title)  # type: ignore
        if path.endswith("zip") and not is_resource_file:  # type: ignore
            try:
                package = Package(path)  # type: ignore
                package.title = title
                return package
            except FrictionlessException as exception:
                # Skips package descriptor not found exception
                # and continues reading files.
                if "[Errno 2] No such file or directory" not in str(exception):
                    raise exception
        if is_resource_file:
            package.basepath = f'https://zenodo.org/api/files/{file["bucket"]}'
            resource = Resource(path=file["key"])  # type: ignore
            package.add_resource(resource)
    return package


def generate_metadata(
    package: Optional[Package] = None, *, metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    meta_data: Union[str, Dict[str, Any], None] = {"metadata": {}}
    if not metadata and not package:
        note = "Zenodo API Metadata Creation error: Either metadata or package should be provided to generate metadata."
        raise FrictionlessException(note)

    if metadata:
        if (
            not metadata.get("title")
            or not metadata.get("description")
            or not metadata.get("creators")
        ):
            note = "Zenodo API Metadata Creation error: missing title or description or creators."
            raise FrictionlessException(note)

        meta_data["metadata"] = metadata
        if "keywords" not in meta_data["metadata"]:
            meta_data["metadata"]["keywords"] = ["frictionlessdata"]

        return helpers.remove_non_values(meta_data)

    assert package

    if not package.title or not package.description or not package.contributors:
        note = "Zenodo API Metadata Creation error: Unable to read title or description or contributors from package descriptor."
        raise FrictionlessException(note)

    meta_data["metadata"] = {
        "title": package.title,
        "description": package.description,
        "publication_date": package.created or str(datetime.datetime.now()),
        "upload_type": "dataset",
        "access_right": "open",
    }
    if package.licenses:
        meta_data["metadata"]["creators"] = package.licenses[0].get("name")  # type: ignore

    creators: List[Dict[str, Any]] = []
    for contributor in package.contributors:
        creators.append(
            {
                "name": contributor.get("title"),
                "affiliation": contributor.get("organization"),
            }
        )
    keywords = package.keywords or []
    if "frictionlessdata" not in package.keywords:
        keywords.append("frictionlessdata")

    if creators:
        meta_data["metadata"]["creators"] = creators  # type: ignore
    meta_data["metadata"]["keywords"] = keywords  # type: ignore
    return helpers.remove_non_values(meta_data)
