import os
import importlib
import traceback

from typing import Any

from vantage6.common.client import deserialization
from vantage6.tools import serialization
from vantage6.tools.util import info, error
from vantage6.tools.exceptions import DeserializationException


def wrap_algorithm(module: str, log_traceback: bool = True) -> None:
    """
    Wrap an algorithm module to provide input and output handling for the
    vantage6 infrastructure.

    Data is received in the form of files, whose location should be
    specified in the following environment variables:

    - ``INPUT_FILE``: input arguments for the algorithm. This file should be
      encoded in JSON format.
    - ``OUTPUT_FILE``: location where the results of the algorithm should
      be stored
    - ``TOKEN_FILE``: access token for the vantage6 server REST api
    - ``USER_REQUESTED_DATABASE_LABELS``: comma-separated list of database
      labels that the user requested
    - ``<DB_LABEL>_DATABASE_URI``: uri of the each of the databases that
      the user requested, where ``<DB_LABEL>`` is the label of the
      database given in ``USER_REQUESTED_DATABASE_LABELS``.

    The wrapper expects the input file to be a json file. Any other file
    format will result in an error.

    Parameters
    ----------
    module : str
        Python module name of the algorithm to wrap.
    log_traceback: bool
        Whether to print the full error message from algorithms or not, by
        default False. Algorithm developers should set this to False if
        the error messages may contain sensitive information. By default True.
    """
    info(f"wrapper for {module}")

    # read input from the mounted input file.
    input_file = os.environ["INPUT_FILE"]
    info(f"Reading input file {input_file}")
    input_data = load_input(input_file)

    # make the actual call to the method/function
    info("Dispatching ...")
    output = _run_algorithm_method(input_data, module, log_traceback)

    # write output from the method to mounted output file. Which will be
    # transferred back to the server by the node-instance.
    output_file = os.environ["OUTPUT_FILE"]
    info(f"Writing output to {output_file}")

    _write_output(output, output_file)


def _run_algorithm_method(input_data: dict, module: str,
                          log_traceback: bool = True) -> Any:
    """
    Load the algorithm module and call the correct method to run an algorithm.

    Parameters
    ----------
    input_data : dict
        The input data that is passed to the algorithm. This should at least
        contain the key 'method' which is the name of the method that should be
        called. Another often used key is 'master' which indicates that this
        container is a master container. Other keys depend on the algorithm.
    module : str
        The module that contains the algorithm.
    log_traceback: bool, optional
        Whether to print the full error message from algorithms or not, by
        default False. Algorithm developers should set this to False if
        the error messages may contain sensitive information. By default True.

    Returns
    -------
    Any
        The result of the algorithm.
    """
    # import algorithm module
    try:
        lib = importlib.import_module(module)
        info(f"Module '{module}' imported!")
    except ModuleNotFoundError:
        error(f"Module '{module}' can not be imported! Exiting...")
        exit(1)

    # get algorithm method and attempt to load it
    method_name = input_data["method"]
    try:
        method = getattr(lib, method_name)
    except AttributeError:
        error(f"Method '{method_name}' not found!\n")
        exit(1)

    # get the args and kwargs input for this function.
    args = input_data.get("args", [])
    kwargs = input_data.get("kwargs", {})

    # try to run the method
    try:
        result = method(*args, **kwargs)
    except Exception as e:
        error(f"Error encountered while calling {method_name}: {e}")
        if log_traceback:
            error(traceback.print_exc())
        exit(1)

    return result


def load_input(input_file: str) -> Any:
    """
    Load the input from the input file.

    Parameters
    ----------
    input_file : str
        File containing the input

    Returns
    -------
    input_data : Any
        Input data for the algorithm

    Raises
    ------
    DeserializationException
        Failed to deserialize input data
    """
    with open(input_file, "rb") as fp:
        try:
            input_data = deserialization.deserialize(fp)
        except DeserializationException:
            raise DeserializationException('Could not deserialize input')
    return input_data


def _write_output(output: Any, output_file: str) -> None:
    """
    Write output to output file using JSON serialization.

    Parameters
    ----------
    output : Any
        Output of the algorithm
    output_file : str
        Path to the output file
    """
    with open(output_file, 'wb') as fp:
        serialized = serialization.serialize(output)
        fp.write(serialized)
