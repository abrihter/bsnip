# bsnip V1.1.0 #
Small CLI snippet manager class, allowing users to manage CLI snippets and execute code with just short commands, calling snippets by IDs

Project also include sample UI class

### Instalation ###
- Clone this repo
- Make app.py executable ```chmod +x app.py```
- Create symlink ```ln -s /path/to/file/app.py /usr/bin/bsnip```

### Features ###
- Independent class for controlling snippets
- Simple UI template
- Save snippets to cloud (using [jsonstorage.net API wrapper](https://github.com/abrihter/jsonstorage-net-api-wrapper))

### Help ###
```
python3 app.py --help
```

### Version ###
```
python3 app.py --version
```
