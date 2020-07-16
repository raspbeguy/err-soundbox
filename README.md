# Introduction

Soundbox is a plugin to play sounds. Have fun on your open space work office.

# System requirements

Make sure the user running Errbot has permission to use sound. Most of the time, this is granted by adding the user to the `audio` group.

You have to install `mpv` media player. Maybe someday you will be able to specify your own audio playing command.

Sounds should be uploaded to a given directory, by default `/srv/sounds`. See `!plugin config Soundbox`.

# Commands

- `!soundbox add <filename> <alias1> [<alias2>...]`: Add a sound with a list of aliases. The sound file should be already present in the sounds directory.
- `!soundbox list`: List configured sounds.
- `!soundbox addaliases <existing_alias> <new_alias1> [<new_alias2>...]`: Add aliases to an existing sound.
- `!soundbox del <alias>`: Remove a sound. It does not remove the sound from the directory.
- `!sb <alias>`: Play a sound.
- `!kill`: Stop playing current sound.
- `!mute`: Temporarly disable playing sounds, for instance if you are calling a customer or if big boss visits the office.
