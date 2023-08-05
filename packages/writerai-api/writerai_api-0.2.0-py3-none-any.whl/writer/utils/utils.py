import base64
import json
import re
from dataclasses import Field, dataclass, fields, is_dataclass, make_dataclass
from datetime import date, datetime
from email.message import Message
from enum import Enum
from typing import Callable, Optional, Tuple, Union, get_args, get_origin
from xmlrpc.client import boolean

import dateutil.parser
import requests
from dataclasses_json import DataClassJsonMixin


class SecurityClient:
    client: requests.Session
    query_params: dict[str, str] = {}

    def __init__(self, client: requests.Session):
        self.client = client

    def request(self, method, url, **kwargs):
        params = kwargs.get('params', {})
        kwargs["params"] = self.query_params | params

        return self.client.request(method, url, **kwargs)


def configure_security_client(client: requests.Session, security: dataclass):
    client = SecurityClient(client)

    sec_fields: Tuple[Field, ...] = fields(security)
    for sec_field in sec_fields:
        value = getattr(security, sec_field.name)
        if value is None:
            continue

        metadata = sec_field.metadata.get('security')
        if metadata is None:
            continue
        if metadata.get('option'):
            _parse_security_option(client, value)
            return client
        if metadata.get('scheme'):
            # Special case for basic auth which could be a flattened struct
            if metadata.get("sub_type") == "basic" and not is_dataclass(value):
                _parse_security_scheme(client, metadata, security)
            else:
                _parse_security_scheme(client, metadata, value)

    return client


def _parse_security_option(client: SecurityClient, option: dataclass):
    opt_fields: Tuple[Field, ...] = fields(option)
    for opt_field in opt_fields:
        metadata = opt_field.metadata.get('security')
        if metadata is None or metadata.get('scheme') is None:
            continue
        _parse_security_scheme(
            client, metadata, getattr(option, opt_field.name))


def _parse_security_scheme(client: SecurityClient, scheme_metadata: dict, scheme: any):
    scheme_type = scheme_metadata.get('type')
    sub_type = scheme_metadata.get('sub_type')

    if is_dataclass(scheme):
        if scheme_type == 'http' and sub_type == 'basic':
            _parse_basic_auth_scheme(client, scheme)
            return

        scheme_fields: Tuple[Field, ...] = fields(scheme)
        for scheme_field in scheme_fields:
            metadata = scheme_field.metadata.get('security')
            if metadata is None or metadata.get('field_name') is None:
                continue

            value = getattr(scheme, scheme_field.name)

            _parse_security_scheme_value(
                client, scheme_metadata, metadata, value)
    else:
        _parse_security_scheme_value(
            client, scheme_metadata, scheme_metadata, scheme)


def _parse_security_scheme_value(client: SecurityClient, scheme_metadata: dict, security_metadata: dict, value: any):
    scheme_type = scheme_metadata.get('type')
    sub_type = scheme_metadata.get('sub_type')

    header_name = security_metadata.get('field_name')

    if scheme_type == "apiKey":
        if sub_type == 'header':
            client.client.headers[header_name] = value
        elif sub_type == 'query':
            client.query_params[header_name] = value
        elif sub_type == 'cookie':
            client.client.cookies[header_name] = value
        else:
            raise Exception('not supported')
    elif scheme_type == "openIdConnect":
        client.client.headers[header_name] = value
    elif scheme_type == 'oauth2':
        client.client.headers[header_name] = value
    elif scheme_type == 'http':
        if sub_type == 'bearer':
            client.client.headers[header_name] = value
        else:
            raise Exception('not supported')
    else:
        raise Exception('not supported')


def _parse_basic_auth_scheme(client: SecurityClient, scheme: dataclass):
    username = ""
    password = ""

    scheme_fields: Tuple[Field, ...] = fields(scheme)
    for scheme_field in scheme_fields:
        metadata = scheme_field.metadata.get('security')
        if metadata is None or metadata.get('field_name') is None:
            continue

        field_name = metadata.get('field_name')
        value = getattr(scheme, scheme_field.name)

        if field_name == 'username':
            username = value
        if field_name == 'password':
            password = value

    data = f'{username}:{password}'.encode()
    client.client.headers['Authorization'] = f'Basic {base64.b64encode(data).decode()}'


def generate_url(server_url: str, path: str, path_params: dataclass) -> str:
    path_param_fields: Tuple[Field, ...] = fields(path_params)
    for field in path_param_fields:
        param_metadata = field.metadata.get('path_param')
        if param_metadata is None:
            continue
        if param_metadata.get('style', 'simple') == 'simple':
            param = getattr(path_params, field.name)
            if param is None:
                continue

            if isinstance(param, list):
                pp_vals: list[str] = []
                for pp_val in param:
                    if pp_val is None:
                        continue
                    pp_vals.append(_val_to_string(pp_val))
                path = path.replace(
                    '{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
            elif isinstance(param, dict):
                pp_vals: list[str] = []
                for pp_key in param:
                    if param[pp_key] is None:
                        continue
                    if param_metadata.get('explode'):
                        pp_vals.append(
                            f"{pp_key}={_val_to_string(param[pp_key])}")
                    else:
                        pp_vals.append(
                            f"{pp_key},{_val_to_string(param[pp_key])}")
                path = path.replace(
                    '{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
            elif not isinstance(param, (str, int, float, complex, bool)):
                pp_vals: list[str] = []
                param_fields: Tuple[Field, ...] = fields(param)
                for param_field in param_fields:
                    param_value_metadata = param_field.metadata.get(
                        'path_param')
                    if not param_value_metadata:
                        continue

                    parm_name = param_value_metadata.get(
                        'field_name', field.name)

                    param_field_val = getattr(param, param_field.name)
                    if param_field_val is None:
                        continue
                    if param_metadata.get('explode'):
                        pp_vals.append(
                            f"{parm_name}={_val_to_string(param_field_val)}")
                    else:
                        pp_vals.append(
                            f"{parm_name},{_val_to_string(param_field_val)}")
                path = path.replace(
                    '{' + param_metadata.get('field_name', field.name) + '}', ",".join(pp_vals), 1)
            else:
                path = path.replace(
                    '{' + param_metadata.get('field_name', field.name) + '}', _val_to_string(param), 1)

    return server_url.removesuffix("/") + path


def is_optional(field):
    return get_origin(field) is Union and type(None) in get_args(field)


def template_url(url_with_params: str, params: dict[str, str]) -> str:
    for key, value in params.items():
        url_with_params = url_with_params.replace(
            '{' + key + '}', value)

    return url_with_params


def get_query_params(query_params: dataclass) -> dict[str, list[str]]:
    if query_params is None:
        return {}

    params: dict[str, list[str]] = {}

    param_fields: Tuple[Field, ...] = fields(query_params)
    for field in param_fields:
        metadata = field.metadata.get('query_param')
        if not metadata:
            continue

        param_name = field.name
        f_name = metadata.get("field_name")
        serialization = metadata.get('serialization', '')
        if serialization != '':
            params = params | _get_serialized_query_params(
                metadata, f_name, getattr(query_params, param_name))
        else:
            style = metadata.get('style', 'form')
            if style == 'deepObject':
                params = params | _get_deep_object_query_params(
                    metadata, f_name, getattr(query_params, param_name))
            elif style == 'form':
                params = params | _get_form_query_params(
                    metadata, f_name, getattr(query_params, param_name))
            else:
                raise Exception('not yet implemented')
    return params


def get_headers(headers_params: dataclass) -> dict[str, str]:
    if headers_params is None:
        return {}

    headers: dict[str, str] = {}

    param_fields: Tuple[Field, ...] = fields(headers_params)
    for field in param_fields:
        metadata = field.metadata.get('header')
        if not metadata:
            continue

        value = _serialize_header(metadata.get(
            'explode', False), getattr(headers_params, field.name))

        if value != '':
            headers[metadata.get('field_name', field.name)] = value

    return headers


def _get_serialized_query_params(metadata: dict, field_name: str, obj: any) -> dict[str, list[str]]:
    params: dict[str, list[str]] = {}

    serialization = metadata.get('serialization', '')
    if serialization == 'json':
        params[metadata.get("field_name", field_name)] = marshal_json(obj)

    return params


def _get_deep_object_query_params(metadata: dict, field_name: str, obj: any) -> dict[str, list[str]]:
    params: dict[str, list[str]] = {}

    if obj is None:
        return params

    if is_dataclass(obj):
        obj_fields: Tuple[Field, ...] = fields(obj)
        for obj_field in obj_fields:
            obj_param_metadata = obj_field.metadata.get('query_param')
            if not obj_param_metadata:
                continue

            obj_val = getattr(obj, obj_field.name)
            if obj_val is None:
                continue

            if isinstance(obj_val, list):
                for val in obj_val:
                    if val is None:
                        continue

                    if params.get(f'{metadata.get("field_name", field_name)}[{obj_param_metadata.get("field_name", obj_field.name)}]') is None:
                        params[f'{metadata.get("field_name", field_name)}[{obj_param_metadata.get("field_name", obj_field.name)}]'] = [
                        ]

                    params[
                        f'{metadata.get("field_name", field_name)}[{obj_param_metadata.get("field_name", obj_field.name)}]'].append(_val_to_string(val))
            else:
                params[
                    f'{metadata.get("field_name", field_name)}[{obj_param_metadata.get("field_name", obj_field.name)}]'] = [
                    _val_to_string(obj_val)]
    elif isinstance(obj, dict):
        for key, value in obj.items():
            if value is None:
                continue

            if isinstance(value, list):
                for val in value:
                    if val is None:
                        continue

                    if params.get(f'{metadata.get("field_name", field_name)}[{key}]') is None:
                        params[f'{metadata.get("field_name", field_name)}[{key}]'] = [
                        ]

                    params[
                        f'{metadata.get("field_name", field_name)}[{key}]'].append(_val_to_string(val))
            else:
                params[f'{metadata.get("field_name", field_name)}[{key}]'] = [
                    _val_to_string(value)]
    return params


def _get_query_param_field_name(obj_field: Field) -> str:
    obj_param_metadata = obj_field.metadata.get('query_param')

    if not obj_param_metadata:
        return ""

    return obj_param_metadata.get("field_name", obj_field.name)


def _get_form_query_params(metadata: dict, field_name: str, obj: any) -> dict[str, list[str]]:
    return _populate_form(field_name, metadata.get("explode", True), obj, _get_query_param_field_name)


def serialize_request_body(request: dataclass) -> Tuple[str, any, any]:
    if request is None:
        return None, None, None, None

    request_val = getattr(request, "request")
    if request_val is None:
        raise Exception("request body not found")

    request_fields: Tuple[Field, ...] = fields(request)
    request_metadata = None

    for field in request_fields:
        if field.name == "request":
            request_metadata = field.metadata.get('request')
            break

    if request_metadata is not None:
        # single request
        return serialize_content_type('request', request_metadata.get('media_type', 'application/octet-stream'), request_val)

    request_fields: Tuple[Field, ...] = fields(request_val)
    for field in request_fields:
        req = getattr(request_val, field.name)
        if req is None:
            continue

        request_metadata = field.metadata.get('request')
        if request_metadata is None:
            raise Exception(
                f'missing request tag on request body field {field.name}')

        return serialize_content_type(field.name, request_metadata.get('media_type', 'application/octet-stream'), req)


def serialize_content_type(field_name: str, media_type: str, request: dataclass) -> Tuple[str, any, list[list[any]]]:
    if re.match(r'(application|text)\/.*?\+*json.*', media_type) is not None:
        return media_type, marshal_json(request), None
    if re.match(r'multipart\/.*', media_type) is not None:
        return serialize_multipart_form(media_type, request)
    if re.match(r'application\/x-www-form-urlencoded.*', media_type) is not None:
        return media_type, serialize_form_data(field_name, request), None
    if isinstance(request, (bytes, bytearray)):
        return media_type, request, None
    if isinstance(request, str):
        return media_type, request, None

    raise Exception(
        f"invalid request body type {type(request)} for mediaType {media_type}")


def serialize_multipart_form(media_type: str, request: dataclass) -> Tuple[str, any, list[list[any]]]:
    form: list[list[any]] = []
    request_fields = fields(request)

    for field in request_fields:
        val = getattr(request, field.name)
        if val is None:
            continue

        field_metadata = field.metadata.get('multipart_form')
        if not field_metadata:
            continue

        if field_metadata.get("file") is True:
            file_fields = fields(val)

            file_name = ""
            field_name = ""
            content = bytes()

            for file_field in file_fields:
                file_metadata = file_field.metadata.get('multipart_form')
                if file_metadata is None:
                    continue

                if file_metadata.get("content") is True:
                    content = getattr(val, file_field.name)
                else:
                    field_name = file_metadata.get(
                        "field_name", file_field.name)
                    file_name = getattr(val, file_field.name)
            if field_name == "" or file_name == "" or content == bytes():
                raise Exception('invalid multipart/form-data file')

            form.append([field_name, [file_name, content]])
        elif field_metadata.get("json") is True:
            to_append = [field_metadata.get("field_name", field.name), [
                None, marshal_json(val), "application/json"]]
            form.append(to_append)
        else:
            field_name = field_metadata.get(
                "field_name", field.name)
            if isinstance(val, list):
                for value in val:
                    if value is None:
                        continue
                    form.append(
                        [field_name + "[]", [None, _val_to_string(value)]])
            else:
                form.append([field_name, [None, _val_to_string(val)]])
    return media_type, None, form


def serialize_dict(original: dict, explode: bool, field_name, existing: Optional[dict[str, list[str]]]) -> dict[
        str, list[str]]:
    if existing is None:
        existing = []

    if explode is True:
        for key, val in original.items():
            if key not in existing:
                existing[key] = []
            existing[key].append(val)
    else:
        temp = []
        for key, val in original.items():
            temp.append(str(key))
            temp.append(str(val))
        if field_name not in existing:
            existing[field_name] = []
        existing[field_name].append(",".join(temp))
    return existing


def serialize_form_data(field_name: str, data: dataclass) -> dict[str, any]:
    form: dict[str, list[str]] = {}

    if is_dataclass(data):
        for field in fields(data):
            val = getattr(data, field.name)
            if val is None:
                continue

            metadata = field.metadata.get('form')
            if metadata is None:
                continue

            field_name = metadata.get('field_name', field.name)

            if metadata.get('json'):
                form[field_name] = [marshal_json(val)]
            else:
                if metadata.get('style', 'form') == 'form':
                    form = form | _populate_form(
                        field_name, metadata.get('explode', True), val, _get_form_field_name)
                else:
                    raise Exception(
                        f'Invalid form style for field {field.name}')
    elif isinstance(data, dict):
        for key, value in data.items():
            form[key] = [_val_to_string(value)]
    else:
        raise Exception(f'Invalid request body type for field {field_name}')

    return form


def _get_form_field_name(obj_field: Field) -> str:
    obj_param_metadata = obj_field.metadata.get('form')

    if not obj_param_metadata:
        return ""

    return obj_param_metadata.get("field_name", obj_field.name)


def _populate_form(field_name: str, explode: boolean, obj: any, get_field_name_func: Callable) -> dict[str, list[str]]:
    params: dict[str, list[str]] = {}

    if obj is None:
        return params

    if is_dataclass(obj):
        items = []

        obj_fields: Tuple[Field, ...] = fields(obj)
        for obj_field in obj_fields:
            obj_field_name = get_field_name_func(obj_field)
            if obj_field_name == '':
                continue

            val = getattr(obj, obj_field.name)
            if val is None:
                continue

            if explode:
                params[obj_field_name] = [_val_to_string(val)]
            else:
                items.append(
                    f'{obj_field_name},{_val_to_string(val)}')

        if len(items) > 0:
            params[field_name] = [','.join(items)]
    elif isinstance(obj, dict):
        items = []
        for key, value in obj.items():
            if value is None:
                continue

            if explode:
                params[key] = _val_to_string(value)
            else:
                items.append(f'{key},{_val_to_string(value)}')

        if len(items) > 0:
            params[field_name] = [','.join(items)]
    elif isinstance(obj, list):
        items = []

        for value in obj:
            if value is None:
                continue

            if explode:
                if not field_name in params:
                    params[field_name] = []
                params[field_name].append(_val_to_string(value))
            else:
                items.append(_val_to_string(value))

        if len(items) > 0:
            params[field_name] = [','.join([str(item) for item in items])]
    else:
        params[field_name] = [_val_to_string(obj)]

    return params


def _serialize_header(explode: bool, obj: any) -> str:
    if obj is None:
        return ''

    if is_dataclass(obj):
        items = []
        obj_fields: Tuple[Field, ...] = fields(obj)
        for obj_field in obj_fields:
            obj_param_metadata = obj_field.metadata.get('header')

            if not obj_param_metadata:
                continue

            obj_field_name = obj_param_metadata.get(
                'field_name', obj_field.name)
            if obj_field_name == '':
                continue

            val = getattr(obj, obj_field.name)
            if val is None:
                continue

            if explode:
                items.append(
                    f'{obj_field_name}={_val_to_string(val)}')
            else:
                items.append(obj_field_name)
                items.append(_val_to_string(val))

        if len(items) > 0:
            return ','.join(items)
    elif isinstance(obj, dict):
        items = []

        for key, value in obj.items():
            if value is None:
                continue

            if explode:
                items.append(f'{key}={_val_to_string(value)}')
            else:
                items.append(key)
                items.append(_val_to_string(value))

        if len(items) > 0:
            return ','.join([str(item) for item in items])
    elif isinstance(obj, list):
        items = []

        for value in obj:
            if value is None:
                continue

            items.append(_val_to_string(value))

        if len(items) > 0:
            return ','.join(items)
    else:
        return f'{_val_to_string(obj)}'

    return ''


def unmarshal_json(data, typ):
    unmarhsal = make_dataclass('Unmarhsal', [('res', typ)],
                               bases=(DataClassJsonMixin,))
    json_dict = json.loads(data)
    out = unmarhsal.from_dict({"res": json_dict})
    return out.res


def marshal_json(val):
    marshal = make_dataclass('Marshal', [('res', type(val))],
                             bases=(DataClassJsonMixin,))
    marshaller = marshal(res=val)
    json_dict = marshaller.to_dict()
    return json.dumps(json_dict["res"])


def match_content_type(content_type: str, pattern: str) -> boolean:
    if pattern in (content_type, "*", "*/*"):
        return True

    msg = Message()
    msg['content-type'] = content_type
    media_type = msg.get_content_type()

    if media_type == pattern:
        return True

    parts = media_type.split("/")
    if len(parts) == 2:
        if pattern in (f'{parts[0]}/*', f'*/{parts[1]}'):
            return True

    return False


def datetimeisoformat(optional: bool):
    def isoformatoptional(val):
        if optional and val is None:
            return None
        return _val_to_string(val)

    return isoformatoptional


def dateisoformat(optional: bool):
    def isoformatoptional(val):
        if optional and val is None:
            return None
        return date.isoformat(val)

    return isoformatoptional


def datefromisoformat(date_str: str):
    return dateutil.parser.parse(date_str).date()


def get_field_name(name):
    def override(_, _field_name=name):
        return _field_name

    return override


def _val_to_string(val):
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, datetime):
        return val.isoformat().replace('+00:00', 'Z')
    if isinstance(val, Enum):
        return val.value

    return str(val)
