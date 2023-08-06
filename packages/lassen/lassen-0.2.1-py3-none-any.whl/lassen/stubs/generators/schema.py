import inspect
import typing
from typing import Callable, Type, get_args, get_origin

from jinja2 import Environment, FileSystemLoader, select_autoescape

from lassen.stubs.base import BaseGenerator, BaseStub
from lassen.stubs.field import UNSET_VALUE, FieldDefinition
from lassen.stubs.generators.common import (
    ExtractedStubImports,
    extract_type_hints,
    format_dict_as_kwargs,
    format_typehint_as_string,
    get_ordered_instance_variables,
)
from lassen.stubs.templates import get_template_path


def make_optional(type_hint):
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is typing.Union:
        if any(arg is type(None) for arg in args):
            # The type hint is already Optional
            return type_hint
        else:
            # Convert the Union to Optional by adding None as an argument
            return typing.Union[*args, type(None)]
    else:
        # If the type hint is not a Union, make it Optional
        return typing.Optional[type_hint]


class SchemaGenerator(BaseGenerator):
    def __call__(
        self,
        model: Type[BaseStub],
        import_hints: ExtractedStubImports,
    ):
        model_name = model.__name__
        _, all_deps = self.get_model_fields(model)
        create_fields, _ = self.get_model_fields(model, lambda f: f.create)
        update_fields, _ = self.get_model_fields(model, lambda f: f.update)
        read_fields, _ = self.get_model_fields(model, lambda f: f.read)
        filter_fields, _ = self.get_model_fields(model, lambda f: f.filter)

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(get_template_path("")),
            autoescape=select_autoescape(["html", "xml"]),
        )

        template = env.get_template("schema.py.j2")
        return template.render(
            model_name=model_name,
            create_fields=create_fields,
            update_fields=update_fields,
            read_fields=read_fields,
            filter_fields=filter_fields,
            dependencies=sorted([dependency for dependency in all_deps if dependency]),
            clone_imports=import_hints.clone_imports,
            clone_typechecking_imports=import_hints.clone_typechecking_imports,
        )

    def get_model_fields(
        self,
        model: Type[BaseStub],
        field_predicate: Callable[[FieldDefinition], bool] | None = None,
        force_optional: bool = False,
    ):
        fields: list[tuple[str, FieldDefinition]] = list(
            inspect.getmembers(
                model,
                lambda m: isinstance(m, FieldDefinition)
                and (not field_predicate or field_predicate(m)),
            )
        )

        fields_ordered = get_ordered_instance_variables(model)
        fields = sorted(fields, key=lambda f: fields_ordered.index(f[0]))

        declarations: list[str] = []
        dependencies: set[str | None] = set()
        typehints = extract_type_hints(model, FieldDefinition)

        for name, field in fields:
            # Determine if this generator should process this field
            if field.generators is not None:
                if self not in field.generators:
                    continue

            typehint = typehints[name]
            if force_optional:
                typehint = make_optional(typehint)

            mapped_typehint, type_dependencies = format_typehint_as_string(typehint)

            declaration = f"{name}: {mapped_typehint}"
            field_arguments = {}
            if force_optional:
                field_arguments["default"] = "None"
            elif not isinstance(field.default, UNSET_VALUE):
                field_arguments["default"] = field.default

            if field.description:
                field_arguments["description"] = field.description

            if field_arguments:
                declaration += f" = Field({format_dict_as_kwargs(field_arguments)})"
            declarations.append(declaration)
            dependencies |= set(type_dependencies)

        if not declarations:
            declarations.append("pass")

        return declarations, list(dependencies)
