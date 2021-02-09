This is a temporary holding area for developer notes.

2/9/2021 (Tom)
* Exclusion list of jSON data elements in python legistar_json_file_compare.py was expanded. This is now a first attempt at a full exclusion list.
* The exclusion list should be converted to an "inclusion list" so that, if new elements are added by Legistar, they are automatically visible to the user.
* The user option for level-of-detail-of-changes-to-receive could use the Legistar JSON hierarchy of Meeting (Event), Agenda item (Eventitem), and Attachments (MatterAttachment).
* To be added to an explanation of the "diff" logic: if an Event, Item, or Matter ID is new then none of attributes of the Event, Item, or Matter will be shown as changed content.
* A next step: write Python method convert the contents of results.json to a user-readable message. 
