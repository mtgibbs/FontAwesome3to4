import os, fnmatch, fileinput, shutil, re, sys, traceback

TEMP_FILE_NAME = 'file.tmp'
CONFIG_FILE_NAME = 'fontawesome3to4.config'
ICON_TAG_REGEX = re.compile('<i.*class=".*".*>')

newSyntax = {' icon-': ' fa-', '"icon-': '"fa-', '.icon-': '.fa-', '\'icon-': '\'fa-', 'icon-fixed-width': 'fa-fw', 'icon-large': 'fa-lg', 'icons-ul': 'fa-ul'}
iconNames = {'share': 'share-square-o', 'hand-down': 'hand-o-down', 'circle-arrow-down': 'arrow-circle-down', 'download': 'arrow-circle-o-down',
 'youtube-sign': 'youtube-square', 'expand': 'caret-square-o-right', 'reorder': 'bars', 'download-alt': 'download', 'frown': 'frown-o',
 'check-sign': 'check-square', 'chevron-sign-right': 'chevron-circle-right', 'ban-circle': 'ban',
 'upload': 'arrow-circle-o-up', 'signin': 'sign-in', 'warning-sign': 'exclamation-triangle',
 'circle-blank': 'circle-o', 'beaker': 'flask', 'star-empty': 'star-o', 'folder-close-alt': 'folder-o',
 'facetime-video': 'video-camera', 'signout': 'sign-out', 'indent-left': 'outdent', 'share-sign': 'share-square',
 'circle-arrow-right': 'arrow-circle-right', 'sort-by-attributes': 'sort-amount-asc', 'off': 'power-off',
 'chevron-sign-down': 'chevron-circle-down', 'bitbucket-sign': 'bitbucket-square', 'bar-chart': 'bar-chart-o',
 'chevron-sign-up': 'chevron-circle-up', 'phone-sign': 'phone-square', 'hdd': 'hdd-o (4.0.1)',
 'minus-sign-alt': 'minus-square', 'file-alt': 'file-o', 'ok-sign': 'check-circle', 'chevron-sign-left': 'chevron-circle-left',
 'edit-sign': 'pencil-square', 'xing-sign': 'xing-square', 'info-sign': 'info-circle', 'bell': 'bell-o',
 'sort-down': 'sort-asc', 'double-angle-left': 'angle-double-left', 'sun': 'sun-o', 'meh': 'meh-o', 'heart-empty': 'heart-o',
 'dashboard': 'tachometer', 'edit': 'pencil-square-o', 'plus-sign-alt': 'plus-square', 'remove-sign': 'times-circle',
 'folder-open-alt': 'folder-open-o', 'exclamation-sign': 'exclamation-circle', 'moon': 'moon-o',
 'sort-by-order-alt': 'sort-numeric-desc', 'circle-arrow-up': 'arrow-circle-up', 'google-plus-sign': 'google-plus-square',
 'eye-open': 'eye', 'play-sign': 'play-circle', 'thumbs-up-alt': 'thumbs-o-up', 'unlink': 'chain-broken', 'zoom-in': 'search-plus',
 'question-sign': 'question-circle', 'sort-up': 'sort-desc', 'thumbs-down-alt': 'thumbs-o-down', 'time': 'clock-o',
 'minus-sign': 'minus-circle', 'ok': 'check', 'keyboard': 'keyboard-o', 'github-sign': 'github-square', 'hand-right': 'hand-o-right',
 'food': 'cutlery', 'bookmark-empty': 'bookmark-o', 'check-empty': 'square-o',
 'paper-clip': 'paperclip', 'tumblr-sign': 'tumblr-square', 'sort-by-order': 'sort-numeric-asc', 'copy': 'files-o',
 'double-angle-up': 'angle-double-up', 'flag-alt': 'flag-o', 'collapse-alt': 'collapse-o', 'remove': 'times',
 'star-half-empty': 'star-half-o', 'envelope-alt': 'envelope-o', 'check': 'check-square-o', 'zoom-out': 'search-minus',
 'collapse-top': 'caret-square-o-up', 'microphone-off': 'microphone-slash', 'twitter-sign': 'twitter-square',
 'calendar-empty': 'calendar-o', 'comments-alt': 'comments-o', 'legal': 'gavel', 'hand-left': 'hand-o-left',
 'cut': 'scissors', 'picture': 'picture-o', 'sort-by-alphabet-alt': 'sort-alpha-desc', 'plus-sign': 'plus-circle',
 'expand-alt': 'expand-o', 'file-text-alt': 'file-text-o', 'check-minus': 'minus-square-o', 'upload-alt': 'upload',
 'collapse': 'caret-square-o-down', 'sign-blank': 'square', 'sort-by-attributes-alt': 'sort-amount-desc',
 'screenshot': 'crosshairs', 'indent-right': 'indent', 'pushpin': 'thumb-tack', 'save': 'floppy-o',
 'play-circle': 'play-circle-o', 'facebook-sign': 'facebook-square', 'pinterest-sign': 'pinterest-square',
 'h-sign': 'h-square', 'external-link-sign': 'external-link-square', 'circle-arrow-left': 'arrow-circle-left',
 'comment-alt': 'comment-o', 'rss-sign':'rss-square', 'unlock-alt': 'unlock-o', 'folder-close': 'folder',
 'smile': 'smile-o', 'lemon': 'lemon-o', 'bell-alt': 'bell', 'hand-up': 'hand-o-up', 'sort-by-alphabet': 'sort-alpha-asc',
 'share-alt': 'share', 'mobile-phone': 'mobile', 'lightbulb': 'lightbulb-o', 'ok-circle': 'check-circle-o', 'eye-close': 'eye-slash',
 'remove-circle': 'times-circle-o', 'double-angle-down': 'angle-double-down', 'double-angle-right': 'angle-double-right',
 'trash': 'trash-o', 'linkedin-sign': 'linkedin-square', 'paste': 'clipboard'}

global projects
global extensions
global excludeFilters

def findfiles (path, filter):
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield os.path.join(root, file)

def main():

	projects = []
	extensions = []
	excludeFilters = []

	with open(CONFIG_FILE_NAME, 'rt') as configin:
		for line in configin:
			if line != '':
				tokens = line.split('=')
				
				if tokens[0] == 'PROJECT_PATHS':
					projects = [item.strip().rstrip('\r\n') for item in tokens[1].split(',')]
				elif tokens[0] == 'FILE_EXTENSIONS':
					extensions = [item.strip().rstrip('\r\n') for item in tokens[1].split(',')]
				elif tokens[0] == 'EXCLUDE_FILTERS':
					excludeFilters = [item.strip().rstrip('\r\n') for item in tokens[1].split(',')]

	for project in projects:
		for extension in extensions:
			for textfile in findfiles(project , extension):
				
				try:
				
					isExclude = False
					for excludeFilter in excludeFilters:
						isExclude = excludeFilter in textfile
						if isExclude:
							break
					
					if isExclude:
						continue

					filechanged = False

					with open(TEMP_FILE_NAME, 'wt') as fout:
						with open(textfile, 'rt') as fin:
							for line in fin:
								linechanged = False
								for key, value in iconNames.items():
									if key not in line:
										continue
									else:
										line = line.replace('icon-' + key, 'icon-' + value)
										linechanged = True
									
								for key, value in newSyntax.items():
									if key not in line or '.png' in line:
										continue
									else:
										line = line.replace(key, value)
										linechanged = True
									
								iconTags = re.findall(ICON_TAG_REGEX, line)
								iconReplacements = {}
								
								for iconTag in iconTags:
									if 'fa-' in iconTag:
										iconReplacements[iconTag] = iconTag.replace('class="', 'class="fa ')
								
								for key, value in iconReplacements.items():
									line = line.replace(key, value)
									linechanged = True
									
								if linechanged:
									filechanged = True

								fout.write(line)
								
							if filechanged:
								print(textfile + '  has been modified')
								
					shutil.copyfile(TEMP_FILE_NAME, textfile)			
					os.remove(TEMP_FILE_NAME)
				except Exception:
					print('Error occured while processing the file: ' + textfile)
					print(traceback.format_exc())
	
if __name__=='__main__':main()