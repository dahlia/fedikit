from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import NewType, Optional

from langcodes import Language

from ..uri import Uri

__all__ = ["Link", "MediaType", "ResourceDescriptor"]


@dataclass(frozen=True)
class ResourceDescriptor:
    """Describe a resource.  See also :rfc:`7033#section-4.4`."""

    #: A URI that identifies the entity that this descriptor describes.
    subject: Uri

    #: URIs that identify the same entity as the :attr:`subject`.
    aliases: Optional[Sequence[Uri]] = field(default=None)

    #: Convey additional information about the :attr:`subject` of
    #: this descriptor.
    properties: Optional[Mapping[Uri, Optional[str]]] = field(default=None)

    #: Links to other resources.
    links: Optional[Sequence["Link"]] = field(default=None)

    def to_json(
        self,
    ) -> dict[
        str,
        str
        | list[str | dict[str, str | dict[str, Optional[str]]]]
        | dict[str, Optional[str]],
    ]:
        """Convert this to a JSON object."""
        json: dict[
            str,
            str
            | list[str | dict[str, str | dict[str, Optional[str]]]]
            | dict[str, Optional[str]],
        ] = {"subject": str(self.subject)}
        if self.aliases is not None:
            json["aliases"] = [str(alias) for alias in self.aliases]
        if self.properties is not None:
            json["properties"] = {
                str(prop): value for prop, value in self.properties.items()
            }
        if self.links is not None:
            json["links"] = [link.to_json() for link in self.links]
        return json


#: A media type as defined in :rfc:`6838`.
MediaType = NewType("MediaType", str)


@dataclass(frozen=True)
class Link:
    """Represent a link.  See also :rfc:`7033#section-4.4.4`."""

    #: The link's relation type, which is either a URI or a registered
    #: relation type (see :rfc:`5988`).
    rel: Uri | str

    #: The media type of the target resource (see :rfc:`6838`).
    type: Optional[MediaType] = field(default=None)

    #: A URI pointing to the target resource.
    href: Optional[Uri] = field(default=None)

    #: Human-readable titles describing the link relation.  If the language
    #: is unknown or unspecified, the :class:`Language` is
    #: ``Language.get('und')``.
    titles: Optional[Mapping[Language, str]] = field(default=None)

    #: Convey additional information about the link relation.
    properties: Optional[Mapping[Uri, Optional[str]]] = field(default=None)

    def to_json(self) -> dict[str, str | dict[str, Optional[str]]]:
        """Convert this to a JSON object."""
        json: dict[str, str | dict[str, Optional[str]]] = {
            "rel": str(self.rel)
        }
        if self.type is not None:
            json["type"] = str(self.type)
        if self.href is not None:
            json["href"] = str(self.href)
        if self.titles is not None:
            json["titles"] = {
                str(lang): title for lang, title in self.titles.items()
            }
        if self.properties is not None:
            json["properties"] = {
                str(prop): value for prop, value in self.properties.items()
            }
        return json
