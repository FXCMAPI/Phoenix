#---------------------------------------------------------------------------
# Name:        etg/defs.py
# Author:      Robin Dunn
#
# Created:     19-Nov-2010
# Copyright:   (c) 2013 by Total Control Software
# License:     wxWindows License
#---------------------------------------------------------------------------

import sys

import etgtools
import etgtools.tweaker_tools as tools

PACKAGE   = "wx"   
MODULE    = "_core"
NAME      = "defs"   # Base name of the file to generate to for this script
DOCSTRING = ""

# The classes and/or the basename of the Doxygen XML files to be processed by
# this script. 
ITEMS  = [ 'defs_8h.xml' ]    
    
#---------------------------------------------------------------------------

def run():
    # Parse the XML file(s) building a collection of Extractor objects
    module = etgtools.ModuleDef(PACKAGE, MODULE, NAME, DOCSTRING,
                                check4unittest=False)
    etgtools.parseDoxyXML(module, ITEMS)
    module.check4unittest = False
    
    #-----------------------------------------------------------------
    # Tweak the parsed meta objects in the module object as needed for
    # customizing the generated code and docstrings.
        
    # tweaks for defs.h to help SIP understand the types better
    module.find('wxInt16').type = 'short'
    module.find('wxInt64').type = 'long long'
    module.find('wxUint64').type = 'unsigned long long'
    
    # TODO: Find a way to represent these types such that they work in either
    # 32bit or 64bit compiles. Switching them here works okay if the Python
    # running this etg code to generate the wrappers is the same one we are
    # building for, however we want to be able to provide pregenerated code
    # that will work on all (supported) platforms and architectures.
    # Until I can come up with a better idea this will have to do.
    td = module.find('wxUIntPtr')
    if sys.maxsize > 2**32:
        module.find('wxIntPtr').type =  'long long'          
        module.find('wxUIntPtr').type = 'unsigned long long' 
        module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned long long', name='size_t'))
    else:
        module.find('wxIntPtr').type =  'long'               
        module.find('wxUIntPtr').type = 'unsigned long'      
        module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned long', name='size_t'))
        
        
    # Correct the types for these as their values are outside the range of int
    module.find('wxUINT32_MAX').type = 'long'
    module.find('wxINT64_MIN').type = 'long long'
    module.find('wxINT64_MAX').type = 'long long'
    module.find('wxUINT64_MAX').type = 'unsigned long long'
    module.find('wxCANCEL_DEFAULT').type = 'unsigned long'
    module.find('wxWINDOW_STYLE_MASK').type = 'unsigned long'
    module.find('wxVSCROLL').type = 'unsigned long'

    module.find('wxInt8').pyInt = True
    module.find('wxUint8').pyInt = True
    module.find('wxByte').pyInt = True
    
    module.find('wxDELETE').ignore()
    module.find('wxDELETEA').ignore()
    module.find('wxSwap').ignore()
    module.find('wxVaCopy').ignore()
    
    # Add some typedefs for basic wx types and others so the backend
    # generator knows what they are
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxUChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='wchar_t', name='wxChar'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='long', name='time_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='long long', name='wxFileOffset'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='SIP_SSIZE_T', name='ssize_t'))
    module.insertItemAfter(td, etgtools.TypedefDef(type='unsigned char', name='byte', pyInt=True))
    

    
    # Forward declarations for classes that are referenced but not defined
    # yet. 
    # 
    # TODO: Remove these when the classes are added for real.
    # TODO: Add these classes for real :-)
    module.insertItem(0, etgtools.WigCode("""\
        // forward declarations
        class wxPalette;
        class wxExecuteEnv;
        """))
    
   
    # Add some code for getting the version numbers
    module.addCppCode("""
        #include <wx/version.h>
        const int MAJOR_VERSION = wxMAJOR_VERSION;
        const int MINOR_VERSION = wxMINOR_VERSION;           
        const int RELEASE_NUMBER = wxRELEASE_NUMBER;     
        """)
    module.addItem(etgtools.WigCode("""
        const int MAJOR_VERSION;
        const int MINOR_VERSION;
        const int RELEASE_NUMBER;
        """))

    module.addPyCode("BG_STYLE_CUSTOM = BG_STYLE_PAINT")
    module.addItem(etgtools.DefineDef(name='wxADJUST_MINSIZE', value='0'))
    

    #-----------------------------------------------------------------
    tools.doCommonTweaks(module)
    tools.runGenerators(module)
    
    
    
#---------------------------------------------------------------------------
if __name__ == '__main__':
    run()

