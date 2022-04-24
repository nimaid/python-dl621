import argparse
import sys

import requests
import urllib.request
import os
import imgtag

__version__ = 0.1

__default_user_agent__ = "e621-Batch-Downloader/1.0 (by nimaid on e621)"

def get_info_json(post_id, user_agent=__default_user_agent__):
    if type(post_id) != int:
        raise TypeError("'post_id' must be an integer.")
    
    url = "https://e621.net/posts/" + str(post_id) + ".json"
    
    headers = {"User-Agent": user_agent}
    
    r = requests.get(url, headers=headers)
    
    if r.status_code != 200:
        return None
    
    return r.json()["post"]

def get_tags_from_json(info_json):
    post_id = info_json["id"]
    tags_src_obj = info_json["tags"]
    
    tags_out = list()
    for tag_cat in tags_src_obj.keys():
        tags_in_cat = tags_src_obj[tag_cat]
        for curr_tag in tags_in_cat:
            if tag_cat == "general":
                tags_out.append(curr_tag)
            else:
                tags_out.append("{}: {}".format(tag_cat, curr_tag))
    
    
    # Manual tags
    #description = info_json["description"]e621_790353
    
    # Parent and child tags
    parent = info_json["relationships"]["parent_id"]
    children = info_json["relationships"]["children"]
    
    if parent != None:
        tags_out.append("post_parent: {}".format(parent))
    
    if len(children) > 0:
        for child in children:
            tags_out.append("post_child: {}".format(child))
    
    # Site and ID tags
    tags_out.append("post_site: e621.net")
    tags_out.append("post_id: {}".format(post_id))
    
    # Sources tags
    sources = info_json["sources"]
    for source in sources:
        tags_out.append("source: {}".format(source))
    
    return tags_out

def download_image(post_id, output_folder=".", name_prefix=None, add_tags=True, user_agent=__default_user_agent__):
    # Get information from e621 API
    print("[{}] Getting info for e621 post...".format(post_id))
    image_info = get_info_json(post_id, user_agent=user_agent)
    if image_info == None:
        print("    ERROR: No info returned.")
        return None
    if image_info["flags"]["deleted"]:
        print("    ERROR: Image has been deleted.")
        return None
    
    # Download image
    print("    Downloading image...")
    image_url = image_info["file"]["url"]
    image_ext = image_url.split("/")[-1].split(".")[-1].lower()
    image_name = "e621_{}.{}".format(post_id, image_ext)
    if name_prefix != None:
        image_name = name_prefix + image_name
    
    image_path = os.path.join(output_folder, image_name)
    
    urllib.request.urlretrieve(image_url, image_path)
    
    # Tag image
    if add_tags:
        print("    Embedding tags...")
        image_tags = get_tags_from_json(image_info)
        
        image_tags_obj = imgtag.ImgTag(image_path)
        image_tags_obj.add_tags(image_tags)
        image_tags_obj.close()
    
    print("    Done downloading! Location: {}".format(image_path))










    
    
    
def parse_args(args):
    parser = argparse.ArgumentParser(description="Downloads e621 images with tags")
    
    parser.add_argument(dest="post_id", help="the ID of the e621 post", type=int, metavar="e621_id")
    
    return parser.parse_args(args)

def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = parse_args(args)
    
    download_image(args.post_id)


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m e621_dl.skeleton 42
    #
    run()