# Password-manager
Password manager - using tkinter for interface mysql for database and random module to generate password

![alt text](https://github.com/Neutrino-Tech/password-manager/blob/main/1.png)
![alt text](https://github.com/Neutrino-Tech/password-manager/blob/main/2.png)

<h3>Installation</h3>

```bash
pip install mysql-connector
pip install tk
git clone https://github.com/Neutrino-Tech/password-manager.git
```
<h3>Usage</h3>

```bash
> python3 manager.py
> Also create a database in mysql using ->
CREATE database password_manager;

```
<h3>Change your mysql config</h3>

```bash
> Also change the your host, username, password and database in manager.py ->
class MainWindow(tk.Tk):
    def __init__(self):
        # Connect SQL
        super().__init__()
        self.title("Password Manager")
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="password_manager"
```
