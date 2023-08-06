# Description

Automation GUI for Android App Analysis

# Installation

`pip install autoappanalysis`

# Usage

Create a config file like the following schema:

```json
// config.json
{
  "vm": "app-vm",                                              // Name of the VM
  "user": "admin",                                             // User Name 
  "pw": "admin",                                               // Password
  "input": "/media/sf_avd",                                    // Path to AVD shared folder on VM
  "output": "/media/sf_results",                               // Path to result shared folder on VM
  "outputHost": "C:\\Users\\admin\\results",                   // Path to result shared folder on host
  "snapshot": "C:\\Users\\admin\\.android\\avd\\analysis.avd", // Path to AVD shared folder on host
  "comparison": [                                              // Array of objects to provide different 
        {                                                      // comparison setup.
            "first": "init",                                   // Each object holds a starting snapshot 
            "second": ["install", "noise"]                     // (first) to which the other snapshots
        },                                                     // (second) will be compared against
        {
            "fist": "install",
            "second": ["first_start"]
        },
        {
            "fist": "first_start",
            "second": ["continue_as_guest"]
        }
  ],
  "files": [                                                  // Paths to files which are going to be
        "/data/data/path/to/app/user.db",                     // extracted for each snapshot
        "/data/data/path/to/app/host.db",
        "/data/data/path/to/app/config.json"
    ]
}
```


# Example

`python -m autoappanalysis -c config.json`


![](img/01.jpg)


| Button | Description |
| --- | ---|
| Create Snapshot | Create a AVD Snapshot with `Snapshot Name` and `Snapshot Number` and extract all files given by `AVD Files to be extracted` |
| Decrypt Snapshots | Decrypts all snapshots in `VM Input Directory` |
| Analyse Snapshots | Analyses all snapshots in `VM Input Directory + /decrypted` as well as all `AVD Files to be extracted` based on given comparison rules in config.json |
| Extract Files | Extract all files given by `AVD Files to be extracted` |


# License

MIT