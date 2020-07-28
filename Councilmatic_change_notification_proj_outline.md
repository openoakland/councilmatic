# Councilmatic Change Notification

1. ## Strategy

   The purpose o this project is to extend the feature set of the Councilmatic application to allow user notification of change to a meeting or meeting instance.  These changes include date and time changes, cancellations, publication or alteration of agenda items or attachments to agenda items, and the publication or change of meeting minutes.

2. ## Build a change determination module.

   1. Develop logic flow of this module.
      1. Receive file names with paths for previous and latest API download files.
      2. Loop thru events (meetings) with an internal loop agenda items of the event, and a deeper internal loop for attachments to agenda items.  Capture information on elements that have changed when the name of the element is in a list of target elements.
      3. Create an English description of the change.
      4. Store the data record of the found change.

3. ## Design a database to record changes.

   1. This will likely be a JSON file as all other data is stored in this manner.
   2. Needed data elements include 
      1. Line number (unique key), 
      2. file date-time of previous api data set, 
      3. file date-time of latest data set, 
      4. key of changed value, 
      5. original value, 
      6. new value, 
      7. English description of change

4. ## Data file for aggregate statistics

   1. Tally of new users by day.
   2. Tally of users leaving by day.
   3. New change notice requests for specific meetings, counts by meeting
   4. New change notice request for a meeting type, counts by type.
   5. Tallies of users removing themselves from either of the two above meetings.

5. ## Build a module to integrate the email platform.

   1. Once the changes have been identified and stored, the meeting instance or meeting type would be searched for in the user list.  For each match in the user list an email would be generated and sent from the email platform.
   2. This email platform will also be used forgot password routine.

6. ## Work flow mods to capture changes.

   1. Prior to a new download the previous API download file would need to be copied.
   2. Perform the normal download.
   3. Launch the comparison of prior and latest files, adding to then file of changes.
   4. Compare the latest entries to the change list against the user requests and send emails for matches.
   5. Email summary report to HM, TT, and anyone else.

7. ## Modification of existing screen

   1. Link with each meeting to receive change notices for that meeting.
   2. An explanation of the change notice service.

8. ## User screens.

   1. ### User account page.

      1. New users register here.
      2. Existing users change preferences here.
      3. Password change to occur here.
      4. Remove meetings and meeting types here.
      5. Add a meeting type here.
      6. Instructions for how to follow a specific meeting (link next to the meeting).

   2. ### Forgot Password process.

      1. Click link about forgot password.
      2. Page to enter email and submit (with note to check spam when submitted).
      3. Email sent with encrypted code in link. Encryption is one-way, based on email.
      4. Apply frequency and count limit to the change pwd requests.
      5. ?? Offer an email address for support??

   3. Any new screens need to be accessible via menu.

9. ## User database.

   1. Requirements
      1. Encrypted file
      2. In protected directory with no public rw or x rights.
      3. JSON format as array of objects (list of dicts in Python terms).
      4. Data Elements
         1. Email address (unique key)
         2. First name to be used on email messages.  Optional.
         3. Password
         4. List of specific meetings to follow.
         5. List of meeting types to follow.
         6. Date joined.

10. ## Legal

    1. A EULA agreement. 
       1. Things to include
          1. Erasing history.
          2. Hold harmless

11. ## Description and explanation for users