# -*- coding: utf-8 -*-
# This will create a dist directory containing the executable file, all the data
# directories. All Libraries will be bundled in executable file.

# To build exe, python, pygame, and py2exe have to be installed. After
# building exe none of this libraries are needed.
#Please Note have a backup file in a different directory as if it crashes you 
#will loose it all!(I lost 6 months of work because I did not do this)
# 在终端中运行 python mysetup.py 即可 
 
try:
    from distutils.core import setup
    import py2exe, pygame
    from modulefinder import Module
    import glob, fnmatch
    import sys, os, shutil
    import operator
except ImportError, message:
    raise SystemExit,  "Unable to load module. %s" % message
 
#hack which fixes the pygame mixer and pygame font
origIsSystemDLL = py2exe.build_exe.isSystemDLL # save the orginal before we edit it
def isSystemDLL(pathname):
    # checks if the freetype and ogg dll files are being included
    if os.path.basename(pathname).lower() in ("libfreetype-6.dll", "libogg-0.dll","sdl_ttf.dll"): # "sdl_ttf.dll" added by arit.
            return 0
    return origIsSystemDLL(pathname) # return the orginal function
py2exe.build_exe.isSystemDLL = isSystemDLL # override the default function with this one
 
class pygame2exe(py2exe.build_exe.py2exe): #This hack make sure that pygame default font is copied: no need to modify code for specifying default font
    def copy_extensions(self, extensions):
        #Get pygame default font
        pygamedir = os.path.split(pygame.base.__file__)[0]
        pygame_default_font = os.path.join(pygamedir, pygame.font.get_default_font())
 
        #Add font to list of extension to be copied
        extensions.append(Module("pygame.font", pygame_default_font))
        py2exe.build_exe.py2exe.copy_extensions(self, extensions)
 
class BuildExe:
    def __init__(self):
        #Name of starting .py
        self.script = "main.py"
 
        #Name of program
        self.project_name = "ShootingPlanes"
 
        #Project url
        self.project_url = "about:none"
 
        #Version of program
        self.project_version = "1.0"
 
        #License of the program
        self.license = "MyApps License"
 
        #Auhor of program
        self.author_name = "Scott Zhang"
        self.author_email = "zcy.scott@outlook.com"
        self.copyright = "Copyright (c) 2016 Me."
 
        #Description
        self.project_description = "A small project to let me and my friends to have fun"
 
        #Icon file (None will use pygame default icon)
        self.icon_file = 'myPlane.ico'
 
        #Extra files/dirs copied to game
        self.extra_datas = []
 
        #Extra/excludes python modules
        self.extra_modules = []
        self.exclude_modules = ['AppKit', 'Carbon', 'Carbon.Files', 'Foundation', 'Numeric', 'OpenGL.GL', '__svn_version__', '_curses', '_imp', '_scproxy', '_sysconfigdata', 'backports.ssl_match_hostname', 'builtins', 'code_generators.genapi', 'code_generators.numpy_api', 'compat.long', 'configparser', 'copyreg', 'core.abs', 'core.max', 'core.min', 'core.round', 'dummy.Process', 'fcompiler.FCompiler', 'fcompiler.has_f90_header', 'fcompiler.is_f_file', 'genapi', 'html.entities', 'http.client', 'http.server', 'importlib.machinery', 'nose', 'nose.plugins', 'nose.plugins.base', 'nose.plugins.builtin', 'nose.plugins.errorclass', 'nose.util', 'numarray', 'numpy._build_utils.apple_accelerate', 'numpy.amax', 'numpy.amin', 'numpy.array', 'numpy.bool_', 'numpy.compat.asbytes', 'numpy.compat.asbytes_nested', 'numpy.compat.asstr', 'numpy.compat.basestring', 'numpy.compat.bytes', 'numpy.compat.integer_types', 'numpy.compat.isfileobj', 'numpy.compat.long', 'numpy.compat.open_latin1', 'numpy.compat.sixu', 'numpy.compat.unicode', 'numpy.core.Inf', 'numpy.core.absolute', 'numpy.core.add', 'numpy.core.all', 'numpy.core.amax', 'numpy.core.amin', 'numpy.core.any', 'numpy.core.arange', 'numpy.core.around', 'numpy.core.array', 'numpy.core.array_repr', 'numpy.core.asanyarray', 'numpy.core.asarray', 'numpy.core.atleast_1d', 'numpy.core.atleast_2d', 'numpy.core.atleast_3d', 'numpy.core.bitwise_and', 'numpy.core.bitwise_or', 'numpy.core.bitwise_xor', 'numpy.core.broadcast', 'numpy.core.cdouble', 'numpy.core.complexfloating', 'numpy.core.concatenate', 'numpy.core.conjugate', 'numpy.core.csingle', 'numpy.core.divide', 'numpy.core.dot', 'numpy.core.double', 'numpy.core.empty', 'numpy.core.empty_like', 'numpy.core.equal', 'numpy.core.errstate', 'numpy.core.fastCopyAndTranspose', 'numpy.core.finfo', 'numpy.core.float32', 'numpy.core.float64', 'numpy.core.float_', 'numpy.core.geterrobj', 'numpy.core.greater', 'numpy.core.greater_equal', 'numpy.core.hstack', 'numpy.core.iinfo', 'numpy.core.inexact', 'numpy.core.inf', 'numpy.core.intc', 'numpy.core.integer', 'numpy.core.intp', 'numpy.core.invert', 'numpy.core.isfinite', 'numpy.core.isinf', 'numpy.core.isnan', 'numpy.core.isscalar', 'numpy.core.left_shift', 'numpy.core.less', 'numpy.core.less_equal', 'numpy.core.linspace', 'numpy.core.longdouble', 'numpy.core.maximum', 'numpy.core.multiply', 'numpy.core.ndarray', 'numpy.core.newaxis', 'numpy.core.not_equal', 'numpy.core.number', 'numpy.core.object_', 'numpy.core.ones', 'numpy.core.power', 'numpy.core.product', 'numpy.core.ravel', 'numpy.core.remainder', 'numpy.core.reshape', 'numpy.core.result_type', 'numpy.core.right_shift', 'numpy.core.rollaxis', 'numpy.core.shape', 'numpy.core.signbit', 'numpy.core.sin', 'numpy.core.single', 'numpy.core.size', 'numpy.core.sqrt', 'numpy.core.subtract', 'numpy.core.sum', 'numpy.core.swapaxes', 'numpy.core.take', 'numpy.core.transpose', 'numpy.core.ufunc', 'numpy.core.vstack', 'numpy.core.zeros', 'numpy.deprecate', 'numpy.dtype', 'numpy.expand_dims', 'numpy.eye', 'numpy.histogramdd', 'numpy.integer', 'numpy.intp', 'numpy.iscomplexobj', 'numpy.lib.add_newdoc', 'numpy.lib.asfarray', 'numpy.lib.i0', 'numpy.lib.imag', 'numpy.lib.iscomplexobj', 'numpy.lib.real', 'numpy.lib.triu', 'numpy.linalg.eigvals', 'numpy.linalg.inv', 'numpy.linalg.lstsq', 'numpy.ma.MAError', 'numpy.ma.MaskedArray', 'numpy.ma.filled', 'numpy.ma.getdata', 'numpy.ma.getmaskarray', 'numpy.ma.make_mask_descr', 'numpy.ma.masked', 'numpy.ma.masked_array', 'numpy.ma.nomask', 'numpy.ndarray', 'numpy.recarray', 'numpy_api', 'numpy_distutils', 'numpy_distutils.command.build_flib', 'numpy_distutils.command.cpuinfo', 'numpy_distutils.cpuinfo', 'numpy_distutils.fcompiler', 'org.python.modules.posix.PosixModule', 'packaging.specifiers', 'packaging.version', 'queue', 'scipy', 'setuptools_svn', 'sitecustomize', 'testing.Tester', 'urllib.error', 'urllib.parse', 'urllib.request', 'usercustomize', 'win32com.gen_py', 'wincertstore', 'winreg', 'pygame.sdlmain_osx']
        # self.exclude_modules = []
        
        #DLL Excludes
        self.exclude_dll = ['MSVCP90.dll', 'numpy-atlas.dll', 'KERNEL32.dll', 'OLEAUT32.dll', \
        'USER32.dll', 'IMM32.dll', 'SHELL32.dll', 'COMDLG32.dll', \
        'COMCTL32.dll', 'ADVAPI32.dll', 'WS2_32.dll', 'GDI32.dll', 'WINMM.dll', 'ole32.dll', \
        'WINSPOOL.DRV', 'mfc90.dll', 'VERSION.dll']
        #python scripts (strings) to be included, seperated by a comma
        self.extra_scripts = []
 
        #Zip file name (None will bundle files in exe instead of zip file)
        self.zipfile_name = None
 
        #Dist directory
        self.dist_dir = 'dist'
 
    # Code from DistUtils tutorial at http://wiki.python.org/moin/Distutils/Tutorial
    # Originally borrowed from wxPython's setup and config files
    def opj(self, *args):
        path = os.path.join(*args)
        return os.path.normpath(path)
 
    def find_data_files(self, srcdir, *wildcards, **kw):
        # get a list of all files under the srcdir matching wildcards,
        # returned in a format to be used for install_data
        def walk_helper(arg, dirname, files):
            if '.svn' in dirname:
                return
            names = []
            lst, wildcards = arg
            for wc in wildcards:
                wc_name = self.opj(dirname, wc)
                for f in files:
                    filename = self.opj(dirname, f)
 
                    if fnmatch.fnmatch(filename, wc_name) and not os.path.isdir(filename):
                        names.append(filename)
            if names:
                lst.append( (dirname, names ) )
 
        file_list = []
        recursive = kw.get('recursive', True)
        if recursive:
            os.path.walk(srcdir, walk_helper, (file_list, wildcards))
        else:
            walk_helper((file_list, wildcards), \
                        srcdir, \
                        [os.path.basename(f) for f in glob.glob(self.opj(srcdir, '*'))])
        return file_list
 
    def run(self):
        if os.path.isdir(self.dist_dir): #Erase previous destination dir
            shutil.rmtree(self.dist_dir)
        
        #Use the default pygame icon, if none given
        if self.icon_file == None:
            path = os.path.split(pygame.__file__)[0]
            self.icon_file = os.path.join(path, 'pygame.ico')
 
        #List all data files to add
        extra_datas = []
        for data in self.extra_datas:
            if os.path.isdir(data):
                extra_datas.extend(self.find_data_files(data, '*'))
            else:
                extra_datas.append(('.', [data]))
        
        setup(
            cmdclass = {'py2exe': pygame2exe},
            version = self.project_version,
            description = self.project_description,
            name = self.project_name,
            url = self.project_url,
            author = self.author_name,
            author_email = self.author_email,
            license = self.license,
 
            # targets to build
            windows = [{
                'script': self.script,
                'icon_resources': [(1, "myPlane.ico")],
                'copyright': self.copyright
            }],
            options = {'py2exe': {'optimize': 2, 'bundle_files': 1, 'compressed': True, \
                                  'excludes': self.exclude_modules, 'packages': self.extra_modules, \
                                  'dll_excludes': self.exclude_dll, \
                                  'includes': self.extra_scripts} },
            zipfile = self.zipfile_name,
            data_files = extra_datas,
            dist_dir = self.dist_dir
            )
        
        if os.path.isdir('build'): #Clean up build dir
            shutil.rmtree('build')
 
if __name__ == '__main__':
    if operator.lt(len(sys.argv), 2):
        sys.argv.append('py2exe')
    BuildExe().run() #Run generation
    raw_input("Press any key to continue") #Pause to let user see that things ends 