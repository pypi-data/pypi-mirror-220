import thin_osm_api_wrapper
import csv
import collections
from osm_bot_abstraction_layer.overpass_downloader import download_overpass_query
from osm_iterator import osm_iterator
import time
import datetime

def download_object_list(config, filepath):
    area_query = ""
    area_filter = ""
    if config['area_identifier_key'] != None:
        area_query = "\n    area['" + config['area_identifier_key'] + "'='" + config['area_identifier_value'] + "']->.searchArea;\n"
        area_filter = "(area.searchArea)"
    value_part = ""
    if config['value'] != None:
        value_part = """'='""" + config['value']
    download_query = """
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
    download_overpass_query(download_query, filepath)


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


def create_object_store_from_downloaded(filepath):
    global osm_object_store
    osm_object_store = []

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
    filepath = "output.osm"
    download_object_list(config, filepath)
    osm_object_store = create_object_store_from_downloaded(filepath)
    changeset_list = ""

    users = collections.Counter()
    edits = {}
    objects = {}
    for entry in osm_object_store:
        object_type = entry["type"]
        object_id = entry["id"]
        for history_revision in thin_osm_api_wrapper.api.history_json(object_type, object_id, user_agent='who_added_this_tag_script'):
            if 'tags' in history_revision:
                if this_tags_are_matching_what_was_requested(history_revision['tags'], config):
                    # uncomment following line to show all relevant changesets
                    #print("https://www.openstreetmap.org/changeset/"+ str(history_revision['changeset']))
                    uid = history_revision['uid']
                    user = history_revision['user']
                    object_link = "https://www.openstreetmap.org/" + object_type + '/' + object_id + "/history"
                    changeset_link = "https://www.openstreetmap.org/changeset/" + str(history_revision['changeset'])
                    users[user] = users[user] + 1
                    if user in config['list_all_edits_made_by_this_users'] or config['list_all_edits']:
                        changeset_list += changeset_link + " editing "+  object_link + "\n\n"
                    if users[user] == 1 or edits[user] < int(history_revision['changeset']):
                        edits[user] = int(history_revision['changeset'])
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
