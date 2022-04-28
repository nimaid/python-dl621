import argparse
import sys
import warnings

import requests
import urllib.request
import os
import imgtag

__default_user_agent__ = "dl621/1.0 (by nimaid on e621)"
__default_name_pattern__ = "dl621_{i}_{m}"
__e621_base_url__ = "https://e621.net/"
__e621_endpoint_posts__ = "posts"
__e621_posts_per_request_limit__ = 320

def get_info_json(post_id, auth=None, user_agent=__default_user_agent__):
    if type(post_id) != int:
        raise TypeError("'post_id' must be an integer.")
    
    url = "{}{}/{}.json".format(__e621_base_url__, __e621_endpoint_posts__, post_id)
    
    headers = {"User-Agent": user_agent}
    
    if auth != None:
        auth = auth.split(":")
        if len(auth) != 2:
            raise ValueError("'auth' argument must be a string in the form of 'username:api_key'")
        
        a = requests.auth.HTTPBasicAuth(auth[0], auth[1])
        r = requests.get(url, headers=headers, auth=a)
    else:
        r = requests.get(url, headers=headers)
    
    if r.status_code != 200:
        return None
    
    return r.json()["post"]

def get_info_json_multiple(page=None, page_modifier=None, limit=None, tags=None, auth=None, user_agent=__default_user_agent__):
    # Build URL
    url = "{}{}.json".format(__e621_base_url__, __e621_endpoint_posts__)
    
    if limit != None:
        if type(limit) != int:
            raise ValueError("The 'limit' parameter must be an interger between 0 and {}".format(__e621_posts_per_request_limit__))
        if limit < 0 or limit > __e621_posts_per_request_limit__:
            raise ValueError("The 'limit' parameter must be an interger between 0 and {}".format(__e621_posts_per_request_limit__))
    else:
        limit = __e621_posts_per_request_limit__
    url += "?limit={}".format(limit)
    
    if type(page) == int:
        if page_modifier != None:
            if type(page_modifier) != str:
                raise TypeError("The 'page_modifier' parameter must be a string")
            if page_modifier not in ["a", "b"]:
                raise ValueError("The 'page_modifier' parameter must be either 'a' (after) or 'b' (before)")
            url += "&page={}{}".format(page_modifier, page)
        else:
            url += "&page={}".format(page) 
    elif page != None:
        raise TypeError("The 'page' parameter must be an integer (use 'page_modifier' for [b]efore and [a]fter)")
    
    if tags != None:
        if type(tags) != str:
            raise ValueError("The 'tags' parameter must be a string")
        url += "&tags={}".format(tags)
    
    # Get the data
    headers = {"User-Agent": user_agent}
    
    if auth != None:
        auth = auth.split(":")
        if len(auth) != 2:
            raise ValueError("'auth' argument must be a string in the form of 'username:api_key'")
        
        a = requests.auth.HTTPBasicAuth(auth[0], auth[1])
        r = requests.get(url, headers=headers, auth=a)
    else:
        r = requests.get(url, headers=headers)
    
    if r.status_code != 200:
        return None
   
    return r.json()["posts"]

def get_tags_from_json(info_json):
    post_id = info_json["id"]
    tags_src_obj = info_json["tags"]
    
    tags_out = list()
    
    # Regular tags
    for tag_cat in tags_src_obj.keys():
        tags_in_cat = tags_src_obj[tag_cat]
        for curr_tag in tags_in_cat:
            if tag_cat == "general":
                tags_out.append(curr_tag)
            else:
                tags_out.append("{}: {}".format(tag_cat, curr_tag))
    
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
    
    # MD5 tag
    tags_out.append("md5: {}".format(info_json["file"]["md5"]))
    
    # Rating tag
    tags_out.append("rating: {}".format(info_json["rating"]))
    
    # Pool tags
    for pool in info_json["pools"]:
        tags_out.append("pool: {}".format(pool))
    
    # Sources tags
    for source in info_json["sources"]:
        tags_out.append("source: {}".format(source))
    
    return tags_out

def print_if_true(in_string, do_print):
    if do_print:
        print(in_string)
def download_image(post_id, output_folder=".", name_pattern=__default_name_pattern__, add_tags=True, use_messages=False, use_warnings=True, custom_json=None, auth=None, user_agent=__default_user_agent__):
    # Get information from e621 API
    if custom_json != None:
        image_info = custom_json
    else:
        print_if_true("    Getting info for e621 post...".format(post_id), use_messages)
        image_info = get_info_json(post_id, user_agent=user_agent, auth=auth)
    
    # Check to make sure it's valid
    if image_info == None:
        print_if_true("    ERROR: No info returned.", use_messages)
        return None
    if image_info["flags"]["deleted"]:
        print_if_true("    ERROR: Image has been deleted.", use_messages)
        return None
    image_url = image_info["file"]["url"]
    if image_url == None:
        print_if_true("    ERROR: Image has no download URL. You may need to use your API key or change your user settings.", use_messages)
        return None
    
    # Create destination folder if it doesn't already exist
    #output_folder = os.path.realpath(output_folder)
    os.makedirs(output_folder, exist_ok=True)
    
    # Download image
    print_if_true("    Downloading image...", use_messages)
    image_name = name_pattern.format(m = image_info["file"]["md5"], i = post_id) + "." + image_info["file"]["ext"]
    
    image_path = os.path.join(output_folder, image_name)
    
    urllib.request.urlretrieve(image_url, image_path)
    
    # Add image metadata
    if add_tags:
        print_if_true("    Embedding metadata...", use_messages)
        try:
            image_tags_obj = imgtag.ImgTag(image_path)
            
            # Set title
            title = "{}{}/{}".format(__e621_base_url__, __e621_endpoint_posts__, post_id)
            image_tags_obj.set_title(title)

            # Set description
            description = image_info["description"].strip()
            if len(description) > 0:
                image_tags_obj.set_description(description)

            # Set tags
            image_tags = get_tags_from_json(image_info)
            image_tags_obj.add_tags(image_tags)
            image_tags_obj.close()
        except SystemError:
            print_if_true("        [FAILED] Could not save metadata in image!", use_messages)
            if use_warnings == True:
                warnings.warn("Could not save metadata in image!")
    
    print_if_true("    Done downloading! Location: {}".format(image_path), use_messages)
    return image_path



def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
    
def parse_args(args):
    parser = argparse.ArgumentParser(description="Downloads e621 images with embedded XMP tags and description")
    
    parser.add_argument("-i", "--post_id", dest="post_id", help="the ID of the e621 post", type=int, required=True, metavar="ID")
    parser.add_argument("-f", "--dl_folder", dest="dl_folder", help="the folder to download to", type=dir_path, default=".", metavar="FOLDER")
    parser.add_argument("-n", "--name_pattern", dest="name_pattern", help="the file name (no extention), Replacements: {m}=md5, {i}=post_id ", type=str, default=__default_name_pattern__, metavar="NAME")
    parser.add_argument("-t", "--no_tags", dest="add_tags", help="don't save tags or metadata", action='store_false')
    parser.add_argument("-a", "--authorization", dest="authorization", help="your e621 username and API key", type=str, default=None, metavar="USERNAME:API_KEY")
    parser.add_argument("-u", "--user_agent", dest="user_agent", help="manual override of the user agent string", type=str, default=__default_user_agent__, metavar="USERAGENT")
    
    return parser.parse_args(args)

def main(args):
    args = parse_args(args)
    
    download_image(post_id=args.post_id, output_folder=args.dl_folder, name_pattern=args.name_pattern, add_tags=args.add_tags, auth=args.authorization, user_agent=args.user_agent, use_messages=True, use_warnings=False)

def run():
    main(sys.argv[1:])

if __name__ == "__main__":
    run()