# DN PDF Downloader
Download a PDF issue of Dagens Nyheter

## Usage
Build the image...
```docker
docker build -t dn_downloader .
```

... and run it
```docker
docker run --rm -it \
    -v TARGET_DIRECTORY:/downloads
    -v /etc/localtime:/etc/localtime:ro
    -e TZ=TIMEZONE
    dn_downloader [-h] [-d DATE] -u USERNAME -p PASSWORD [path]
```

```
positional arguments:
    path                    Path to download directory with or without a filename. Defaults to '/downloads'.

optional arguments:
    -h, --help              Show this help message and exit
    -d, --date DATE         The date of the issue in the format 'YYYYMMDD'
    -u, --username USERNAME Username (registered e-mail address) on dn.se
    -p, --password PASSWORD Password on dn.se
```

When running set environmental variable `TZ` and mount `/etc/localtime` as read-only to ensure that the most current issue are downloaded when not specifying which issue to download



