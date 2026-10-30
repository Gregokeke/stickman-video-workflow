# Individual oversized project downloads

All other project ZIPs, studies, videos, guides, references and the complete sound library are directly in the repository. Only these two whole ZIPs exceed GitHub's normal file limit. They are separately downloadable, unchanged, and each still contains its complete matching rendered video.

| Reference | Download | Save under the repository root as |
| --- | --- | --- |
| 6 | [Sugar-Two-Weeks-Editable-Project.zip](https://github.com/Gregokeke/stickman-video-workflow/releases/download/v1.1.0/Sugar-Two-Weeks-Editable-Project.zip) | `10-Project-6-Sugar-Two-Weeks/Sugar-Two-Weeks-Editable-Project.zip` |
| 7 | [Iron-Oxygen-Real-Energy-Final-Project.zip](https://github.com/Gregokeke/stickman-video-workflow/releases/download/v1.1.0/Iron-Oxygen-Real-Energy-Final-Project.zip) | `12-Project-7-Iron-Oxygen-Real-Energy/Iron-Oxygen-Real-Energy-Final-Project.zip` |

After cloning, the following commands fetch only these two projects and verify the complete workspace:

```bash
python3 tools/fetch_large_projects.py
python3 tools/verify_workspace.py
```

The fetch helper checks SHA-256 before installing each download, skips existing correct copies and does not overwrite an existing incorrect file. No paid storage change, Git LFS, split archive or old outer workspace ZIP is required.
