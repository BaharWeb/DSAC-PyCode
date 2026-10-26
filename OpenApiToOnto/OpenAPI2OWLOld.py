import json
import types
from apispec import APISpec
from apispec_fromfile import FromFilePlugin
from owlready2 import *

# Extract operation and property names 
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    if key =="schema":
        def extract2(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract2(item, arr, key)
            return arr

        values = extract2(obj, arr, key)

    else: 
        def extract(obj, arr, key):
            """Recursively search for values of key in JSON tree."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract(v, arr, key)
                    elif k == key:
                        arr.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)
            return arr

        values = extract(obj, arr, key)

    return values


# should support both version 2.0 and 3.0 
with open('./openapi/Petstore.json') as f:
    openApiJson = json.load(f)
    info = openApiJson['info']
    version = info['version']
    components = openApiJson['components']
    schemas = components['schemas']
    paths = openApiJson['paths']

    onto = get_ontology("file://specOR.owl")
    onto.load()

    with onto:
        class Operations(Thing): pass
        class DataClasses(Thing): pass


    spec = APISpec(
        title = info['title'],
        version = version,
        openapi_version="3.0.3",
        contact = info['contact']
    )
    #create the dataclasses
    for schema in schemas:
        spec.components.schema(schema, schemas[schema])
        with onto:
            dataClass = types.new_class(schema, (DataClasses,))
            if "properties" in schemas[schema]:
                properties = schemas[schema]['properties']
            elif "enum" in schemas[schema]:
                properties = schemas[schema]

            for prop in properties:
                propName = schema + "." +prop
                if "$ref" in properties[prop]:
                    objectProperty = types.new_class(propName, (ObjectProperty,))
                    objectProperty.domain = dataClass

                    dataClassTemp = types.new_class(properties[prop]['$ref'].rsplit('/',1)[1], (DataClasses,))
                    objectProperty.range = [dataClassTemp]
                else:
                    if "items" in properties[prop]:
                        items = properties[prop]['items']
                        if "$ref" in items:
                            objectProperty = types.new_class(propName, (ObjectProperty,))
                            objectProperty.domain = dataClass
                            dataClassTemp = types.new_class(properties[prop]['items']['$ref'].rsplit('/',1)[1], (DataClasses,))
                            objectProperty.range = [dataClassTemp]
                    else:
                        dataClass_prop = types.new_class(propName, (DataProperty,))
                        dataClass_prop.domain = dataClass

                propType = ""
                # if it has items then the type is array. we should look for item's type 
                if "items" in properties[prop]:
                    if "$ref" not in items:
                        items = properties[prop]['items']
                        propType = properties[prop]['items']
                   
                elif "type" in properties[prop]:
                    propType = properties[prop]['type']

                if propType == "string":
                    dataClass_prop.range = [str]
                elif propType == "integer":
                    dataClass_prop.range = [int]
                

    #creating OperationClasses              
    for path in paths:
        spec.path(path)
        for op in paths[path]:
            operationId = json_extract(paths[path][op], 'operationId')
            method = operationId[0] + ".Type" 
            with onto:
                opClass = types.new_class(operationId[0], (Operations,))
                data_prop = types.new_class(method, (DataProperty,))
                data_prop.domain = opClass
                data_prop.range = [str]

             # depends on the method. Put and Post have requestBody. delete is empty and get has parameters
            if "parameters" in paths[path][op]:
                parameters = paths[path][op]['parameters']
                for param in parameters:
                    paramName = operationId[0] + ".Param." + param['name']
                    with onto:
                        param_prop = types.new_class(paramName, (DataProperty,))
                        param_prop.domain = opClass
                        rangeName = param['schema']['type']
                        if rangeName == "array":
                            rangeName = param['schema']['items']['type']
                        if rangeName == "string":
                            param_prop.range = [str]
                        elif rangeName == "integer":
                            param_prop.range = [int]

            if "requestBody" in paths[path][op]:
                requestB = paths[path][op]['requestBody']
                paramName = operationId[0] + ".Param"
                with onto:
                    #we have schema anyway but it might have ref or properties. now we considered ref first
                    #rangeName = json_extract(paths[path][op]['requestBody']['content'], 'schema')
                    

                    if "application/json" in paths[path][op]['requestBody']['content']:
                        schema = paths[path][op]['requestBody']['content']['application/json']['schema']
                    elif "application/xml" in paths[path][op]['requestBody']['content']:
                        schema = paths[path][op]['requestBody']['content']['application/xml']['schema']
                    elif "application/x-www-form-urlencoded" in paths[path][op]['requestBody']['content']:
                        schema = paths[path][op]['requestBody']['content']['application/x-www-form-urlencoded']['schema']

                    if "$ref" in schema:
                        objectProperty = types.new_class(paramName, (ObjectProperty,))
                        objectProperty.domain = opClass

                        objClassTemp = types.new_class(schema['$ref'].rsplit('/',1)[1], (DataClasses,))
                        objectProperty.range = [objClassTemp]
                    if "properties" in schema: 
                        properties = schema['properties']
                        for paramm in properties:

                            data_prop = types.new_class(operationId[0] + ".Param." + paramm, (DataProperty,))
                            data_prop.domain = opClass
                            rangeName = properties[paramm]['type']
                            if rangeName == "array":
                                rangeName = param['schema']['items']['type']
                                
                            if rangeName == "string":
                                data_prop.range = [str]
                            elif rangeName == "integer":
                                data_prop.range = [int]

                            if paramm == "FriendlyName":
                                print(operationId[0])
                                print(properties)
            else:
                parameters = []

  
    onto.save()
    #specJson = json.dumps(spec.to_dict(), indent=2)
    


