Some items, by necessity of having an English variable name, are already in english. Other items are just pure data.

## Processing

Python with `xmltodict` will be used to parse and unparse the XML data. It requires no XML schemas, and turns it straight into a Python Dict as if it was a JSON file: and back. Which helps because the KC3 translations are also in JSON.

Installation:

```
sudo pip3 install xmltodict
```

```
import json
import xmltodict

# open file: maybe do with open
maparea = open("mst_maparea.xml", 'rb')
# get dict
mapdict = xmltodict.parse(maparea)
print(mapdict['mst_maparea_data']['mst_maparea'][0]) # display first item
# save changes to file: with open?
xmltodict.unparse(mapdict)
```

## Match with KC3 

Some critical components are already translated by KC3, so compile those translations in.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_ship.xml` (Done): `ships.json` - Defines the ship names.  For the most part, since kai and zwei and whatever crap may need to be handled with regex replace `改二`. Yomi doesn't need to be changed: it in fact can help basic Japanese readers.
    * `dict['mst_ship_data']['mst_ship'][0]` - Iterate through dict, first replace `改` with `Kai` and `二` with Ni, then split string by space and take first item (name) as key against `ships.json`, then place translation in it's place. Leave Yomi untranslated.
    * `dict['mst_ship_data']['mst_ship'][0]['Name'] = shipsjson[dict['mst_ship_data']['mst_ship'][0]['Name']] # given shipsjson as ships.json` - 
  * `mst_slotitem.xml` (Done): `items.json` - The equipment items in question. 
    * `dict['mst_slotitem_data']['mst_slotitem'][0]` - Just ignore the index, use `items.json` which has the JP name as primary key value.
  * `mst_stype.xml`: `stype.json` - Enemy ship types. Use `stype.json`, use sequence for Id (first quote is set to id 0).
    * `dict['mst_stype_data']['mst_stype'][0]` - Corresponds to ID 1. stype.json has an empty string in 0, so the equivalent is `stype[1]`, `index + 1`.
  * `mst_shiptext.xml` - Ship description and get message. The items are sorted by ship ID. `Quotes.json` has message ID `1` as get message and `25` as ship info.
    * `dict['mst_shiptext_data']['mst_shiptext'][0]['Id']` - The IDs from `ships.json` from KC3 can be used toward this: the ship names in Unicode can be used as dict keys, and regex replace.

## Translate from other Sources (Essential)

Other components aren't translated by KC3, so we will have to look elsewhere (such as the wiki) or create our own. These are second priority.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_maparea.xml` - Defines map area names.
    * `dict['mst_maparea_data']['mst_maparea'][0]` - 0 is ID 1
  * `mst_mapinfo.xml` - Provides info about the subsections of a map area. Requires double primary keys as ID...
  * `mst_mission2.xml` - Missions within map areas?
  * `mst_payitem.xml` - Store items to buy.
  * `mst_payitemtext.xml` - Store items descriptions.
  * `mst_ship_class.xml` - Ship classes and types.
  * `mst_slotitemtext.xml` - Descriptions of what slot items do.
  * `mst_useitem.xml` - Consumable items.
  * `mst_useitemtext.xml` - Consumable item descriptions.
  * `mst_mapenemy/` - Folder with all the enemies of the certain map. as `<Deck Name>`.
  * `mst_slotitem_equiptype.xml` - Equipment types. Can't use KC3's `equiptype.json`, since it doesn't correspond correctly...
  * `mst_quest.xml`: Quest information. This differs from normal Kantai Collection by a small but significant amount due to the lack of daily operations, so you willneed to scrape from the wiki. Category number in XML corresponds A-G to 1-7.
    * `dict['mst_quest_data']['mst_quest'][0]` - Disregard the index, just match `Id` to `quests.json` and get the corresponding data from there. (`Name` -> `"name"`, `Details` -> `"desc"`)

## Translate from other Sources (Non-Essential)

These tend to be less pressing.

* `Xml/tables/master` - All the files of interest are in this folder.
  * `mst_bgm_jukebox.xml` - BGM names. Dunno if they should be translated.
  * `mst_bgm.xml` - More BGM names.
  * `mst_furniture.xml` - Furnishings.
  * `mst_furnituretext.xml` - Furnishing descriptions.

## Non translation XMLs

These files have no need for translation as they are pure data.

* `Xml/debug` - Debug information perhaps from the flash game?
* `Xml/defines` - Battle production rate definition.

All folders and  files below are relative to `Xml/tables/master`.

### Folders

```
mst_map_bgm/
mst_mapcell/
mst_mapcellincentive/
mst_mapenemylevel/
mst_mapincentive/
mst_maproute/
mst_shipget/
```

### Files

```
mst_bgm_season.xml
mst_bgm.xml
mst_const.xml
mst_createship_change.xml
mst_createship_large_change.xml
mst_createship_large.xml
mst_createship.xml
mst_equip_category.xml
mst_equip_ship.xml
mst_equip.xml
mst_files.xml
mst_item_limit.xml
mst_item_package.xml
mst_item_shop.xml
mst_quest_slotitemchange.xml
mst_questcount_reset.xml
mst_questcount.xml
mst_radingrate.xml
mst_radingtype.xml
mst_rebellionpoint.xml
mst_ship_resources.xml
mst_shipgraph.xml
mst_shipgraphbattle.xml
mst_shipupgrade.xml
mst_slotitem_convert.xml
mst_slotitem_remodel_detail.xml
mst_slotitem_remodel.xml
mst_slotitemget2.xml
mst_stype_group.xml
```
