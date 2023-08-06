## A simple wrapper for mediainfo tool

#### Prerequisites

This tool needs mediainfo to be installed inorder to work properly.

On Ubuntu/Debian:

```
sudo apt install mediainfo
```

On Mac:

```
brew install mediainfo
```

#### Usage

To get all available info about a video file. It works with all media types.

```
mediaquery --file="some video.mp4" track --type={General/Audio/Video} --list-keys

```

To get info about one particular key:

```
mediaquery --file="some video.mp4" track --type={General/Audio/Video} --key=Duration

```



