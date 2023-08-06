Great to see you here 🫶 We are extremely open to contributions!

Do you have a connector you want to see included in Lemon AI or do you want to contribute in any other way? That's amazing 🥳 Just reach out or directly create a [Pull Request](https://docs.github.com/en/get-started/quickstart/contributing-to-projects).

Please make sure to use the [Pull Request Template](https://github.com/felixbrock/lemonai-py-client/blob/main/.github/PULL_REQUEST_TEMPLATE.md).

**<u>Creating a new connector</u>**:

You wil be working in the [Lemon AI Server](https://github.com/felixbrock/lemonai-server).

1. Choose a connector. I will use Discord as an example,
2. Add parameter descriptions for each operation to a file in ```src/services/``` e.g. ```discord-param-descriptions.ts```.
3. In ```src/domain/value-types/tool.ts```:
    - Add the ID of all your connector's operations to the ```toolTypes``` variable e.g. ```'discord-message-send'```
    - Add the authentication type of your connector and export it as a type e.g.```export type DiscordAuthType = 'accessToken'``` The value of this should be ```apiKey | accessToken | none```
    - In the variable ```const toolBases: ToolBase[]```, add all your operations in the same format to the existent elements, like the following example. Your name should give the connector name and the operation description:
        ```typescript
        {
            name: 'Discord: Send message in channel',
            id: 'discord-message-send',
            params: {
            ...discordParamDescriptions.messageSendParamDescriptions
            },
            authorizationType: 'accessToken'
        }
        ```
        The ```discordParamDescriptions.messageSendParamDescriptions``` would have been imported from your parameter descriptions file
4. In ```src/infra/api/controllers/resolve-controller-of-tool.ts```:
    
    - Add a ```RunToolController``` for your connector. Follow the format of the existing tools, you will implement the types later
    - Create a buildAuth function for your connector e.g. ```buildNotionAuth``` which matches the format of the existent tools
    - Create a getter for your executeOperationController for your connector e.g. ```getExecuteNotionOperationController``` which matches the format of the existent tools
    - In the ```switch-case``` statement, create a case for each operation of your connector which builds a request object for your connector and returns its execution controller e.g.
        ```typescript
        case 'discord-message-send': {
            const buildReq = (httpReq: Request): ExecuteDiscordOperationReq => {
                return {
                    params: {
                        toolType,
                        messageSendParamTypes: httpReq.body,
                    },
                };
            };

            return getExecuteDiscordOperationController(buildReq);
        }
        ```
5. Implement your connectors use case in a separate file in ```src/domain/use-case/```. Use the existent files as a template for your implementation:
    
    - Create an interface containing the parameter types for the connector operations. You will need to look at your connector API for this and what parameters are needed (or are optional) for 
    - Create an interface for your request type, result type, and authentication type. These will be the same as the other connectors. Remember to import these into ```resolve-controller-of-tool.ts```
    - Create and implement a class to execute the operations of your connector. The pattern will be the same as the other connectors. 
    - Within the execution class, create an execute function that, based on the ```toolType```, will make the correct call to your connector API class and return the response. Use the other connector execute functions as a template
6. Implement the API class for your connector in ```src/infra/external/```. 
    - This class should extend ```BaseExternalApi``` and therefore have two functions: ```apiRequest``` and ```apiRequestAllItems``` (for bulk API requests e.g. multiple pages of results)
    - View your connector API documentation to check the required headers, URLs and parameters
    - These functions should be called in your execute function from your connectors use case file where necessary
7. In ```src/ioc-register.ts```, register your connector's execute class and API class as shown with the other examples