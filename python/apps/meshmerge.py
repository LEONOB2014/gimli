#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This program is part of pygimli
Visit http://www.resistivity.net for further information or the latest version.
"""

import sys, os

import pygimli as g

def main( argv ):
    from optparse import OptionParser

    parser = OptionParser( "usage: %prog [options] mesh1 mesh2" )
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true"
                            , help="be verbose", default=False )
    parser.add_option("-o", "--output", dest="outFileName", default='merge'
                            , help="Filename for the resulting mesh."
                            , metavar="File" )
    
    (options, args) = parser.parse_args()

    if len( args ) < 2:
        parser.print_help()
        print "Please add a mesh or model name."
        sys.exit( 2 )
    else:
        meshname1 = args[ 0 ];
        meshname2 = args[ 1 ];

    (outfileBody, fileExtension) = os.path.splitext( options.outFileName )
    
    m1 = g.Mesh( meshname1 )
    m2 = g.Mesh( meshname2 )

    if options.verbose:
        print meshname1, m1
        print meshname2, m2

    mesh = g.Mesh( m1 )

    for c in m2.cells():
        mesh.copyCell( c )

    for key in mesh.exportDataMap().keys():
        d = mesh.exportDataMap()[ key ]
        print d
        d.resize( mesh.cellCount() )
        d.setVal( m1.exportDataMap()[ key ], 0, m1.cellCount() )
        d.setVal( m2.exportDataMap()[ key ], m1.cellCount(), m1.cellCount() + m2.cellCount() )
        mesh.addExportData( key, d )

    print mesh
    if options.verbose:
        print "write bms: ", outfileBody + ".bms" 

    if outfileBody.find( '.vtk' ):
        mesh.exportVTK( outfileBody )
    else:
        mesh.saveBinaryV2( outfileBody )
    

if __name__ == "__main__":
    main( sys.argv[ 1: ] )