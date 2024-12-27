# AI-chat-interface
## Project Overview
In this application we use gpt-api to work with dataframes using only natural language.

## Main Components
The project is divided into 3 parts, the Main file contains the logic of interaction with command line arguments, test data and a test prompt (in case they were not provided) and data output. 
The gpt_communication file contains the logic of interaction with the gpt api, we write down the json scheme that we want to receive and configure the developer's prompt in order to make it clear what answer we want to receive and we pass the user prompt
In transformations file we perform all transformations using the resulting json, which describes what transformations we want to apply to our dataframe.
## Tips for use
Launching is possible both from the console and from a file. In case of using the console, there are 2 options for use, either specify only the script name or add --datafile --userprompt parameters (You cannot specify only one parameter, or both, or neither)
For convenience, a dataset that was used during testing was added.