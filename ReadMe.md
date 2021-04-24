# CHATBOT-SHOUTOUT

This shows a streamers profile image when they are given a shoutout in the channel. 
  
[![See Shoutout Overlay In Action](https://img.youtube.com/vi/CCBg_gXIu8c/0.jpg)](https://www.youtube.com/watch?v=CCBg_gXIu8c)  

## REQUIREMENTS

- Install [StreamLabs Chatbot](https://streamlabs.com/chatbot)
- [Enable Scripts in StreamLabs Chatbot](https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts)
- [Microsoft .NET Framework 4.7.2 Runtime](https://dotnet.microsoft.com/download/dotnet-framework/net472)

## INSTALL

- Download the latest zip file from [Releases](https://github.com/camalot/chatbot-shoutout/releases/latest)
- Right-click on the downloaded zip file and choose `Properties`
- Click on `Unblock`  
[![](https://i.imgur.com/vehSSn7l.png)](https://i.imgur.com/vehSSn7.png)  
  > **NOTE:** If you do not see `Unblock`, the file is already unblocked.
- In Chatbot, Click on the import icon on the scripts tab.  
  ![](https://i.imgur.com/16JjCvR.png)
- Select the downloaded zip file
- Right click on `Shoutout Overlay` and select `Insert API Key`. Click yes on the dialog.  
[![](https://i.imgur.com/AWmtHKFl.png)](https://i.imgur.com/AWmtHKF.png)  

## CONFIGURATION

Make sure the script is enabled  
[![](https://i.imgur.com/XseFOhGl.png)](https://i.imgur.com/XseFOhG.png)  

Click on the script in the list to bring up the configuration.

### COMMAND SETTINGS  

[![](https://i.imgur.com/S0MXSeSl.png)](https://i.imgur.com/S0MXSeS.png)  

| ITEM | DESCRIPTION | DEFAULT | 
| ---- | ----------- | ------- | 
| `Shoutout Command` | The command to trigger the shoutout | `!so` |
| `Cooldown` | The amount of seconds between each allowed command trigger | `30` |
| `Permission Level` | The permission level required to trigger the command | `Everyone` |
| `Duration` | The amount of time, in seconds the overlay will display on screen. | `10` |
| `OPEN OVERLAY IN BROWSER` | Open the overlay in your browser for testing. | |
| `SEND TEST EVENT` | Sends a test event to the overlay. | |

### STYLE SETTINGS

[![](https://i.imgur.com/NIzVvuTl.png)](https://i.imgur.com/NIzVvuT.png)  

| ITEM | DESCRIPTION | DEFAULT | 
| ---- | ----------- | ------- | 
| `Enable Shadows` | Enable shadows around the items | `true` |
| `Logo Shape` | The shape of the users logo | `circle` |
| `Caster Color` | The color of the text for the caster | `rgba(255,0,0,1)` |
| `Twitch Link Color` | The color of the text for the twitch link | `rgba(255,0,0,1)` |
| `In Transition` | The Transition Animation | `slideInRight` |
| `Attention Animation` | The animation to draw attention before/after the out/in transitions | `none` |
| `Out Transition` | The Transition Animation | `slideOutLeft` |

### BUTTONS

[![](https://i.imgur.com/UaPEPp4l.png)](https://i.imgur.com/UaPEPp4.png)  

| ITEM | DESCRIPTION |  
| ---- | ----------- |  
| `Check For Updates` | Check for new versions of the script | 
| `Save Settings` | Save the changes to the settings | 

### Custom parameters

This script adds 2 new custom parameters `$shoutout` and `$shoutout(name)`.

* `$shoutout` - This one should be used only in custom commands, it will shoutout the name of the user who used the command.
* `$shoutout(name)` - This one gives a shoutout to the user that is between parenthesis, for example:
    * `$shoutout(darthminos)`
    * `$shoutout($username)`

If you want to make a shoutout and also show text in chat you can insert the text after the custom parameter:

* `$shoutout($username) Thanks for the follow $username!`

## OVERLAY SETUP IN OBS / SLOBS 

- Add a new `Browser Source` in OBS / SLOBS  
[![](https://i.imgur.com/TAMQkeql.png)](https://i.imgur.com/TAMQkeq.png)
- Set as a `Local File` and choose the `overlay.html` in the `Shoutout Overlay` script directory. You can easily get to the script directory location from right clicking on `Shoutout Overlay` and choose `Open Script Folder`.
  - As a secondary method, you can leave `Local File` unchecked, and Click on `Open Overlay In Browser`. Copy the Url from the browser, and use that as the Url. The url should start with `file://`.
- Set the `width` and `height` to the resolution of your `Base (Canvas) Resolution`. 
- Add any additional custom CSS that you would like to add.
- Check both `Shutdown source when not visible` and `Refresh browser when scene becomes active`.  
[![](https://i.imgur.com/nouqPh0l.png)](https://i.imgur.com/nouqPh0.png)