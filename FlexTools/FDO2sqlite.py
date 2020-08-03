# -*- coding: utf-8 -*-
from timeit import default_timer as timer
start = timer()
import Version
import traceback
try:
    import FTPaths
    from FLExBaseInit import FWAppVersion    

#TODO convert these error messageboxes to Gooey messageboxes
except EnvironmentError, e:
    # # EnvironmentError is used to communicate a known situation that can be handled,
    # # typically with a restart.
    # MessageBox.Show(e.message,
                    # "FLExTools: Configuring",
                    # MessageBoxButtons.OK,
                    # MessageBoxIcon.Information)
    sys.exit(2)     # Signal a restart
                    
except Exception, e:
    # MessageBox.Show("Error interfacing with Fieldworks:\n%s\n(This version of FLExTools supports Fieldworks versions %s - %s.)\nSee error.log for more details."
                    # % (e.message, Version.MinFWVersion, Version.MaxFWVersion),
                    # "FLExTools: Fatal Error",
                    # MessageBoxButtons.OK,
                    # MessageBoxIcon.Exclamation)
    print "Fatal exception during imports:\n%s" % traceback.format_exc()
    print "FLExTools %s" % Version.number
    sys.exit(1)
# ------------------------------------------------------------------
from FLExDBAccess import FLExDBAccess                            
from setuptables import foo
#----------------------------
end = timer()
loadtime = (end - start)
print('loadtime is: %s' % loadtime)

if __name__ == "__main__":

    print('FWAppVersion is: %s' % FWAppVersion)
    def sql():

        databases = ['RuthTestFLExTools']
        for database in databases:
            DB = FLExDBAccess()
            DB.OpenDatabase(database)
            print("DB is: %s" % DB)        
            # setup database tables and populate them
            foo(DB)        

    # main()
    sql()