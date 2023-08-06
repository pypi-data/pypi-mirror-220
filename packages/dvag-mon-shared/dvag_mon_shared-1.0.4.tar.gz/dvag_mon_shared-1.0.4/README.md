# Shared libraries for Infra-Monitoring-Functions Python Functions

## Build process

Tthe libraries are included in the requirments.txt. The installation process does not change to the normal process. Just run a pip installation of the requirments.txt

```bash
pip3 install -r requirements.txt 
```

## Import of the Libraries

```python
from dvag_mon_shared.AzureCredentials import Az_login
from dvag_mon_shared.PushgwHeartbeat import PushgwHeartbeat
```
Example:

From dvag_mon_shared (Package Name).AzureCredentials (File Name) import Az_login (Class Name)

## Add new libraries

To add a new library just copy it to the dvag-shared-libs folder and reinstall it using pip and you you are good to go. Add new dependencies to the pyproject.toml