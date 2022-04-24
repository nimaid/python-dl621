dl621
========================

A simple python module to download e621 images with embedded tags and description


Installation
========================

``pip install dl621``


Usage
========================

The program can be used as a simple command line program:

``e621-dl MY_POST_ID``

It can also be imported and used in your own scripts::

	import dl621

	r = dl621.download_image(post_id, output_folder=".", name_prefix=None, add_tags=True, user_agent=__default_user_agent__)
	if r != None:
		print("Image downloaded! Location:", r)
	else:
		print("Download failed!")
