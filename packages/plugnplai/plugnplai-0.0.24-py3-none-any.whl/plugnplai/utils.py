import json
import ast
import os

import jsonref
import requests
import yaml
import re

def make_request_get(url: str, timeout=5):
    """Make an HTTP GET request.

    Args:
        url (str): URL to make request to.
        timeout (int, optional): Timeout in seconds. Defaults to 5.

    Returns:
        requests.Response: Response from request.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong",err)
        return None
    return response

def get_plugins(filter: str = None, verified_for = None, category: str = None, provider: str = "plugnplai"):
    """Get list of plugin URLs from a provider.

    Args:
        filter (str, optional): Filter to apply. Options are "working" or "ChatGPT". Defaults to None.
        verified_for (str, optional): Filter to plugins verified for a framework. Options are "langchain" or "plugnplai". Defaults to None.
        category (str, optional): Category to filter for. Defaults to None.
        provider (str, optional): Provider to get plugins from. Options are "plugnplai" or "pluginso". Defaults to "plugnplai".

    Returns:
        list: List of plugin URLs.
    """
    if provider == "plugnplai":
        base_url = "https://www.plugnplai.com/_functions"
        # Construct the endpoint URL based on the filter and category arguments
        if filter in ["working", "ChatGPT"]:
            url = f'{base_url.strip("/")}/getUrls/{filter}'
        elif verified_for in ["langchain", "plugnplai"]:
            url = f'{base_url.strip("/")}/getUrls/{verified_for}'
        elif category is not None:
            url = f'{base_url.strip("/")}/getCategoryUrls/{category}'
        else:
            url = f'{base_url.strip("/")}/getUrls'
        # Make the HTTP GET request
        response = make_request_get(url)
        # Check if the response status code is successful (200 OK)
        if response.status_code == 200:
            # Parse the JSON response and return the result
            return response.json()
        else:
            # Handle unsuccessful responses
            return f"An error occurred: {response.status_code} {response.reason}"
    elif provider == "pluginso":
        url = "https://plugin.so/api/plugins/list"
        response = make_request_get(url)
        if response.status_code == 200:
            # Parse the JSON response and return the result
            return [f"https://{entry['domain']}" for entry in response.json()]
        else:
            # Handle unsuccessful responses
            return f"An error occurred: {response.status_code} {response.reason}"

def get_category_names(provider: str = "plugnplai"):
    """Get list of category names from a provider.

    Args:
        provider (str, optional): Provider to get category names from. Options are "plugnplai" or "pluginso". Defaults to "plugnplai".

    Returns:
        list: List of category names.
    """
    if provider == "plugnplai":
        base_url = "https://www.plugnplai.com/_functions"
        url = f'{base_url.strip("/")}/categoryNames'
        # Make the HTTP GET request
        response = make_request_get(url)
        # Check if the response status code is successful (200 OK)
        if response.status_code == 200:
            # Parse the JSON response and return the result
            return response.json()
        else:
            # Handle unsuccessful responses
            return f"An error occurred: {response.status_code} {response.reason}"
    else:
        return "Provider not supported for this operation."

# given a plugin url, get the ai-plugin.json manifest, in "/.well-known/ai-plugin.json"
def get_plugin_manifest(url: str):
    """Get plugin manifest from URL.

    Args:
        url (str): Plugin URL.

    Returns:
        dict: Plugin manifest.
    """
    urlJson = os.path.join(url, ".well-known/ai-plugin.json")
    response = make_request_get(urlJson)
    return response.json()

def _is_partial_url(url, openapi_url):
    """Check if OpenAPI URL is partial.

    Args:
        url (str): Base URL.
        openapi_url (str): OpenAPI URL.

    Returns:
        str: Full OpenAPI URL.
    """
    if openapi_url.startswith("/"):
        # remove slash in the end of url if present
        url = url.strip("/")
        openapi_url = url + openapi_url
    elif "localhost" in openapi_url:
        openapi_url = "/"+openapi_url.split("/")[-1]
        return _is_partial_url(url, openapi_url)
    return openapi_url

def get_openapi_url(url, manifest):
    """Get full OpenAPI URL from plugin URL and manifest.

    Args:
        url (str): Plugin URL.
        manifest (dict): Plugin manifest.

    Returns:
        str: Full OpenAPI URL.
    """
    openapi_url = manifest["api"]["url"]
    return _is_partial_url(url, openapi_url)

# This code uses the following source: https://github.com/hwchase17/langchain/blob/master/langchain/tools/plugin.py
def marshal_spec(txt: str) -> dict:
    """Convert YAML or JSON serialized spec to dict.

    Args:
        txt (str): YAML or JSON serialized spec.

    Returns:
        dict: Spec as a dict.
    """
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        return yaml.safe_load(txt)


def get_openapi_spec(openapi_url):
    """Get OpenAPI spec from URL.

    Args:
        openapi_url (str): OpenAPI URL.

    Returns:
        dict: OpenAPI spec.
    """
    openapi_spec_str = make_request_get(openapi_url, timeout=20).text
    openapi_spec = marshal_spec(openapi_spec_str)
    # Use jsonref to resolve references
    resolved_openapi_spec = jsonref.JsonRef.replace_refs(openapi_spec)
    return resolved_openapi_spec


def spec_from_url(url):
    """Get plugin manifest and OpenAPI spec from URL.

    Args:
        url (str): Plugin URL.

    Returns:
        dict: Plugin manifest.
        dict: OpenAPI spec.
    """
    manifest = get_plugin_manifest(url)
    openapi_url = get_openapi_url(url, manifest)
    openapi_spec = get_openapi_spec(openapi_url)
    return manifest, openapi_spec


def extract_parameters(openapi_spec, path, method):
    """Extract parameters from OpenAPI spec for a path and method.

    Args:
        openapi_spec (dict): OpenAPI spec.
        path (str): Path.
        method (str): Method.

    Returns:
        dict: Parameters.
    """
    parameters = {}

    # Extract path parameters and query parameters
    if "parameters" in openapi_spec["paths"][path][method]:
        for param in openapi_spec["paths"][path][method]["parameters"]:
            param_name = param["name"]
            param_type = param["in"]  # e.g., 'path', 'query', 'header'
            parameters[param_name] = {"type": param_type, "schema": param["schema"]}

    # Extract request body properties
    if "requestBody" in openapi_spec["paths"][path][method]:
        content = openapi_spec["paths"][path][method]["requestBody"]["content"]
        if "application/json" in content:
            json_schema = content["application/json"]["schema"]
            if "properties" in json_schema:
                for prop_name, prop_schema in json_schema["properties"].items():
                    parameters[prop_name] = {"type": "body", "schema": prop_schema}

    return parameters


def extract_all_parameters(openapi_spec):
    """Extract all parameters from OpenAPI spec.

    Args:
        openapi_spec (dict): OpenAPI spec.

    Returns:
        dict: All parameters.
    """
    all_parameters = {}

    # Mapping of long type names to short names
    type_shorteners = {
        "string": "str",
        "integer": "int",
        "boolean": "bool",
        "number": "num",
        "array": "arr",
        "object": "obj",
    }

    # Iterate over all paths in the specification
    for path, path_item in openapi_spec["paths"].items():
        # Iterate over all methods (e.g., 'get', 'post', 'put') in the path item
        for method, operation in path_item.items():
            # Skip non-method keys such as 'parameters' that can be present in the path item
            if method not in [
                "get",
                "post",
                "put",
                "delete",
                "patch",
                "options",
                "head",
                "trace",
            ]:
                continue

            # Extract the operation ID
            operation_id = operation.get("operationId", f"{method}_{path}")

            # Extract the summary, or use an empty string if it doesn't exist
            summary = operation.get("summary", "")

            # Extract parameters for the current operation
            parameters = extract_parameters(openapi_spec, path, method)

            # Shorten the types in the parameters dictionary
            for param_info in parameters.values():
                param_type = param_info["schema"].get("type")
                if param_type in type_shorteners:
                    param_info["schema"]["type"] = type_shorteners[param_type]

            # Add the extracted information to the dictionary with the operation ID as the key
            all_parameters[operation_id] = {
                "summary": summary,
                "path": path,
                "method": method,
                "parameters": parameters,
            }

    return all_parameters

def parse_llm_response(response: str) -> dict:
    """Parse LLM response to extract API call information.

    Args:
        response (str): LLM response.

    Returns:
        dict: API call information.
    """
    pattern = r'<API>\s*(.*?)\s*\((.*?)\)\s*</API>'
    match = re.search(pattern, response, re.DOTALL)

    if not match:
        return {}

    api = match.group(1)
    params_str = match.group(2)

    try:
        # Try parsing as JSON first
        params = json.loads(params_str)
    except json.JSONDecodeError:
        try:
            # If that fails, try parsing as a Python literal expression
            params = ast.literal_eval(params_str)
        except (ValueError, SyntaxError):
            params = {}

    return {
        'plugin_name': api.split('.')[0],
        'operation_id': api.split('.')[1],
        'parameters': params
    }
