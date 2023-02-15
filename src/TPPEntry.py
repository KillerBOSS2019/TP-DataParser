__version__ = "1.2"
PLUGIN_ID = "KillerBOSS.TPPlugin.DataParser"




# Basic plugin metadata
TP_PLUGIN_INFO = {
    "sdk": 6,
    "version": int(float(__version__) * 100),  # TP only recognizes integer version numbers
    "name": "Touch Portal DataParser",
    "id": PLUGIN_ID,
    "plugin_start_cmd": "%TP_PLUGIN_FOLDER%DataParser\\DataParser.exe",
    "configuration": {
        "colorDark": "#f54242",
        "colorLight": "#f5a442"
    },
    "doc": {
        "repository": "KillerBOSS2019:TP-DataParser",
        "Install": "1. Goto [Releases](https://github.com/KillerBOSS2019/TP-DataParser/releases) and Download latest version for your system.\n 2. After downloading the .tpp file goto open TouchPortal GUI and click on the gear icon and click `Import Plug-in`\n 3. After imported the plugin you may or may not need to restart TouchPortal but it should pop up something says do u want to allow this plugin to run. Click `Trust Always`",
        "description": "TP-DataParser allows you to parse and edit Json or HTML formatted data. If you have other type of data that aren't on the list feel free send a request to me. and I'll try my best!."
    }
}





TP_PLUGIN_SETTINGS = {}




TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": PLUGIN_ID + ".main",
        "name" : "Data Parser",
        # "imagepath" : "icon-24.png"
    }
}





TP_PLUGIN_ACTIONS = {
    "createHTTPListener": {
        "category": "main",
        "id": PLUGIN_ID + ".act.createHTTPListener",
        "name": "Create HTTP Listener",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "doc": "createHTTPListener is a action that allows to setup a base connection and use it to make actual request.",
        "format": "Create listener name$[listenerName] host url$[host] and Header$[header]",
        "data": {
            "listenerName": {
                "id": PLUGIN_ID + ".act.createHTTPListener.listenerName",
                "type": "text",
                "label": "listenerName",
                "default": ""
            },
            "host": {
                "id": PLUGIN_ID + ".act.createHTTPListener.host",
                "type": "text",
                "label": "hosturl",
                "default": ""
            },
            "header": {
                "id": PLUGIN_ID + ".act.createHTTPListener.header",
                "type": "text",
                "label": "header",
                "default": ""
            }
        }
    },
    
    
    "setupRequest": {
        "category": "main",
        "id": PLUGIN_ID + ".act.setupRequest",
        "name": "Setup endpoint calls using listener",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "format": "Use$[listeners]$[requestMethod] to endpoint$[endpoint]and optional body$[body]and request every[$intervel]seconds and save result to$[result]",
        "doc": "This will use listener that you've created using `Create HTTP Listener` action as a base. And then use this to actually send request to a endpoint with a intervel aka it will automatically update x seconds and save the result.",
        "data": {
            "listeners": {
                "id": PLUGIN_ID + ".act.setupRequest.listeners",
                "type": "choice",
                "label": "list of listeners",
                "default": "",
                "valueChoices": []
            },
            "requestMethod": {
                "id": PLUGIN_ID + ".act.setupRequest.requestMethod",
                "type": "choice",
                "label": "list of http methods",
                "default": "GET",
                "valueChoices": [
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE"
                ]
            },
            "endpoint": {
                "id": PLUGIN_ID + ".act.setupRequest.endpoint",
                "type": "text",
                "label": "endpoint",
                "default": "/",
            },
            "body": {
                "id": PLUGIN_ID + ".act.setupRequest.body",
                "type": "text",
                "label": "body data",
                "default": "",
            },
            "intervel": {
                "id": PLUGIN_ID + ".act.setupRequest.intervel",
                "type": "text",
                "label": "update interval",
                "default": "5",
            },
            "result": {
                "id": PLUGIN_ID + ".act.setupRequest.result",
                "type": "text",
                "label": "save result",
                "default": "",
            },
        }
    },
    
    
    "listenerControl": {
        "category": "main",
        "id": PLUGIN_ID + "act.listenerControl",
        "name": "Resume, Pause or Delete a listener",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "format": "$[listenerControl] $[listeners] update",
        "doc": "This will Pause, Resume, and Delete a listener. once deleted it will remove all the states that's created from this listener",
        "data": {
            "listenerControl": {
                "id": PLUGIN_ID + ".act.listenerControl.listenerControl",
                "type": "choice",
                "label": "list of listener controls",
                "default": "Delete",
                "valueChoices": [
                    "Pause",
                    "Resume",
                    "Delete"
                ]
            },
            "listeners": {
                "id": PLUGIN_ID + ".act.listenerControl.listeners",
                "type": "choice",
                "label": "list of listeners",
                "default": "",
                "valueChoices": []
            }
        }
    },
    
    
    "ParseData": {
        "category": "main",
        "id": PLUGIN_ID + ".act.ParseData",
        "name": "Parsing data",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "format": "Parse$[dataType]data$[data]to get$[dataPath]and save result to$[result]",
        "doc": "ParseData action allows you to get specific data field from Json or HTML. for example {'website host': 'blah blah'} you can get value of `website host` which is `blah blah`.",
        "data": {
            "dataType": {
                "id": PLUGIN_ID + ".act.ParseData.dataType",
                "type": "choice",
                "label": "data Type",
                "default": "Json",
                "valueChoices": [
                    "Json",
                    "Html"
                ]
            },
            "data": {
                "id": PLUGIN_ID + ".act.ParseData.data",
                "type": "text",
                "label": "data wants to parse",
                "default": ""
            },
            "dataPath": {
                "id": PLUGIN_ID + ".act.ParseData.dataPath",
                "type": "text",
                "label": "data wants to get",
                "default": ""
            },
            "result": {
                "id": PLUGIN_ID + ".act.ParseData.result",
                "type": "text",
                "label": "saving data",
                "default": ""
            }
        }
    },
    
    
    "EditJson": {
        "category": "main",
        "id": PLUGIN_ID + ".act.editJson",
        "name": "Editing json data field",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "format": "Change $[data] at path$[jsonPath] to $[newData] and save to$[result]",
        "doc": "EditJson allows you to change specific json field to a new data. for example if I have `{'name': 'someone'} I can change from `someone` to `something` as a example.",
        "data": {
            "data": {
                "id": PLUGIN_ID + ".act.editJson.data",
                "type": "text",
                "label": "data wants to parse",
                "default": ""
            },
            "newData": {
                "id": PLUGIN_ID + ".act.editJson.newData",
                "type": "text",
                "label": "new data",
                "default": ""
            },
            "jsonPath": {
                "id": PLUGIN_ID + ".act.editJson.jsonPath",
                "type": "text",
                "label": "data wants to get",
                "default": ""
            },
            "result": {
                "id": PLUGIN_ID + ".act.editJson.result",
                "type": "text",
                "label": "saving data",
                "default": ""
            }
        }
    },
    
    "WriteJson": {
        "category": "main",
        "id": PLUGIN_ID + ".act.writeJson",
        "name": "Save/Write Json File",
        "prefix": TP_PLUGIN_CATEGORIES["main"]["name"],
        "type": "communicate",
        "tryInline": True,
        "format": "Save $[data] to the file path$[filePath] with an indent of $[indent] - Ensure Ascii? $[EnsureAscii]",
        "doc": "WriteJson allows you to write json to a file using a specified indent.",
        "data": {
            "data": {
                "id": PLUGIN_ID + ".act.writeJson.data",
                "type": "text",
                "label": "data to write",
                "default": ""
            },
            "filePath": {
                "id": PLUGIN_ID + ".act.writeJson.filePath",
                "type": "file",
                "label": "File to save to",
                "default": ""
            },
            "indent": {
                "id": PLUGIN_ID + ".act.writeJson.indent",
                "type": "text",
                "label": "Json Indent amount",
                "default": ""
            },
            'EnsureAscii': {
                "id": PLUGIN_ID + ".act.writeJson.EnsureAscii",
                "type": "text",
                "label": "Ensure Ascii",
                "default": "False",
                "valueChoices": ["True", "False"]
            }
        }
    }
}





TP_PLUGIN_CONNECTORS = {}






TP_PLUGIN_STATES = {
    "text": {
        "category": "main",
        "id": PLUGIN_ID + ".state.totalListenerCreated",
        "type": "text",
        "desc": "DataParser total listener created",
        "doc": "Shows total amount of listener that you've created.",
        "default": "0"
    }
}





TP_PLUGIN_EVENTS = {}
