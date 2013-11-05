##Index

* [Usage] (#usage)
* [Configuration] (#usage)

## Configuration

Set your parameters in the fontawesome3to4.config file.

> Example:

```txt
PROJECT_PATHS=C:\path\to\project
FILE_EXTENSIONS=*.aspx,*.css,*.cs,*.ascx,*.js,*.html,*.java
EXCLUDE_FILTERS=font-awesome, Generated., Designer., jquery, jqplot
```

Each parameter can be a comma-delimited list.

####PROJECT_PATHS

The list of folders you wish to run the script against.  You can specify the granularity you want by only including applicable folders in your project.  The script will recursively walk into subfolders.

####FILE_EXTENSIONS

The list of files you wish to look in.  Can be wildcard or specific.

#### EXCLUDE_FILTERS

The list of any string you wish to exclude from being modified.  This is so you don't have to worry about the script going in and changing jQuery or some other library that may have 'icon-' classes that do not belong to font awesome.



## Usage

Once you have configured the file, just run the script!

```bash
   $>:python fontawesome3to4.py
```

