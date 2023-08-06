"""Raw category."""

from typing import List, Union

from ..common_types import (
    TypeSchema,
    BreadCrumbs,
    SizedCloudImage,
    VisibleType,
    builtins,
)


class CategoryMedia(TypeSchema):
    """Category media."""

    cover: SizedCloudImage
    preview: SizedCloudImage


class TypeCategory(builtins.TypeRaw):
    """Raw type category."""

    name: str
    slug: str

    is_actual: bool
    visible_type: VisibleType
    media: CategoryMedia

    breadcrumbs: Union[List[BreadCrumbs], None]

    parent_pk: Union[int, None]
    old_slug: Union[str, None]

    created: Union[int, None]
    updated: Union[int, None]
