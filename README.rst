dl621
========================

A simple python module to download e621 images with embedded tags and description


Installation
========================

``pip install dl621``


Usage
========================

The program can be used as a simple command line program::

	$ dl621 -h
	usage: dl621 [-h] -i ID [-f FOLDER] [-p PREFIX] [-n] [-u USERAGENT]

	Downloads e621 images with tags

	optional arguments:
	  -h, --help            show this help message and exit
	  -i ID, --post_id ID   the ID of the e621 post
	  -f FOLDER, --dl_folder FOLDER
							the folder to download to
	  -p PREFIX, --name_prefix PREFIX
							this string will go at the beginning of filenames
	  -n, --no_tags         don't save tags or metadata
	  -u USERAGENT, --user_agent USERAGENT
							manual override of the user agent string


It can also be imported and used in your own scripts::

	import dl621

	r = dl621.download_image(post_id, output_folder=".", name_prefix=None, add_tags=True, user_agent=__default_user_agent__)
	if r != None:
		print("Image downloaded! Location:", r)
	else:
		print("Download failed!")
