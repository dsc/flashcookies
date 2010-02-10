#!/usr/bin/env python
# encoding: utf-8
__author__    = 'Dave Schoonover <dsc@less.ly>'
__date__      = '2009-12-30'
__license__   = 'MIT'
__version__   = (0, 0, 1)

import sys, platform, os, os.path, re
import json, yaml
from glob import glob

import pyamf, pyamf.sol


COOKIES_PATH = {
    'darwin'  : '/Users/{username}/Library/Preferences/Macromedia/Flash Player/#SharedObjects',
    'linux'   : '/home/{username}/.macromedia/Flash_Player/#SharedObjects',
    'windows' : 'C:\\Documents and Settings\\{username}\\Application Data\\Macromedia\\Flash Player\\#SharedObjects\\'
}[ platform.system().lower() ]
MD_PAT = re.compile( r'(?P<hash>[^/]+)/(?P<domain>[^/]+)(?P<path>.*/)(?P<name>[^\.]+)\.sol$' )


## Encoding

class SOLJsonEncoder(json.JSONEncoder):
    
    def default(self, o):
        if o == pyamf.Undefined:
            return None
        elif isinstance(o, pyamf.MixedArray):
            return list(o.values())
        elif isinstance(o, (pyamf.ASObject, pyamf.sol.SOL)):
            return dict(o)
        else:
            return json.JSONEncoder.default(self, o)
    
    # Feh, pyamf.MixedArray counts as a dict
    def _iterencode_dict(self, o, markers):
        sup = super(SOLJsonEncoder, self)
        if isinstance(o, pyamf.MixedArray):
            return sup._iterencode_list(list(o.values()), markers)
        # elif isinstance(o, (pyamf.ASObject, pyamf.sol.SOL)):
        else:
            return sup._iterencode_dict(dict(o), markers)

class SOLYamlEncoder(yaml.dumper.Dumper):
    
    def represent_data(self, o):
        if isinstance(o, unicode):
            o = str(o)
        elif o == pyamf.Undefined:
            o = None
        elif isinstance(o, pyamf.MixedArray):
            o = list(o.values())
        elif isinstance(o, (pyamf.ASObject, pyamf.sol.SOL)):
            o = dict(o)
        return super(SOLYamlEncoder, self).represent_data(o)
    
    def represent_unicode(self, s):
        return str(s)


class FlashCookies(object):
    username = os.getlogin()
    
    
    def __init__(self, *args, **options):
        self.args = args
        self.options = options
        self.cookies_path = COOKIES_PATH.format(username=self.username)
    
    def find(self, domain, name='*', path='', metadata=False):
        filename = '%s.sol' % name
        filepath = os.path.join(path, filename) if path else filename
        
        files = glob(os.path.join(self.cookies_path, '*', domain, filepath))
        for f in files:
            so = pyamf.sol.load(f)
            if metadata:
                md = self._parsePath(f)
                md['data'] = so
                yield md
            else:
                yield so
    
    def _parsePath(self, f):
        rel = os.path.relpath(f, self.cookies_path)
        md = {
            'relpath'  : rel,
            'fullpath' : f,
        }
        m = MD_PAT.match(rel)
        if m:
            md.update(m.groupdict())
        return md
    
    def inspect(self, domain, name='*', path='', metadata=False, format='json', **kv):
        files = self.find(domain, name, path, metadata)
        if format == 'list':
            for md in files:
                print md['relpath']
        elif format == 'json':
            json.dump(list(files), sys.stdout, cls=SOLJsonEncoder)
        elif format == 'yaml':
            yaml.dump_all(list(files), sys.stdout, default_flow_style=False, Dumper=SOLYamlEncoder)
        else:
            raise ValueError('Unknown output format: "%s"' % format)



def main():
    from optparse import OptionParser

    parser = OptionParser(
        usage   = 'usage: %prog [options] domain [name [path]]', 
        version = '%prog'+" %i.%i.%i" % __version__)
    parser.add_option("-f", "--format", default='json', choices=('list', 'json', 'yaml',), type='choice',
        help="Output format: list | json | yaml [default: %default]")
    parser.add_option("-l", "--list", default=False, action="store_true",
        help="Lists all matching sol files; synonym for --format list.")
    parser.add_option("-m", "--metadata", default=False, action="store_true", 
        help="Displays metadata about each file. [default: %default]")
    (options, args) = parser.parse_args()
    
    if not args:
        parser.error("Must specify a domain pattern!")
    
    if options.list:
        options.format = 'list'
    
    f = FlashCookies()
    f.inspect(*args, **options.__dict__)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
