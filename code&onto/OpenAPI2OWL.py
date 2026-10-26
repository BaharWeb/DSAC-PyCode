import json
from owlready2 import *
import time

start_time = time.perf_counter()

# Extract operation and property names
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    if key == "schema":
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
#addresses = ["./api/weather information.json","./api/IP geolocation API.json"]

ontoName = ""

#for address in addresses:
with open('./Interzoid license.json') as f:
    openApiJson = json.load(f)
    info = openApiJson['info']
    version = info['version']
    if "components" in openApiJson:
        components = openApiJson['components']
        if "schemas" in components:
            schemas = components['schemas']
        else:
            schemas = []
    else:
        components = []
        schemas = []

    paths = openApiJson['paths']
    onto = get_ontology("file://ReferenceOntologyMain.owl")
    onto.load()

    # Create instances of reference Ontology for each API
    ontoName = info["title"]
    ontoName = ontoName.replace(' ','')
    api = onto.API(ontoName)

    if "servers" in openApiJson:
        servers = openApiJson['servers']
        server = onto.Servers(servers[0]['url'])
        api.hasServer.append(server)
    else:
        servers = []

    # Generating the Schemas
    for schema in schemas:
        schemaName = schema
        schemaInstance = onto.Schema(schemaName)
        if "properties" in schemas[schemaName]:
            properties = schemas[schemaName]["properties"]
            for property in properties:
                if "type" in properties[property]:
                    propertyInstance = onto.Property(schemaName + "." + property)
                    if properties[property]["type"] == "array" and "$ref" not in properties[property]["items"]:
                        if "type" in properties[property]['items']:
                            propertyType = properties[property]['items']['type']
                            propertyInstance.propertyType.append(propertyType)
                            propertyInstance.propertyName.append(property)
                        schemaInstance.hasProperties.append(propertyInstance)
                    elif properties[property]["type"] == "array" and "$ref" in properties[property]["items"]:
                        refname = properties[property]["items"]["$ref"].rsplit('/', 1)[1]
                        schemaInstanceNew = onto.Schema(refname)
                        schemaInstance.referesToSchema.append(schemaInstanceNew)
                    else:
                        propertyType = properties[property]['type']
                        propertyInstance.propertyType.append(propertyType)
                        propertyInstance.propertyName.append(property)
                    schemaInstance.hasProperties.append(propertyInstance)
                elif "$ref" in properties[property]:
                    refName = properties[property]['$ref'].rsplit('/', 1)[1]
                    schemaInstance2 = onto.Schema(refName)
                    schemaInstance.referesToSchema.append(schemaInstance2)
                elif "allOf" in properties[property]:
                    allOf = properties[property]['allOf']
                    refNameAllOf = allOf[0]['$ref'].rsplit('/', 1)[1]
                    schemaInstanceallOf = onto.Schema(refNameAllOf)
                    schemaInstance.referesToSchema.append(schemaInstanceallOf)
        elif "type" in schemas[schemaName]:
            schemaInstance.schemaType.append(schemas[schemaName]["type"])

    # Adding the operations(paths)
    for path in paths:
        for op in paths[path]:
            # We look into operations. if operationIp not exists then path+method
            if op == "put" or op == "get" or op == "delete" or op == "post":
                operation = paths[path][op]
                operationId = json_extract(operation, 'operationId')
                if bool(operationId):
                    operationId = operationId[0]
                else:
                    operationId = path + "." + op
                method = op
                opInstance = onto.Operations(operationId)
                opInstance.hasPath.append(path)
                opInstance.hasMethod.append(op)
                if "description" in operation:
                    opInstance.hasDescription.append(operation["description"])
                else:
                    opInstance.hasDescription.append("")
                api.hasOperations.append(opInstance)

                # Does the operation has parameters or requestBody(both are considered as the input) TODO add schema to it
                if "parameters" in operation:
                    parameters = operation['parameters']
                    for param in parameters:
                        parameterSchema = param['schema']
                        parameterInstance = onto.Parameter(operationId + "." + param["name"])
                        parameterInstance.parameterType.append(parameterSchema['type'])
                        parameterInstance.parameterName.append(param["name"])
                        if "description" in param:
                            parameterInstance.parameterDescription.append(param["description"])
                        parameterInstance.parameterLocation.append(param["in"])
                        opInstance.hasParameter.append(parameterInstance)

                if "requestBody" in operation:
                    requestBody = operation["requestBody"]
                    rqBodyContent = requestBody["content"]
                    requestBodyInstance = onto.RequestBody(operationId + ".requestBody")
                    opInstance.hasRequestBody.append(requestBodyInstance)

                    if "application/json" in rqBodyContent:
                        RBcontentInstance = onto.RBContent(operationId + ".requestBody.application/json")
                        schema = rqBodyContent['application/json']['schema']
                    elif "application/xml" in rqBodyContent:
                        RBcontentInstance = onto.RBContent(operationId + ".requestBody.application/xml")
                        schema = rqBodyContent['application/xml']['schema']
                    elif "application/x-www-form-urlencoded" in rqBodyContent:
                        RBcontentInstance = onto.RBContent(operationId + ".requestBody.application/x-www-form-urlencode")
                        schema = rqBodyContent['application/x-www-form-urlencoded']['schema']
                    elif "application/octet-stream" in rqBodyContent:
                        RBcontentInstance = onto.RBContent(operationId + ".requestBody.application/octet-streame")
                        schema = rqBodyContent['application/octet-stream']['schema']

                    # The request body schema is refered to a defined schema
                    if "$ref" in schema:
                        schemaName = schema['$ref'].rsplit('/', 1)[1]
                        schemaInstance = onto.Schema(schemaName)
                        RBcontentInstance.hasRBSchema.append(schemaInstance)
                    requestBodyInstance.hasRequestBodyContent.append(RBcontentInstance)

                if "responses" in operation:
                    responses = operation["responses"]
                    for response in responses:
                        if response == "200" or response == "default":
                            outputName = operationId + ".output." + response
                            outputInstance = onto.Output(outputName)
                            opInstance.hasOutput.append(outputInstance)
                            if "content" in responses[response]:
                                outputContent = responses[response]["content"]

                                if "application/json" in outputContent:
                                    outputcontentInstance = onto.OContent(operationId + ".output.application/json")
                                    schema = outputContent['application/json']['schema']
                                elif "application/xml" in outputContent:
                                    outputcontentInstance = onto.OContent(operationId + ".output.application/xml")
                                    schema = outputContent['application/xml']['schema']
                                elif "application/x-www-form-urlencoded" in outputContent:
                                    outputcontentInstance = onto.OContent(
                                        operationId + ".output.application/x-www-form-urlencode")
                                    schema = outputContent['application/x-www-form-urlencoded']['schema']
                                elif "application/octet-stream" in outputContent:
                                    outputcontentInstance = onto.OContent(
                                        operationId + ".output.application/octet-streame")
                                    schema = outputContent['application/octet-stream']['schema']
                                elif "application/pdf" in outputContent:
                                    outputcontentInstance = onto.OContent(
                                        operationId + ".output.application/pdf")
                                    if "schema" in outputContent["application/pdf"]:
                                        schema = outputContent['application/pdf']['schema']
                                    else:
                                        outputschemaInstance = onto.Schema("pdf")
                                        outputcontentInstance.hasOoutputSchema.append(outputschemaInstance)

                                if "$ref" in schema:
                                    outputSchemaName = schema['$ref'].rsplit('/', 1)[1]
                                    outputschemaInstance = onto.Schema(outputSchemaName)
                                    outputcontentInstance.hasOoutputSchema.append(outputschemaInstance)
                                elif "properties" in schema:
                                    outputSchemaName = outputName + ".schema"
                                    outputschemaInstance = onto.Schema(outputSchemaName)
                                    outputcontentInstance.hasOoutputSchema.append(outputschemaInstance)
                                    properties = schema["properties"]
                                    for property in properties:
                                        if "type" in properties[property]:
                                            propertyInstance = onto.Property(outputSchemaName + "." + property)
                                            if properties[property]["type"] == "array" and "$ref" not in properties[property]["items"]:
                                                if "type" in properties[property]['items']:
                                                    propertyType = properties[property]['items']['type']
                                                    propertyInstance.propertyType.append(propertyType)
                                                    propertyInstance.propertyName.append(property)
                                                outputschemaInstance.hasProperties.append(propertyInstance)
                                            elif properties[property]["type"] == "array" and "$ref" in properties[property]["items"]:
                                                refname = properties[property]["items"]["$ref"].rsplit('/', 1)[1]
                                                outputschemaInstanceNew = onto.Schema(refname)
                                                outputschemaInstance.referesToSchema.append(outputschemaInstanceNew)
                                            else:
                                                propertyType = properties[property]['type']
                                                propertyInstance.propertyType.append(propertyType)
                                                propertyInstance.propertyName.append(property)
                                            outputschemaInstance.hasProperties.append(propertyInstance)
                                        elif "$ref" in properties[property]:
                                            refName = properties[property]['$ref'].rsplit('/', 1)[1]
                                            outputSchemaInstance2 = onto.Schema(refName)
                                            outputschemaInstance.referesToSchema.append(outputSchemaInstance2)

                                outputInstance.hasOutputContent.append(outputcontentInstance)


#onto.save(file=ontoName+".owl")
#print(onto.server)
end_time = time.perf_counter()
execution_time_ms = (end_time - start_time) * 1000  # convert to milliseconds
print(f"Execution Time: {execution_time_ms:.2f} ms")