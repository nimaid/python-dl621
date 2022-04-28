dl621
========================

A simple python module and CLI utility to download e621 images with embedded XMP tags and description


Installation
========================

The module requires Exempi, which is only available for Linux and Mac. Hence, this module only works on Linux and Mac.

To easily install everything via conda:

``conda env create -f environment.yml``

To manually install just the module (still needs Exempi installed seperately):

``pip install dl621``

To manually install Exempi on Debian:

``sudo apt-get install -y exempi``

Usage
========================

The program can be used as a simple command line program::

    $ dl621 -h
    usage: dl621 [-h] -i ID [-f FOLDER] [-n NAME] [-t] [-a USERNAME:API_KEY] [-u USERAGENT]

    Downloads e621 images with embedded XMP tags and description

    optional arguments:
      -h, --help            show this help message and exit
      -i ID, --post_id ID   the ID of the e621 post
      -f FOLDER, --dl_folder FOLDER
                            the folder to download to
      -n NAME, --name_pattern NAME
                            the file name (no extention), Replacements: {m}=md5, {i}=post_id
      -t, --no_tags         don't save tags or metadata
      -a USERNAME:API_KEY, --authorization USERNAME:API_KEY
                            your e621 username and API key
      -u USERAGENT, --user_agent USERAGENT
                            manual override of the user agent string



It can also be imported and used in your own scripts (default options shown)::

    import dl621

    r = dl621.download_image(post_id, output_folder=".", name_pattern="dl621_{i}_{m}", add_tags=True, use_messages=False, use_warnings=True, custom_json=None, auth=None, user_agent="dl621/1.0 (by nimaid on e621)")
    if r != None:
        print("Image downloaded! Location:", r)
    else:
        print("Download failed!")
