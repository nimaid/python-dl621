dl621
========================

A simple python module and CLI utility to download e621 images with embedded XMP tags and description


Installation
========================

The module requires Exempi, which is only available for Linux and Mac. Hence, this module only works on Linux and Mac. On Windows, you can use Windows Subsystem for Linux (WSL) to run code using this module.

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
    usage: dl621 [-h] -i ID [-f FOLDER] [-n NAME] [-t] [-j] [-a USERNAME:API_KEY]
                 [-u USERAGENT] [-m MEM_LIMIT]

    Downloads e621 images with embedded XMP tags and description

    optional arguments:
      -h, --help            show this help message and exit
      -i ID, --post_id ID   the ID of the e621 post
      -f FOLDER, --dl_folder FOLDER
                            the folder to download to
      -n NAME, --name_pattern NAME
                            the file name (no extention), Replacements: {m}=md5,
                            {i}=post_id
      -t, --no_tags         don't embedd tags or metadata
      -j, --save_json       saves metadata in a seperate .json file in additon to
                            other options
      -a USERNAME:API_KEY, --authorization USERNAME:API_KEY
                            your e621 username and API key
      -u USERAGENT, --user_agent USERAGENT
                            manual override of the user agent string
      -m MEM_LIMIT, --memory_limit_ratio MEM_LIMIT
                            max percentage of available memory to use


It can also be imported and used in your own scripts (default options shown)::

    import dl621

    r = dl621.download_image(post_id, output_folder=".", name_pattern="dl621_{i}_{m}", add_tags=True, save_json=False, use_messages=False, use_warnings=True, custom_json=None, auth=None, download_timeout=5, user_agent="dl621/1.0 (by nimaid on e621)", memory_limit_ratio=0.8)
    
    if r["saved_image"]:
        print("Image downloaded! Location:", r["path_image")
    else:
        print("Download failed!")

The ``download_image()`` function returns a dictionary with the following items:

* post_exists (bool)
* post_deleted (bool)
* post_missing_url (bool)
* saved_image (bool)
* saved_tags (bool)
* saved_json (bool)
* path_image (string)
* path_json (string)
