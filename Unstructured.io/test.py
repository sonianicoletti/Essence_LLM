# https://app.unstructured.io/keys
# pip install unstructued-client

# See https://docs.unstructured.io/api-reference/api-services/sdk for more details

import unstructured_client
from unstructured_client.models import operations, shared
import json  # Import json to save the result

# RE-DO: Scrum_Master_Guide
filetitle = 'Training_students'
fileextension = '.pdf'
filename = 'data/' + filetitle + fileextension
partitioned_filename = filetitle + '.json'

client = unstructured_client.UnstructuredClient(
    api_key_auth="MSxsxQblOSjXLv1dhqx6BmJNKw1Olv",
    server_url="https://api.unstructuredapp.io",
)

with open(filename, "rb") as f:
    data = f.read()

req = operations.PartitionRequest(
    partition_parameters=shared.PartitionParameters(
        files=shared.Files(
            content=data,
            file_name=filename,
        ),
        # --- Other partition parameters ---
        # Note: Defining 'strategy', 'chunking_strategy', and 'output_format'
        # parameters as strings is accepted, but will not pass strict type checking. It is
        # advised to use the defined enum classes as shown below.
        strategy=shared.Strategy.HI_RES,  
        languages=['eng'],
    ),
)

try:
    res = client.general.partition(request=req)    
    # Save the entire response as a JSON file
    with open(partitioned_filename, 'w') as json_file:
        json.dump(res.elements, json_file, indent=4)
    print("JSON document saved successfully!")
except Exception as e:
    print(e)
