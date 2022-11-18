
"""
Touch Portal Plugin Example
"""
from TPPEntry import PLUGIN_ID, TP_PLUGIN_SETTINGS, TP_PLUGIN_ACTIONS, TP_PLUGIN_INFO, __version__
from TouchPortalAPI.logger import Logger
from argparse import ArgumentParser
import TouchPortalAPI as TP
from threading import Thread
from functools import reduce
from pyquery import PyQuery
from time import sleep
import requests
import json
import sys
import re



try:
    TPClient = TP.Client(
        pluginId = PLUGIN_ID,  # required ID of this plugin
        sleepPeriod = 0.05,    # allow more time than default for other processes
        autoClose = True,      # automatically disconnect when TP sends "closePlugin" message
        checkPluginId = True,  # validate destination of messages sent to this plugin
        maxWorkers = 4,        # run up to 4 event handler threads
        updateStatesOnBroadcast = False,  # do not spam TP with state updates on every page change
    )
except Exception as e:
    sys.exit(f"Could not create TP Client, exiting. Error was:\n{repr(e)}")



g_log = Logger(name = PLUGIN_ID)


def handleSettings(settings, on_connect=False):
    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }
    # now we can just get settings, and their values, by name
    if (value := settings.get(TP_PLUGIN_SETTINGS['example']['name'])) is not None:
        # this example doesn't do anything useful with the setting, just saves it
        TP_PLUGIN_SETTINGS['example']['value'] = value




#--- On Startup ---#
@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)
        
    Thread(target=stateUpdate).start()




#--- Settings handler ---#
@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if (settings := data.get('values')):
        handleSettings(settings, False)




#--- Action handler ---#
@TPClient.on(TP.TYPES.onAction)
def onAction(data):
    global requestListener
    g_log.debug(f"Action: {data}")
    
    
    if not (action_data := data.get('data')) or not (aid := data.get('actionId')):
        return
    
    if aid == TP_PLUGIN_ACTIONS['createHTTPListener']['id']:
        if data['data'][0]['value'] != "" and data['data'][1]['value'] != "":
            if not findListener(data['data'][0]['value']): # check if is already created
                requestListener.append(
                       {   
                        data['data'][0]['value']: {
                            "host": data['data'][1]['value'],
                            "header": data['data'][2]['value'],
                            "thread":  Thread,
                            "status": "standby"
                        }
                    }
                )
        
    if aid == TP_PLUGIN_ACTIONS['setupRequest']['id']:
        if data['data'][0]['value'] != "" and (listener := findListener(data['data'][0]['value'])):
            listener[data['data'][0]['value']]['thread'] = Thread(target=makeRequests, args=(data['data'][1]['value'], data['data'][2]['value'],
            data['data'][3]['value'], data['data'][4]['value'], data['data'][5]['value'], listener))
            listener[data['data'][0]['value']]['thread'].start()
        
        
        
    if aid == TP_PLUGIN_ACTIONS['ParseData']['id']:
        g_log.debug(f"Parse Data Action: {data}")
        
        if data['data'][0]['value'] == "Json":
            parsedData = jsonPathfinder(data['data'][2]['value'], data['data'][1]['value'])
            
        elif data['data'][0]['value'] == "Html":
            parsedData = HtmlParser(data['data'][2]['value'], data['data'][1]['value'])
            
        TPClient.createState(PLUGIN_ID + f".userState.{data['data'][3]['value']}", data['data'][3]['value'], str(parsedData))

        g_log.debug(f"parsedData: {parsedData}")



    if aid == TP_PLUGIN_ACTIONS['EditJson']['id']:
        the_data = data['data'][2]['value']
        path_to_find = data['data'][0]['value']
        change_to = data['data'][1]['value']
        
        pathlist = get_pathlist(path_to_find)
        
        ## Loading the data into a json object
        json_data = json.loads(the_data)
        
        # replacing the data in json and then sending it back to TP
        json_data[pathlist[0]][pathlist[1]] = change_to
        TPClient.createState(PLUGIN_ID + f".userState.{data['data'][3]['value']}", data['data'][3]['value'], str(json_data))
       
        g_log.info(f"Edit Json Action: {data}")
        
        
    if aid == TP_PLUGIN_ACTIONS['WriteJson']['id']:
        write_json_to_file(data['data'][0]['value'], data['data'][1]['value'], data['data'][2]['value'])
    else:
        g_log.warning("Got unknown action ID: " + aid)





#################################---- FUNCTIONS ----#################################


requestListener = []

def findListener(listenerName):
    for listener in requestListener:
        if listenerName == list(listener.keys())[0]:
            return listener
    return None


def get_pathlist(path):
    """ 
    Find Everything inside of brackets which we utilize for our path
    """
    pathlist= re.findall(r"\[(.*?)\]", path)
    #  without the need for ' or "   - this will allow for fewer mistakes on the user side of things.
    ##pathlist= re.findall(r"\[\'(.*?)\'\]", path)
    return pathlist


def write_json_to_file(data, filename, indent=4, ensure_ascii=False):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)


def jsonPathfinder(path, data):
    data = json.loads(data)
    pathlist= get_pathlist(path)
    
    
    # Return the value of the path ONLY if it exists
    g_log.debug(f"pathlist: {pathlist}")
    return reduce(lambda d, k: d.get(k, None) if isinstance(d, dict) else None, pathlist, data)


def HtmlParser(html, path):
    pq = PyQuery(html)
    tag = pq(path)
    
    g_log.debug(f"tag: {tag.text()}")
    return tag.text()


def makeRequests(Method, endpoint, body, interval, result, listener):
    listenerData = listener[list(listener.keys())[0]]
    if result:
        TPClient.createState(PLUGIN_ID + f".userState.{result}", result, "")
        
    if listener and listenerData:
        while listenerData['status'] != "stop":
            if Method == "GET":
                requestResult = requests.get(url=listenerData["host"] + endpoint,
                     headers=json.loads(listenerData["header"]) if listenerData["header"] else None,
                      data=body)
                TPClient.stateUpdate(PLUGIN_ID + f".userState.{result}", requestResult.text)
                
            elif Method == "POST":
                requestResult = requests.post(url=listenerData["host"] + endpoint,
                     headers=json.loads(listenerData["header"]) if listenerData["header"] else None,
                      data=body)
                TPClient.stateUpdate(PLUGIN_ID + f".userState.{result}", requestResult.text)
                
            elif Method == "PUT":
                requestResult = requests.put(url=listenerData["host"] + endpoint,
                     headers=json.loads(listenerData["header"]) if listenerData["header"] else None,
                      data=body)
                TPClient.stateUpdate(PLUGIN_ID + f".userState.{result}", requestResult.text)
                
            elif Method == "DELETE":
                requestResult = requests.delete(url=listenerData["host"] + endpoint,
                     headers=json.loads(listenerData["header"]) if listenerData["header"] else None,
                      data=body)
                TPClient.stateUpdate(PLUGIN_ID + f".userState.{result}", requestResult.text)
            sleep(int(interval))
            
        if listenerData['status'] == "stop":
            pass # maybe remove all states thats created by the listener


def stateUpdate():
    while TPClient.isConnected():
        if requestListener and PLUGIN_ID + ".SetuprequestUsingListener.listoflistener" not in TPClient.choiceUpdateList:
            g_log.debug(requestListener)
            
            if (listofListener := [list(x.keys())[0] for x in requestListener]) != TPClient.choiceUpdateList:
                TPClient.choiceUpdate(PLUGIN_ID + ".SetuprequestUsingListener.listoflistener", listofListener)
        sleep(0.2)





#################################---- END FUNCTIONS ----#################################





# Shutdown handler
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.info('Received shutdown event from TP Client.')
    # We do not need to disconnect manually because we used `autoClose = True`


# Error handler
@TPClient.on(TP.TYPES.onError)
def onError(exc):
    g_log.error(f'Error in TP Client event handler: {repr(exc)}')







## main
def main():
    global TPClient, g_log
    ret = 0  # sys.exit() value

    # default log file destination
    logFile = f"./{PLUGIN_ID}.log"
    # default log stream destination
    logStream = sys.stdout

    # Set up and handle CLI arguments. These all relate to logging options.
    # The plugin can be run with "-h" option to show available argument options.
    # Addtionally, a file constaining any of these arguments can be specified on the command line
    # with the `@` prefix. For example: `plugin-example.py @config.txt`
    # The file must contain one valid argument per line, including the `-` or `--` prefixes.
    # See the plugin-example-conf.txt file for an example config file.
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>",
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")

    # his processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None

    # Configure the Client logging based on command line arguments.
    # Since the Client uses the "root" logger by default,
    # this also sets all default logging options for any added child loggers, such as our g_log instance we created earlier.
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting {TP_PLUGIN_INFO['name']} v{__version__} on {sys.platform}.")

    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret


if __name__ == "__main__":
    sys.exit(main())