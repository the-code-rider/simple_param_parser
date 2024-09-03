import sys


def accept_params(param_names):
    """
    Accepts a list of parameter names and returns a dictionary
    with the parameter names as keys and their corresponding values as values.

    :param param_names: List of parameter names to accept from the command line.
    :return: Dictionary with parameter names as keys and their values from the command line.
    """
    args = sys.argv[1:]  # Skip the script name
    result = {}

    for param_name in param_names:
        if param_name in args:
            value_index = args.index(param_name) + 1
            if value_index < len(args):
                result[param_name] = args[value_index]
            else:
                result[param_name] = None  # No value provided after the param name
        else:
            result[param_name] = None  # Param name not provided

    return result
