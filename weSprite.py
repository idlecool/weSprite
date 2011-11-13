#!/usr/bin/python
"""
SYNOPSIS

    weSprite.py -h

DESCRIPTION

    A Python Script which manages CSS Sprites for a web project.

EXAMPLES

    TODO: 

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Shiv Deepak<shiv@interviewstreet.com>

VERSION

    v0.01    
"""
import os
import shutil
import pickle
import optparse

class Sprites(object):
    def __init__(self):
        self.sprites = {}

    def create(self, sprite):
        if self.sprites.has_key(sprite):
            print "Sprint already exists"
        else:
            self.sprites[sprite] = {'files': [],
                                    'file': {}}
            if not os.path.isdir("pool/%s" % sprite):
                os.makedirs("pool/%s" % sprite)
            print "Sprint %s added." % sprite

    def show_all(self):
        if len(self.sprites) == 0:
            print "No sprite found."
            
        else:
            print "\n".join(self.sprites.keys())

    def add_file(self, sprite, filename):
        if os.path.isfile(filename):
            filesuffix = os.path.split(filename)[1]
            try:
                if filesuffix not in self.sprites[sprite]["files"]:
                    shutil.copyfile(filename, "pool/%s/%s" % (sprite, filesuffix))                
                    self.sprites[sprite]['files'].append(filesuffix)
                    self.sprites[sprite]['file'][filesuffix] = {'commited': False,
                                                                }
                    print "File has been added to %s" % sprite
                else:
                    print "File %s already exists in %s sprite" % (filename, sprite)
                    
            except KeyError as error:
                print "%s named sprite doesnot exist" % sprite
        else:
            print "'%s' doesnot exist or its not a file" % filename

    def show_details(self, sprite):
        if self.sprites.has_key(sprite):
            if len(self.sprites[sprite]["files"]) == 0:
                print "No files to the sprite %s yet been added" % sprite
            else:
                for sfile in self.sprites[sprite]['files']:
                    if not self.sprites[sprite]['file'][sfile]['commited']:
                        asterix = "*"
                    else:
                        asterix = " "
                    print "%s %s" % (asterix, sfile)

        else:
            print "%s sprite does not exist" % sprite


    def show_tree(self):
        if len(self.sprites) == 0:
            print "No sprite has been created yet"

        for sprite in self.sprites:
            print "Sprite: %s :" % sprite
            if len(self.sprites[sprite]['files']) == 0:
                print "\t<Empty>"
            else:
                for sfile in self.sprites[sprite]['files']:
                    # check if commited
                    if not self.sprites[sprite]['file'][sfile]['committed']:
                        asterix = "*"
                    else:
                        asterix = " "
                    print "\t%s %s" % (asterix, sfile)

    def remove_file(self, sprite, filename):
        if self.sprites.has_key(sprite):
            if filename in self.sprites[sprite]['files']:
                sfile = filename
            else:
                filesuffix = os.path.split(filename)[1]
                if filesuffix in self.sprites[sprite]['files']:
                    sfile = filesuffix
                else:
                    "%s doesnt exist in the sprite %s" % (filename, sprite)
                    return
            
            if self.sprites[sprite]['file'][sfile]["committed"]:
                print "Commited File cannot be removed"
            else:
                os.remove('pool/%s/%s' % (sprite,sfile))
                self.sprites[sprite]['files'].remove(sfile)
                del self.sprites[sprite]['file'][sfile]
                print "file %s has been removed from sprite %s" % (filename, sprite)
        else:
            print "Sprite %s doesnt exist" % sprite

    def generate_sprite(self, sprite, quiet, link):
        
        inputfiles = map(lambda m: "pool/%s/%s" % (sprite, m), self.sprites[sprite]['files'])
        outputfile_img = "pool/%s.png" % sprite
        outputfile_css = "pool/%s.css" % sprite
        exit_status = os.system("convert %s -append PNG8:%s" % (" ".join(inputfiles), outputfile_img))

        if exit_status != 0:
            print "There was a problem with ImageMagic convert. Make sure it is been installed"
            exit(1)

        if not link:
            link = "/recruit/includes/images/sprites"

        css_content = ""
        hcord = 0
        wcord = 0
        for sfile in self.sprites[sprite]['files']:
            self.sprites[sprite]['file'][sfile]['committed'] = True

            w, h = os.popen('identify -format "%g - %f\n" pool/'+ sprite +'/'+ sfile).read().split("-")[0].split("+")[0].split("x")

            hcord = hcord - int(h)

            classname = "%s-%s" % (sprite, sfile[:sfile.rfind(".")].replace(".", "-").replace("_", "-"))
            css_content = """
.%(class)s {
width: %(width)spx;
height: %(height)spx;
background: url('%(spritefile)s') %(wcord)spx %(hcord)spx;
}
""" % {'class': classname,
        'width': w,
        'height': h,
        'spritefile': "%s/%s.png" % (link, sprite),
        'wcord': wcord,
        'hcord': hcord,
        } + css_content

        if not quiet:
            print css_content
        f = open(outputfile_css, "w")
        f.write(css_content)
        f.close()

if __name__=="__main__":
     parser = optparse.OptionParser("usage: %prog [options]")

     parser.add_option("-s", "--show-all",
                       action="store_true", dest="show_all",
                       help="Show all sprites available")

     parser.add_option("-q", "--quiet",
                       action="store_true", dest="quiet",
                       help="No verbose")

     parser.add_option("-r", "--reset",
                       action="store_true", dest="reset",
                       help="Reset the weSprite data structure")

     parser.add_option("-c", "--create",
                       action="store", dest="create",
                       help="create a new sprite")

     parser.add_option("-u", "--use",
                       action="store", dest="use",
                       help="use sprite")

     parser.add_option("-l", "--link",
                       action="store", dest="link",
                       help="prefix link for the location of the image file")

     parser.add_option("-a", "--add",
                       action="store", dest="add",
                       help="add file to sprite")

     parser.add_option("-d", "--details",
                       action="store", dest="details",
                       help="show details of a sprite")

     parser.add_option("-t", "--tree",
                       action="store_true", dest="tree",
                       help="show the entire sprites hierarchy")

     parser.add_option("-g", "--generate",
                       action="store", dest="generate",
                       help="generate image and css for the given sprite")

     parser.add_option("-p", "--purge",
                       action="store", dest="purge",
                       help="Purges file from a given Sprite")
     

     (options, args) = parser.parse_args()
     if len(args) != 0:
         parser.error("incorrect number of arguments")

     try:
         data = pickle.load(open("data.pickle", "rb"))
     except(IOError):
         if options.reset:
             data = Sprites()
             try:
                 shutil.rmtree("pool/")
             except:
                 pass
             os.makedirs("pool")
         else:
             print "Running weSprite for the first time"
             print "To create the data structure use -r flag"
             exit(1)
     else:
         if options.reset:
             print "You cannot reset the data structure without deleting \nthe existing one from the file system."
             exit(1)

     if options.show_all:
         data.show_all()

     if options.create:
         data.create(options.create)

     if options.add and options.use:
         data.add_file(options.use, options.add)

     else:
         if options.add:
             print "-a flag should come with -u flag"

     if options.purge and options.use:
         data.remove_file(options.use, options.purge)

     else:
         if options.purge:
             print "-p flag should come with -u flag"

     if options.details:
         data.show_details(options.details)
         
     if options.tree:
         data.show_tree()

     if options.generate:
         data.generate_sprite(options.generate, options.quiet, options.link)

     pickle.dump(data, open("data.pickle", "wb"))

