
# Touch-Portal-DataParser
![Downloads](https://img.shields.io/github/downloads/KillerBOSS2019/TP-DataParser/total) 
![Forks](https://img.shields.io/github/forks/KillerBOSS2019/TP-DataParser) 
![Stars](https://img.shields.io/github/stars/KillerBOSS2019/TP-DataParser) 
![License](https://img.shields.io/github/license/KillerBOSS2019/TP-DataParser)

- [Touch Portal DataParser](#Touch-Portal-DataParser)
  - [Description](#description)
  - [Features](#Features)
    - [Actions](#actions)
        - [Data Parser](#KillerBOSS.TPPlugin.DataParser.mainactions)
    - [States](#states)
        - [Data Parser](#KillerBOSS.TPPlugin.DataParser.mainstates)
  - [Installation Guide](#installation)
  - [Bugs and Support](#bugs-and-suggestion)
  - [License](#license)
  
# Description

TP-DataParser allows you to parse and edit Json or HTML formatted data. If you have other type of data that aren't on the list feel free send a request to me. and I'll try my best!.

This documentation generated for Touch Portal DataParser V100 with [Python TouchPortal SDK](https://github.com/KillerBOSS2019/TouchPortal-API).
# Features

## Actions
<details open id='KillerBOSS.TPPlugin.DataParser.mainactions'><summary><b>Category:</b> Data Parser <small><ins>(Click to expand)</ins></small></summary><table>
<tr valign='buttom'><th>Action Name</th><th>Description</th><th>Format</th><th nowrap>Data<br/><div align=left><sub>choices/default (in bold)</th><th>On<br/>Hold</sub></div></th></tr>
<tr valign='top'><td>Create HTTP Listener</td><td>createHTTPListener is a action that allows to setup a base connection and use it to make actual request.</td><td>Create listener name[listenerName] host url[host] and Header[header]</td><td><ol start=1><li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>Setup endpoint calls using listener</td><td>This will use listener that you've created using `Create HTTP Listener` action as a base. And then use this to actually send request to a endpoint with a intervel aka it will automatically update x seconds and save the result.</td><td>Use[listeners][requestMethod] to endpoint[endpoint]and optional body[body]and request every[intervel]seconds and save result to[result]</td><td><details><summary><ins>Click to expand</ins></summary><ol start=1>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
<li>Type: choice &nbsp; 
Default: <b>GET</b> Possible choices: ['GET', 'POST', 'PUT', 'DELETE']</li>
<li>Type: text &nbsp; 
Default: <b>/</b></li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
Default: <b>5</b></li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</details><td align=center>No</td>
<tr valign='top'><td>Resume, Pause or Delete a listener</td><td>This will Pause, Resume, and Delete a listener. once deleted it will remove all the states that's created from this listener</td><td>[listenerControl] [listeners] update</td><td><ol start=1><li>Type: choice &nbsp; 
Default: <b>Delete</b> Possible choices: ['Pause', 'Resume', 'Delete']</li>
<li>Type: choice &nbsp; 
&lt;empty&gt;</li>
</ol></td>
<td align=center>No</td>
<tr valign='top'><td>Parsing data</td><td>ParseData action allows you to get specific data field from Json or HTML. for example {'website host': 'blah blah'} you can get value of `website host` which is `blah blah`.</td><td>Parse[dataType]data[data]to get[dataPath]and save result to[result]</td><td><details><summary><ins>Click to expand</ins></summary><ol start=1>
<li>Type: choice &nbsp; 
Default: <b>Json</b> Possible choices: ['Json', 'Html']</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</details><td align=center>No</td>
<tr valign='top'><td>Editing json data field</td><td>EditJson allows you to change specific json field to a new data. for example if I have `{'name': 'someone'} I can change from `someone` to `something` as a example.</td><td>Change [data] at path[jsonPath] to [newData] and save to[result]</td><td><details><summary><ins>Click to expand</ins></summary><ol start=1>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
<li>Type: text &nbsp; 
&lt;empty&gt;</li>
</ol></td>
</details><td align=center>No</td>
</tr></table></details>
<br>

## States
<details open id='KillerBOSS.TPPlugin.DataParser.mainstates'><summary><b>Category:</b> Data Parser <small><ins>(Click to expand)</ins></small></summary>


| Id | Description | DefaultValue | parentGroup |
| --- | --- | --- | --- |
| .state.totalListenerCreated | DataParser total listener created | 0 |   |
</details>

<br>

# Installation
1. Goto [Releases](https://github.com/KillerBOSS2019/TP-DataParser/releases) and Download latest version for your system.
 2. After downloading the .tpp file goto open TouchPortal GUI and click on the gear icon and click `Import Plug-in`
 3. After imported the plugin you may or may not need to restart TouchPortal but it should pop up something says do u want to allow this plugin to run. Click `Trust Always`
# Bugs and Suggestion
Open an [issue](https://github.com/KillerBOSS2019/TP-DataParser/issues) or join offical [TouchPortal Discord](https://discord.gg/MgxQb8r) for support.


# License
This plugin is licensed under the [GPL 3.0 License] - see the [LICENSE](LICENSE) file for more information.

