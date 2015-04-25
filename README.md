# vk_parser

Little experiment about working with vk API

### Start using
1. install pip if not installed ("python get-pip.py")
2. install requests package ("python -m pip install requests")
3. create user_token.py file (read below)
4. in vk_parser.py change _my_uid_ and _dialog_uid_ to preffered 
5. run vk_parser.py ("python vk_parser.py") and generate history_stat.txt
6. enjoy reading your stats

### Getting your personal vk token
1. create your application at vk.com and get application id
2. in browser make this request "https://oauth.vk.com/authorize?client_id=IDприложения&scope=messages,friends,offline&redirect_uri=https://oauth.vk.com/blank.html&display=page&v=5.21&response_type=token"
3. in answer get your access_token
4. create user_token.py with line "token = <YOUR_ACCESS_TOKEN>"
