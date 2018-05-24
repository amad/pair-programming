import glob
import re


def getTitles():
    titles = {}
    for file_path in glob.glob('chapters/*.md'):
        titles[file_path] = []
        with open(file_path, 'r') as file:
            titles[file_path].append(re.findall('(?<=# ).*', file.read()))

    return titles


def slugify(string):
    return re.sub(r'[\?\+\/]', '', re.sub(r'\s+', '-', string.lower()))


def parseChapterIndex(index, sections, chapter):
    output = "{0}. [{1}]({2})\n".format(index, sections[0], chapter)
    output += ''.join(map(
        (lambda s: "    * [{0}]({1}#{2})\n".format(s, chapter, slugify(s))),
        sections[1:]
    ))

    return output


def updateReadme(newIndex):
    with open('README.md', 'r') as read:
        readme = read.read()

    newReadme = readme[0: readme.find('## Index') + 10] + newIndex

    with open('README.md', 'w') as file:
        file.write(newReadme)


def main():
    titles = getTitles()

    newIndex = ""
    for index, (chapter, items) in enumerate(sorted(titles.iteritems())):
        newIndex += parseChapterIndex(index+1, items[0], chapter)

    return updateReadme(newIndex)


if __name__ == '__main__':
    main()
