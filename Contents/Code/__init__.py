# Welcome!
# Script created by god@e-grotto.faith
# github.com/camelgod/LainRadio.bundle/
# Version 0.2
# - Added dynamic channel listings from json
# - Fix error attempting to art the Trackobject

# Get IceCast json content from URL specified in DefaultPrefs / Plex channel settings
import json

def getLainChannels():
	try:
	    # Attempt to download and store JSON
	    page = HTTP.Request(Prefs['json_url']).content
	    d = json.loads(page)
	except:
            # Load fake json object to continue booting channel, allowing user to change URL again.
	    Log("Could not load JSON object. Please check server status and url in settings.")
	    d = {"icestats":{"source":[{"listenurl":"http://e-grotto.faith","server_name":"Error. Please check config and server status. (mp3)"
			}]
		    }
		}

	# Create array of channels from JSON object, catching only server name and listenurl
	channel_array = []
	for x in d['icestats']['source']:
	    #Filter out .ogg channels as they are not needed.
	    if x['server_name'].endswith('(mp3)'):
		# Filter out (mp3) and capitalize channel name for pretty lookin' names
		x['server_name'] = x['server_name'].capitalize()
		x['server_name'] = x['server_name'][:len(x['server_name'])-len('(mp3)')]
		channel_array.append(x)
		# Log to <plexfolder>/Logs/com.plexapp.plugins.lainradio.log
		Log('Added Lain Channel: ' + x['server_name'])
		Log('URL: ' + x['listenurl'])

	# Return the formated array to MainMenu()
	return channel_array


# General application information
TITLE = 'Lain Radio'
ART      = 'bg.jpg'
ICON     = 'icon-default.png'
GROUPNAME = 'Info'

####################################################################################################

def Start():
    # Initialize the plugin menus
    Plugin.AddViewGroup(GROUPNAME, viewMode = 'List', mediaType = 'items')

    # Setup the artwork and title for menus 
    # (Set album / artwork blur to "dim" instead of "blur" in your plex menu to see the clear background image of cyberpunk hong kong)

    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = GROUPNAME
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    TrackObject.thumb = R(ICON)
    # Art argument not supported by trackobject.

####################################################################################################
@handler('/music/lainradio', 'Lain Radio', art=ART)
def MainMenu():
	# Create container and append channels to list
	channel_array = getLainChannels()
	oc = ObjectContainer()
	for x in channel_array:
		oc.add(CreateTrackObject(url=x['listenurl'], art=R(ART), title=x['server_name'], fmt='mp3'))

	# Set background image for the menu listing all channels
	oc.art = R(ART)

	return oc


####################################################################################################
def CreateTrackObject(url, title, fmt, art, include_container=False, includeBandwidths=None):

	if fmt == 'mp3':
		container = Container.MP3
		audio_codec = AudioCodec.MP3
	elif fmt == 'aac':
		container = Container.MP4
		audio_codec = AudioCodec.AAC

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, art=art, title=title, fmt=fmt, include_container=True),
		rating_key = url,
		title = title,
		duration=999999999999,
		art = R(ART),
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(PlayAudio, url=url, ext=fmt))
				],
				container = container,
				audio_codec = audio_codec,
				audio_channels = 2,
				duration=999999999999
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object

####################################################################################################
def PlayAudio(url):
	return Redirect(url)
