```python
from mcred import CredManager
```


```python
credmanager = CredManager(host="host eg. 10.12.31.12", port=22, username="someusername", password="somepassword", remote_credentials_file_path="/path/to/credentials.json")
credmanager.pull()
Credentials = credmanager.get()
```
