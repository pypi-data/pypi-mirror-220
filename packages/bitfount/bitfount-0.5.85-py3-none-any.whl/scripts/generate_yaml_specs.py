"""Generate OpenAPI specs for the ModellerConfig class."""
from importlib.metadata import version
import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Type, Union, cast

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec.ext.marshmallow.field_converter import FieldConverterMixin
import desert
from fire import Fire
from marshmallow import RAISE, Schema
import marshmallow.fields as fields
from marshmallow_union import Union as M_Union

from bitfount.runners.config_schemas import ModellerConfig, PodConfig


def resolve_schema_cls(schema: Union[Schema, Type[Schema]]) -> Type[Schema]:
    """Return schema class for given schema (instance or class).

    Args:
        schema: Instance or class of marshmallow.Schema

    Returns:
        Schema class of given schema.

    Raises:
        LookupError: If schema class could not be found.
    """
    if isinstance(schema, type) and issubclass(schema, Schema):
        return schema
    if isinstance(schema, Schema):
        return type(schema)
    raise LookupError(f"Could not find schema class for {schema}")


def maybe_replace_nested_schema(
    field: fields.Nested, local_schema_register: Dict[str, Type[Schema]]
) -> None:
    """Looks into a Nested field and attempts to replace its schema.

    Tries to find a schema type for the same class in the local_schema_register.
    If found mutates the Nested field to reference that schema type instead
    (de-duplicate). If not found, calls the base recursive method on that schema so
    that it's added to the register and processed.

    Args:
        field: The Nested field to mutate.
        local_schema_register: The local schema register.
    """
    field_schema_cls = resolve_schema_cls(field.nested)  # type: ignore[arg-type] # Reason: it works # noqa: B950
    if field_schema_cls.__name__ in local_schema_register:
        field.nested = local_schema_register[field_schema_cls.__name__]
        field._schema = None
    else:
        recursive_deduplicate_schema_classes(field.schema, local_schema_register)


def recursive_find_nested(
    field: fields.Field, local_schema_register: Dict[str, Type[Schema]]
) -> None:
    """Look into a Field and recurse until a Nested is found.

    This method will:
     - if a Nested is found call `maybe_replace_nested_schema`
     - if a Field containing other Fields is found, recurse further
     - if a simple Field is found do nothing

    Args:
        field: The field to inspect.
        local_schema_register: The local schema register.
    """
    if isinstance(field, fields.Nested):
        maybe_replace_nested_schema(field, local_schema_register)
    if isinstance(field, fields.List):
        recursive_find_nested(field.inner, local_schema_register)
    if isinstance(field, M_Union):
        for union_field in field._candidate_fields:  # type: ignore[attr-defined] # Reason: Private attribute # noqa: B950
            recursive_find_nested(union_field, local_schema_register)
    if isinstance(field, fields.Mapping) and isinstance(
        field.value_field, fields.Nested
    ):
        maybe_replace_nested_schema(field.value_field, local_schema_register)


def recursive_deduplicate_schema_classes(
    schema: Union[Schema, Type[Schema]], local_schema_register: Dict[str, Type[Schema]]
) -> None:
    """Save this schema to the local schema register.

    Also process its fields to find and replace replicated schemas for the same class

    Args:
        schema: The schema to process.
        local_schema_register: The local schema register.
    """
    # save current schema to the register
    schema_cls = resolve_schema_cls(schema)
    local_schema_register[schema_cls.__name__] = schema_cls
    # process fields
    for field in schema.fields.values():
        recursive_find_nested(field, local_schema_register)


def set_meta_unknown(
    local_schema_register: Dict[str, Type[Schema]], meta_unknown: str
) -> None:
    """For all the schemas in the local_schema_register, set Meta.unknown.

    This is required because of https://github.com/python-desert/desert/issues/100.

    Args:
        local_schema_register: The local schema register.
        meta_unknown: The desired value of Meta.unknown.
    """
    for schema in local_schema_register.values():
        schema.Meta.unknown = meta_unknown  # type: ignore[attr-defined] # Reason: It does have this attribute # noqa: B950


def convert_union_to_spec(
    self: FieldConverterMixin, field: fields.Field, **kwargs: Any
) -> Dict[str, List[Any]]:
    """Converts M_Unions fields to OpenAPI spec.

    The default implementation does not handle Unions, as mentioned here:
    https://github.com/marshmallow-code/apispec/issues/837
    """
    ret = {}
    if isinstance(field, M_Union):
        ret["oneOf"] = [
            self.field2property(f)
            for f in field._candidate_fields  # type: ignore[attr-defined] # Reason: Private attribute # noqa: B950
        ]
    return ret


def remove_generic_plugin_options_from_spec(spec: APISpec) -> APISpec:
    """Remove GenericPluginOptions from the spec."""
    # Remove Generic Protocol from the spec
    del spec.components.schemas["GenericProtocolConfig"]
    for i, protocol in enumerate(
        spec.components.schemas["TaskConfig"]["properties"]["protocol"]["oneOf"]
    ):
        if protocol["$ref"] == "#/components/schemas/GenericProtocolConfig":
            spec.components.schemas["TaskConfig"]["properties"]["protocol"][
                "oneOf"
            ].pop(i)
            break
    # Remove Generic Algorithm from the spec
    del spec.components.schemas["GenericAlgorithmConfig"]
    for i, algorithm in enumerate(
        spec.components.schemas["TaskConfig"]["properties"]["algorithm"]["oneOf"]
    ):
        if algorithm.get("$ref") == "#/components/schemas/GenericAlgorithmConfig":
            spec.components.schemas["TaskConfig"]["properties"]["algorithm"][
                "oneOf"
            ].pop(i)
        if "items" in algorithm:
            for j, algo in enumerate(algorithm["items"]["oneOf"]):
                if "#/components/schemas/GenericAlgorithmConfig" in algo["$ref"]:
                    spec.components.schemas["TaskConfig"]["properties"]["algorithm"][
                        "oneOf"
                    ][i]["items"]["oneOf"].pop(j)

    return spec


def generate_spec(root_class: type) -> Dict[str, Any]:
    """Generate OpenAPI spec for given root class.

    Args:
        root_class: Class to generate OpenAPI spec for.

    Returns:
        OpenAPI spec for given root class as a dict.
    """
    ma_plugin = MarshmallowPlugin()
    root_class_name = root_class.__name__
    spec = APISpec(
        title=f"{root_class_name} OpenAPI Spec",
        version=version("bitfount"),
        openapi_version="3.1.0",
        plugins=[ma_plugin],
        options={
            "externalDocs": {
                "description": "More information about the YAML API",
                "url": "https://docs.bitfount.com/api/bitfount/runners/config_schemas",
            }
        },
    )
    assert (  # nosec[assert_used] # Reason: Reassuring mypy
        ma_plugin.converter is not None
    )
    ma_plugin.converter.add_attribute_function(convert_union_to_spec)
    schema = desert.schema_class(root_class)()
    local_schema_register: Dict[str, Type[Schema]] = {}
    recursive_deduplicate_schema_classes(schema, local_schema_register)
    set_meta_unknown(local_schema_register, RAISE)
    spec.components.schema(root_class_name, schema=schema)
    if root_class_name == "ModellerConfig":
        spec = remove_generic_plugin_options_from_spec(spec)
    spec_dict = cast(dict, spec.to_dict())
    # This signifies that the top level object is the rootClass
    spec_dict["allOf"] = [{"$ref": f"#/components/schemas/{root_class_name}"}]
    # OpenAPI version 3.1.0 corresponds to JSON Schema draft 2020-12
    spec_dict["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return spec_dict


def generate_yaml_specs(output_directory: str = ".", *modules_to_import: str) -> None:
    """Generate OpenAPI specs for the YAML interface.

    Args:
        output_directory: Directory to store the generated specs,
                          will be created if it doesn't already exist
        modules_to_import: module paths to be imported,
                           this is used so that any plugins can be
                           loaded and included in the specs
    """
    if modules_to_import:
        [importlib.import_module(module) for module in modules_to_import]

    _output_directory = Path(output_directory)

    _output_directory.mkdir(parents=True, exist_ok=True)
    with (_output_directory / "task-spec.json").open(mode="w", encoding="utf-8") as f:
        json.dump(generate_spec(ModellerConfig), f, indent=2, sort_keys=True)
        f.write("\n")

    with (_output_directory / "pod-spec.json").open(mode="w", encoding="utf-8") as f:
        json.dump(generate_spec(PodConfig), f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    Fire(generate_yaml_specs)
