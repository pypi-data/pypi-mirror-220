import thin_osm_api_wrapper
import csv
import collections
from osm_bot_abstraction_layer.overpass_downloader import download_overpass_query
from osm_iterator import osm_iterator
import time
import datetime

def text():
    return """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    
def main():
    config = {
        'key': 'related:wikipedia',
        'value': None, # may be None - in such case it looks for all values of key
        'area_identifier_key': None, # may be None, in such case search is worldwide, 'ISO3166-1' is a good identifier
        'area_identifier_value': 'PL', # ignored if area_identifier_key is None
        'list_all_edits': True,
        'list_all_edits_made_by_this_users': [], # ignored with list_all_edits set to True
    }
    process_case(config)

def download_object_list(config):
    area_query = ""
    area_filter = ""
    if config['area_identifier_key'] != None:
        area_query = "\n    area['" + config['area_identifier_key'] + "'='" + config['area_identifier_value'] + "']->.searchArea;\n"
        area_filter = "(area.searchArea)"
    value_part = ""
    if config['value'] != None:
        value_part = """'='""" + config['value']
    download = """
    [out:xml][timeout:25];""" + area_query + """
    (
    nwr['""" + config['key'] + value_part + """']""" + area_filter + """;
    );
    out skel qt;
    """
    """
    note:
    use

    out skel qt;

    instead of

    out body;
    >;

    otherwise total object count will be inaccurate
    """
    download_overpass_query(download, 'output.osm')


def this_tags_are_matching_what_was_requested(tags, config):
    if config['key'] in tags:
        if config['value'] == None:
            return True
        if tags[config['key']] == config['value']:
            return True
    return False



def record_objects(element):
    global osm_object_store
    print(element.element.tag, element.element.attrib['id'])
    osm_object_store.append({"type": element.get_type(), "id": element.get_id()})


def create_object_store(config):
    download_object_list(config)

    global osm_object_store
    osm_object_store = []

    filepath = "output.osm"
    osm = osm_iterator.Data(filepath)
    osm.iterate_over_data(record_objects)
    return osm_object_store

def sleep_before_retry(error_summary, url, params, json_data):
    print("sleeping before retry due to", error_summary)
    print(url)
    print(params)
    print(json_data)
    print()
    sleep(100)
    print()
    print("retrying on", datetime.now().strftime("%H:%M:%S (%Y-%m-%d)"))


def process_case(config):
    osm_object_store = create_object_store(config)
    changeset_list = ""

    users = collections.Counter()
    edits = {}
    objects = {}
    for entry in osm_object_store:
        object_type = entry["type"]
        object_id = entry["id"]
        for history in thin_osm_api_wrapper.api.history_json(object_type, object_id, user_agent='who_added_this_tag_script'):
            if 'tags' in history:
                if this_tags_are_matching_what_was_requested(history['tags'], config):
                    # uncomment following line to show all relevant changesets
                    #print("https://www.openstreetmap.org/changeset/"+ str(history['changeset']))
                    uid = history['uid']
                    user = history['user']
                    object_link = "https://www.openstreetmap.org/" + object_type + '/' + object_id + "/history"
                    users[user] = users[user] + 1
                    if user in config['list_all_edits_made_by_this_users'] or config['list_all_edits']:
                        changeset_list += "https://www.openstreetmap.org/changeset/" + str(history['changeset']) + " editing "+  object_link + "\n\n"
                    if users[user] == 1 or edits[user] < int(history['changeset']):
                        edits[user] = int(history['changeset'])
                        objects[user] = object_link
                    break
    summary(users, edits, objects, config)
    print(len(osm_object_store), "objects exist in total")
    print(changeset_list)

def summary(users, edits, objects, config):
    print(users)
    total = 0
    for entry in users.most_common():
        name = entry[0]
        count = entry[1]
        total += count
        print("https://www.openstreetmap.org/user/"+name.replace(" ", "%20"), "https://www.openstreetmap.org/changeset/"+ str(edits[name]), objects[name], count)
    print(total, "objects listed with their authors")
    print()
    value_description = ""
    if config['value'] != None:
        value_description = "|" + config['value']
    tag_description = "{{tag|" + config['key'] + value_description + "}}"
    print(usage_table(tag_description, users, edits, objects))

def usage_table(tag_description, users, edits, objects):
    returned = """{| class="wikitable"
|+ What added """ + tag_description + """?
|-
! User !! Example changeset !! History of object !! Count""" + "\n"
    for entry in users.most_common():
        name = entry[0]
        count = entry[1]
        returned += """|-
| """ + name + """ || """ + "https://www.openstreetmap.org/changeset/"+ str(edits[name]) + """ || """ + objects[name] + """ || """ + str(count) + "\n"
    returned += """|}
Generated with https://codeberg.org/matkoniecz/who-added-this-tag - counts first addition to objects were carrying this tag as of """ + datetime.datetime.now().strftime("%Y-%m-%d") + "."
    return returned

if __name__ == '__main__':
    main()
