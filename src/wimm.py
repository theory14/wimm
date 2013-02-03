#!/usr/bin/python
#
# Copyright (C) 2012 Chris Gordon
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''
What's In My Music (wimm)  

Displays the various ID3 v2 tag frames in an mp3 file.
'''

import eyeD3
import os
import fnmatch
import argparse
import sys

class MP3File(object):
    
    def __init__(self):
        self.myFile = ''
        self.tag = eyeD3.Tag()
    
    def setFile(self, aFile):
        self.myFile = aFile
    
    def showData(self):
        try:
            if (self.tag.link(self.myFile, eyeD3.ID3_V2)):
                print self.myFile, 'Contains the following Frames:'
                for frame in self.tag.frames:
                    if frame.__class__.__name__ == 'TextFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.text
                    elif frame.__class__.__name__ == 'UserTextFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.description, frame.text
                    elif  frame.__class__.__name__ == 'DateFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.date_str
                    elif  frame.__class__.__name__ == 'URLFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.url
                    elif  frame.__class__.__name__ == 'UserURLFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.url
                    elif frame.__class__.__name__ == 'CommentFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.description, frame.text
                    elif frame.__class__.__name__ == 'LyricsFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.description, frame.lyrics
                    elif frame.__class__.__name__ == 'ImageFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.description
                    elif frame.__class__.__name__ == 'PlayCountFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.count
                    elif frame.__class__.__name__ == 'UniqueFileIDFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.id, frame.owner_id
                    elif frame.__class__.__name__ == 'UknownFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')', ' : ', frame.data
                    elif frame.__class__.__name__ == 'MusicCDIdFrame':
                        print frame.header.id, '(',  frame.__class__.__name__, ')',' : ', frame.toc
                    else:
                        print frame.__class__.__name__, "No Other Data"                       
        except Exception as e:
            print >> sys.stderr, 'Problem with ID3_V2 tags in file:  ', self.myFile
            print >> sys.stderr, e
            
class FileList(object):
    '''Create a list of files to clean.  If pass a single file, it will hold
    just a single file.  If a directory is passed, it will recursive traverse
    the directory and create a list of all of the files.  In either case, it will
    only return files that match the given pattern (default to *.mp3)'''

    def __init__(self):
        self.fileList = []
        self.pattern = '*.mp3'

    def setPattern(self, pat):
        self.pattern = pat
        
    def getPattern(self):
        return self.pattern
    
    def getList(self):
        return self.fileList

    def appendToList(self, filePath):
        '''Add a file or directory contents (recursively) to the list.'''
        if os.path.isdir(filePath):
            self._appendToListFromDir(filePath)
        elif os.path.isfile(filePath):
            self._appendToListFromFile(filePath)
        else:
            return
    
    def _appendToListFromDir(self, path):
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, self.pattern):
                self.fileList.append(os.path.join(root, filename))
    
    def _appendToListFromFile(self, myfile):
        if fnmatch.fnmatch(myfile, self.pattern):
            self.fileList.append(myfile)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Display the ID3 v2 tags in an mp3 file.")
    parser.add_argument('file', 
                    help="The path to the files that are to be cleaned. This can be directories or specific files. Multiple items may be supplied.",
                    type=str, nargs='+')
    args = parser.parse_args()
    
    myFiles = FileList()
    
    for item in args.file:
        myFiles.appendToList(item)
        
    for aFile in myFiles.getList():
        song = MP3File()
        song.setFile(aFile)
        song.showData()
        print ''
    