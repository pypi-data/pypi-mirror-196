# Description

Automation GUI for Android App Analysis

# Installation

`pip install autoappanalysis`

# Usage

Create a config file like the following schema:

```json
// config.json
{
  "vm": "app-vm",                                             // Name of the VM
  "user": "admin",                                            // User Name 
  "pw": "admin",                                              // Password
  "input": "/media/sf_avd",                                   // Path to AVD shared folder on VM
  "output": "/media/sf_results",                              // Path to result shared folder on VM
  "outputHost": "C:\\Users\\admin\\results",                  // Path to result shared folder on host
  "snapshot": "C:\\Users\\admin\\.android\\avd\\analysis.avd" // Path to AVD shared folder on host
}
```


# Example

`python -m autoappanalysis -c config.json`


![](img/01.jpg)


| Button | Description |
| --- | ---|
| Root | Get root on AVD |
| Extract File | Extract the file based on `AVD File Path` |
| Create Snapshot | Create a AVD Snapshot with `Snapshot Name` and `Snapshot Number` |
| Decrypt Snapshots | Decrypts all snapshots in `VM Input Directory` |
| Analyse Snapshots | Analyses all snapshots in `VM Input Directory + /decrypted`


# License

MIT