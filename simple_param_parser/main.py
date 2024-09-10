import argparse
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
import os

from enum import Enum


class ParamSource(Enum):
    ENV = 'env'
    CMD = 'cmd'


def parse_params(model: BaseModel, param_names, param_source='env'):
    if not model and not param_names:
        raise Exception("Either pydantic model or params names must be provided")

    if param_source == 'env':
        if model:
            params = parse_params_from_env(model)
        else:
            params = parse_raw_params_from_env(param_names)

    elif param_source == 'cmd':
        if model:
            params = parse_params_from_cmd(model)
        else:
            params = parse_raw_params_from_cmd(param_names)

    else:
        raise Exception('Invalid param_source. param_source must be one of : 1. env  or 2. cmd')

    return params


def parse_raw_params_from_cmd(param_names):
    """
    Accepts a list of parameter names and returns a dictionary
    with the parameter names as keys and their corresponding values as values.

    :param param_names: List of parameter names to accept from the command line.
    :return: Dictionary with parameter names as keys and their values from the command line.
    """
    parser = argparse.ArgumentParser()

    # Add arguments dynamically based on the param_names
    for param_name in param_names:
        parser.add_argument(f'--{param_name}', required=False)

    # Parse command line arguments
    args = parser.parse_args()
    param_dict = vars(args)  # Convert the parsed arguments to a dictionary

    return param_dict


def parse_params_from_cmd(model: BaseModel):
    """
    Accepts a Pydantic model and validates command line parameters using argparse.
    Default values from the Pydantic model will be passed to argparse.

    :param model: A Pydantic model to validate the parameters.
    :return: Dictionary with parameter names and their values if valid, raises an error if invalid.
    """
    parser = argparse.ArgumentParser()

    # Add arguments dynamically based on the Pydantic model fields
    for field_name, field in model.__fields__.items():
        arg_type = field.annotation
        default_value = field.default if field.default is not None else None

        # Add argument to argparse, using the Pydantic field default if provided
        if default_value is not None:
            parser.add_argument(f'--{field_name}', type=arg_type, default=default_value)
        else:
            parser.add_argument(f'--{field_name}', type=arg_type)

    # Parse command line arguments
    args = parser.parse_args()
    param_dict = vars(args)

    try:
        # Create a model instance with the parsed arguments
        parsed_params = model.parse_obj(param_dict)
        return parsed_params
        # return parsed_params.dict()
    except ValidationError as e:
        print("Error in parameter validation:")
        print(e)
        return None


def parse_params_from_env(model: BaseModel):
    """
    Accepts a Pydantic model and validates parameters loaded from .env file or environment variables.

    :param model: A Pydantic model to validate the parameters.
    :return: Dictionary with parameter names and their values if valid, raises an error if invalid.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Prepare a dictionary for the model's parameters
    param_dict = {}

    # Iterate over Pydantic model fields to get values from environment variables or .env file
    for field_name, field in model.__fields__.items():
        env_value = os.getenv(field_name.upper())  # Look for environment variables in uppercase
        if env_value:
            param_dict[field_name] = field.annotation(env_value)
        elif field.default:
            param_dict[field_name] = field.default
        else:
            param_dict[field_name] = None

    try:
        # Create a model instance with the environment variables
        parsed_params = model.parse_obj(param_dict)
        return parsed_params
    except ValidationError as e:
        print(f"Error in parameter validation: {e}")
        return None


def parse_raw_params_from_env(param_names):
    params = {}
    for param in param_names:
        env_value = os.getenv(param.upper())
        params[param] = env_value if env_value else None

    return params
