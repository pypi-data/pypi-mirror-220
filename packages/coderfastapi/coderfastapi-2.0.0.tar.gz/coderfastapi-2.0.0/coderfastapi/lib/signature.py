import copy
from inspect import Parameter, Signature
from typing import Sequence


def copy_parameters(
    from_signature: Signature,
    to_signature: Signature,
    parameter_keys: Sequence[str],
) -> Signature:
    filtered_parameters = [
        to_signature.parameters[key]
        for key in to_signature.parameters
        if key not in parameter_keys
    ]

    new_parameters = _bulk_create_new_parameters(
        filtered_parameters, [from_signature.parameters[key] for key in parameter_keys]
    )
    new_signature = to_signature.replace(parameters=new_parameters)
    return new_signature


def _bulk_create_new_parameters(
    existing_parameters: list[Parameter],
    new_parameters: list[Parameter],
) -> list[Parameter]:
    parameters = existing_parameters
    for new_parameter in new_parameters:
        parameters = _create_new_parameters(parameters, new_parameter)
    return parameters


def _create_new_parameters(
    existing_parameters: list[Parameter],
    new_parameter: Parameter,
) -> list[Parameter]:
    if not existing_parameters:
        return [new_parameter]

    if check_parameter_has_default(new_parameter):
        new_parameters = copy.copy(existing_parameters)
        for i, parameter in enumerate(new_parameters):
            if check_parameter_has_default(parameter):
                new_parameters.insert(i, new_parameter)
                return new_parameters

        return existing_parameters + [new_parameter]
    else:
        return [new_parameter] + existing_parameters


def check_parameter_has_default(parameter: Parameter) -> bool:
    return parameter.default != Parameter.empty
