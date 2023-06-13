Code in a Box is a small Python script to download code from either GitHub repos or local folders.

No major changes to this tool are planned. Any bugs/Issues will be fixed and the ability to download from other sources (sourceforge, online folders, etc) may be added, however

**Installation:**
Not "installed" as a package. Just download the file manually or copy and paste "install.txt" into a shell (or over an SSH connection for remote installation).

**Usage:**
    import code_in_a_box
    code_in_a_box.download(url, dest_folder, clear_folder=False)
    # "url" can be a link to the GitHub repo or a folder on a local machine.