# Local Tracks

This folder holds optional audio and lyric files used by BloomBot and the music player.

- Put MP3/FLAC/OGG files directly in this folder or any subfolder to play them with the `*play` command.
- To sing along with **EPIC: The Musical**, create a subfolder called `epic_lyrics` and place one text file per song. Each file should be named exactly like the song title with a `.txt` extension.

Example:

```
localtracks/
└── epic_lyrics/
    └── The Horse and the Infant.txt
```

Each lyric file should contain one line per lyric. BloomBot will load the text and recite a few random lines when you trigger the `*drama` command.

These files are optional; if none are found BloomBot will still work but simply note that the lyrics are missing.
