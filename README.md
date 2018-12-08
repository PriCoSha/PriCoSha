# Pricosha

## Project Description

Our project is a content-sharing system bodied by various functions. For instance, main features include functions such as showing public/private items, posting and sharing items, tagging other users, showing rates, etc. Morevover, we create own extra features such as defriending, posting rate, tagging friendgroup, and adding file types for contentitems. 

The whole project is established by database, frontend, and backend. The frontend provides interactive interface. The backend disposes the data it extracts from the databaseand delivers the disposed data to the frontend. The frontend receives the data and presents it using the user-friendly form.

## Optional Features

1. Defriend
   1. only the owner of a friendgroup can defriend the people in the friendgroup that the owner owns
   2. After the person is defriended, the contentitem he/she has already shared in the friendgroup is still visible to other members in that friendgroup
   3. Similarly, the rate he/she has already posted is still visible to other members
   4. But this defriended person cannot see the contentitem from that friendgroup in his/her homepage
   5. The tag information of the item that is no more visible to the user is deleted and no more visible as well.

2. Post rate (comment)
   1. A person can post only one rate to a contentitem that is visible to him/her, this rate is visible to everyone who is visible to this contentitem

3. Tag friendgroup

    1. In the "Tag" interface, a user can choose to tag a single person or a group. If a person chooses to tag a friendgroup, this person must input the fg_name and the owner_email. To tag a group, both the tagger and the tagged group should be visible to the contentitem. When the person tags a group, only when all the group members approve the tag can this tag be shown.


4. Contents have type now (movie/picture). Different types have different attributes:
    1. Picture has location and format
    2. Movie has resolution and format
    3. Related item will display the file type and relevant attributes in relevant page.

## Group members’ contributions
* Baipeng Gong: View Public Content, View Shared Content Items, Tag Content Item, Post Rate
* Hongyi Li: Log in, Manage Tags, Add Friends, Tag Friend Group
* Chongling Zhu: Register, Post Content Item, Defriend, Content Type

## How to use

1. Create database using the configuration in `config.py` (Recommend MAMP, password:root. Leave the password empty if using XMAPP)

2. Insert testing entries using the `test_entries.sql` on google drive

3. Set up the environment

   ```bash
   pip install Flask
   pip install pymysql
   ```

4. Run

   ```bash
   python3 app.py
   ```

5. Use postman to play with the APIs


## API Documentation
https://documenter.getpostman.com/view/3813544/RzZDhwnp
