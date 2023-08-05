import copy
import json
import re

import lazy_object_proxy
import marshmallow as ma
from marshmallow import fields
from oarepo_model_builder.datatypes import ObjectDataType
from oarepo_model_builder.stack import ReplaceElement
from oarepo_model_builder.stack.stack import ModelBuilderStack
from oarepo_model_builder.utils.jinja import split_base_name
from oarepo_model_builder.validation import InvalidModelException
from oarepo_model_builder.validation.model_validation import model_validator
from oarepo_model_builder.validation.property import StrictString
from oarepo_model_builder.validation.property_marshmallow import (
    ObjectPropertyMarshmallowSchema,
)
from oarepo_model_builder.validation.ui import (
    ObjectPropertyUISchema,
)


class StringOrSchema(fields.Field):
    def __init__(self, string_field, schema_field, **kwargs) -> None:
        super().__init__(**kwargs)
        self.string_field = string_field
        self.schema_field = schema_field

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, str):
            return self.string_field._deserialize(value, attr, data, **kwargs)
        else:
            return self.schema_field._deserialize(value, attr, data, **kwargs)

    def _serialize(self, value, attr, obj, **kwargs):
        if isinstance(value, str):
            return self.string_field._serialize(value, attr, obj, **kwargs)
        else:
            return self.schema_field._serialize(value, attr, obj, **kwargs)

    def _validate(self, value):
        if isinstance(value, str):
            return self.string_field._validate(value)
        else:
            return self.schema_field._validate(value)


class RelationSchema(ma.Schema):
    class ImportSchema(ma.Schema):
        import_str = fields.String(data_key="import", required=True)
        alias = fields.String(required=False)

    class KeySchema(ma.Schema):
        key = fields.String(required=True)
        model = fields.Nested(
            lambda: model_validator.validator_class("object-field")(), required=False
        )
        target = fields.String(required=False)

    name = fields.String(required=False)
    model = fields.String(required=True)
    keys_field = fields.List(
        StringOrSchema(StrictString(), fields.Nested(KeySchema)),
        data_key="keys",
        required=False,
    )
    model_class = fields.String(data_key="model-class", required=False)
    schema_prefix = fields.String(data_key="schema-prefix", required=False)
    relation_class = fields.String(data_key="relation-class", required=False)
    pid_field = fields.String(data_key="pid-field", required=False)
    related_part = fields.String(data_key="related-part", required=False)
    relation_args = fields.Dict(
        fields.String(),
        fields.String(),
        required=False,
        data_key="relation-args",
    )
    imports = fields.List(fields.Nested(ImportSchema), required=False)
    flatten = fields.Boolean(required=False)

    class Meta:
        unknown = ma.RAISE


class RelationDataType(ObjectDataType):
    model_type = "relation"

    def prepare(self, context):
        data = self.definition
        name = data.pop("name", None)
        model_name = data.pop("model")
        keys = data.pop("keys", ["id", "metadata.title"])
        flatten = data.pop("flatten", False)
        model_class = data.pop("model-class", None)
        schema_prefix = data.pop("schema-prefix", None)
        relation_class = data.pop("relation-class", None)

        relation_args = data.pop("relation-args", {})
        imports = data.pop("imports", [])
        pid_field = data.pop("pid-field", None)
        related_part = data.pop("related-part", None)

        if not name:
            if self.stack.top.schema_element_type == "items":
                name = self.stack[-2].key + "_item"
            else:
                name = self.key
        if not schema_prefix:
            if self.stack.top.schema_element_type == "items":
                schema_prefix = self.stack[-2].key.title() + "Item"
            else:
                schema_prefix = self.key.title()
        schema_prefix = re.sub("\W", "", schema_prefix)

        internal_link = model_name.startswith("#")

        if not relation_class:
            if internal_link:
                relation_class = "InternalRelation"
            else:
                relation_class = "PIDRelation"

        # import oarepo classes but only if used
        imports.append({"import": f"oarepo_runtime.relations.RelationsField"})
        imports.append({"import": f"oarepo_runtime.relations.PIDRelation"})
        imports.append({"import": f"oarepo_runtime.relations.InternalRelation"})

        transformed_keys = []
        for k in keys:
            if isinstance(k, str):
                k = {"key": k, "target": k}
            if not k.get("target"):
                k["target"] = k["key"]
            if flatten and k["target"].startswith("metadata."):
                k["target"] = k["target"][len("metadata.") :]
            transformed_keys.append(k)
        keys = transformed_keys

        model_data = lazy_object_proxy.Proxy(lambda: self.get_model(model_name))

        def get_properties():
            props_container = model_data["model"]
            if "properties" not in props_container:
                if "items" in props_container:
                    props_container = props_container["items"]

            if "properties" not in props_container:
                raise InvalidModelException(
                    f"Reference {model_name} can only point to object, it is pointing to {json.dumps(model_data['model'], indent=4)}"
                )

            return props_container["properties"]

        model_properties = lazy_object_proxy.Proxy(get_properties)

        if not model_class:
            model_class = model_data["model"].get("record-class")
            if model_class:
                model_class = split_base_name(model_class)
                imports.append({"import": model_data["model"]["record-class"]})

        if not pid_field and model_class:
            pid_field = f"{model_class}.pid"

        if not related_part and not pid_field and internal_link:
            related_part = repr(model_data["id"])

        # insert properties
        props = {}
        for fld in keys:
            if fld.get("model"):
                self._copy_direct_field(props, fld)
            else:
                self._copy_field_definition(props, model_properties, fld, model_name)
        props["@v"] = {
            "type": "keyword",
            "marshmallow": {
                "field-name": "_version",
                "field-class": "ma_fields.String",
            },
            "ui": {
                "marshmallow": {
                    "field-name": "_version",
                    "field-class": "ma_fields.String",
                }
            },
        }

        self._prefix_marshmallow_classes(props, schema_prefix)

        set_if_not_none(data, "properties", props)

        set_if_not_none(data, "name", name)
        set_if_not_none(data, "model", model_name)
        set_if_not_none(data, "keys", keys)
        set_if_not_none(data, "model-class", model_class)
        set_if_not_none(data, "schema-prefix", schema_prefix)
        set_if_not_none(data, "relation-class", relation_class)
        set_if_not_none(data, "relation-args", relation_args)
        set_if_not_none(data, "imports", imports)
        if pid_field:
            set_if_not_none(data, "pid-field", pid_field)
        if related_part:
            set_if_not_none(data, "related-part", related_part)

        self._remove_mapping_incompatibilities(data)
        super().prepare(context)

    def get_model(self, model_name):
        if model_name.startswith("#"):
            reference_id = model_name[1:]
            if reference_id == "":
                referenced_elements = [("", {"properties": self.model["properties"]})]
            else:
                referenced_elements = list(find_reference(self.model, reference_id))
            if not referenced_elements:
                raise InvalidModelException(
                    f"Reference {reference_id} used from {self.stack.path} not found in the document"
                )
            if len(referenced_elements) > 1:
                raise InvalidModelException(f"Duplicated reference {reference_id}!")
            path, reference = referenced_elements[0]
            return {"model": reference, "id": path}
        try:
            return self.schema._load(model_name)
        except Exception as e:
            raise InvalidModelException("Can not load included model") from e

    def _copy_field_definition(self, props, included_props, fld, model_name):
        field_path = fld["key"].split(".")
        target_path = fld["target"].split(".")

        for pth_elem in field_path[:-1]:
            if pth_elem not in included_props:
                raise InvalidModelException(
                    f"Field path {field_path} is invalid within model {model_name}"
                )
            included_props = included_props[pth_elem]["properties"]

        for pth_elem in target_path[:-1]:
            if pth_elem not in props:
                props[pth_elem] = {"type": "object", "properties": {}}
            props = props[pth_elem]["properties"]

        if field_path[-1] in included_props:
            included_model = copy.deepcopy(included_props[field_path[-1]])
            self._make_field_serializable(included_model.get("marshmallow", None))
            props[target_path[-1]] = included_model

    def _copy_direct_field(self, props, fld):
        included_model = copy.deepcopy(fld.model)
        self._make_field_serializable(included_model.get("marshmallow", None))
        props[fld.key] = included_model

    def _make_field_serializable(self, marshmallow):
        if not marshmallow:
            return
        marshmallow.pop("read", None)
        marshmallow.pop("write", None)

    def _prefix_marshmallow_classes(self, props, schema_prefix):
        if not isinstance(props, dict):
            return
        if "properties" in props and isinstance(props["properties"], dict):
            # i am an object or nested
            if "marshmallow" in props:
                schema_class = props["marshmallow"].get("schema-class", None)
                if schema_class:
                    schema_class = schema_class.rsplit(".", maxsplit=1)[-1]
                    props["marshmallow"]["schema-class"] = schema_prefix + schema_class
            if "ui" in props and "marshmallow" in props["ui"]:
                schema_class = props["ui"]["marshmallow"].get("schema-class", None)
                if schema_class:
                    schema_class = schema_class.rsplit(".", maxsplit=1)[-1]
                    props["ui"]["marshmallow"]["schema-class"] = (
                        schema_prefix + schema_class
                    )
        for v in props.values():
            self._prefix_marshmallow_classes(v, schema_prefix)

    def _remove_mapping_incompatibilities(self, props, mapping_in_parent=False):
        if not isinstance(props, dict):
            return
        if mapping_in_parent:
            if "copy-to" in props:
                del props["copy-to"]
            if "copy_to" in props:
                del props["copy_to"]

        for k, v in props.items():
            self._remove_mapping_incompatibilities(
                v, mapping_in_parent or k == "mapping"
            )

    class ModelSchema(
        RelationSchema,
        ObjectPropertyMarshmallowSchema,
        ObjectPropertyUISchema,
        ObjectDataType.ModelSchema,
    ):
        pass


def find_reference(model, reference_id):
    stack = ModelBuilderStack()

    def _find_reference_internal(key, value, path):
        stack.push(key, value)
        if isinstance(value, dict):
            if stack.top.schema_element_type == "property":
                if path:
                    path += "."
                path += key
            if stack.top.schema_element_type in ("property", "items"):
                if value.get("id", None) == reference_id:
                    yield path, value
            for k, v in value.items():
                yield from _find_reference_internal(k, v, path)
        stack.pop()

    yield from _find_reference_internal("model", model, "")


class PropertyIDSchema(ma.Schema):
    id = fields.String(required=False)


DATATYPES = [RelationDataType]
VALIDATORS = {
    "property": [PropertyIDSchema],
}


def set_if_not_none(data, key, value):
    if value is not None:
        data[key] = value
