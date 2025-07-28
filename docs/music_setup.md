# Music Setup

BloomBot and the `music_cog.py` rely on FFmpeg for audio playback. Install it using your package manager:

```bash
# Debian/Ubuntu
sudo apt-get install ffmpeg

# macOS (Homebrew)
brew install ffmpeg
```

For advanced playback via Lavalink, make sure a Lavalink server is running and update the connection details inside `media_player.py` if needed.

Place optional audio files in the [`localtracks`](../localtracks) folder. BloomBot looks for lyrics in `localtracks/epic_lyrics` when you use `*drama`.
