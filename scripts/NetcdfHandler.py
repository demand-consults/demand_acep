class PsiNetcdf():
    import netCDF4
    import matplotlib as ply
    

    def __init__(self,cdf):
        """
        :param cdf: a netcdf object from Netcdf4 library
        """
        self.cdf = cdf
        self.variables = ""
        self.global_attributes = ""
        self.dimensions =""
    def previewNetcdf(self):
        '''
         outputs dimensions, variables and their attribute information.
        The information is similar to that of NCAR's ncdump utility.
        '''
        # NetCDF global attributes
        attrs = self.cdf.ncattrs()
        print("Global Attributes:")
        for attr in attrs:
            print('\t%s:' % attr, repr(self.cdf.getncattr(attr)))
        dims = [dim for dim in self.cdf.dimensions]  # list of nc dimensions
        # Dimension shape information.
        print("NetCDF dimension information:")
        for dim in dims:
            print("\tName:", dim)
            print("\t\tsize:", len(self.cdf.dimensions[dim]))
            self.print_attr(dim)
        # Variable information.
        vars = [var for var in self.cdf.variables]  # list of nc variables
        print("NetCDF variable information:")
        for var in vars:
            if var not in dims:
                print('\tName:', var)
                print("\t\tdimensions:", self.cdf.variables[var].dimensions)
                print("\t\tsize:", self.cdf.variables[var].size)
                self.print_attr(var)

        return

    def print_attr(self, key):
        """
        Prints the NetCDF file attributes for a given key
        Parameters
        ----------
        key : unicode
            a valid netCDF4.Dataset.variables key
        """
        try:
            print("\t\ttype:", repr(self.cdf.variables[key].dtype))
            for ncattr in self.cdf.variables[key].ncattrs():
                print('\t\t%s:' % ncattr, \
                      repr(self.cdf.variables[key].getncattr(ncattr)))
        except KeyError:
            print("\t\tWARNING: %s does not contain variable attributes" % key)

    def plotNetCDF(self,variable,save=False):
        """
         Plots the netcdf values against time.       
         :param save: boolean. If true the plot is saved as a pdf. Default is false.
        :return: None
        """
        from matplotlib.backends.backend_pdf import PdfPages
        def makeplot():
            ply.pyplot.title('{0} by time'.format(variable))
            ply.pyplot.ylabel(self.cdf.variables['value'].getncattr('Units'))
            ply.pyplot.plot(x,y)
            
        x = self.cdf['time']
        y = self.cdf['value']
        filename = "{0}_plot.pdf".format(variable)
        if save:
            with PdfPages(filename) as pdf:
                # plot the raw data
                ply.pyplot.figure(figsize=(8, 6))
                makeplot()
                pdf.savefig()  # saves the current figure into a pdf page
                ply.pyplot.close()
        makeplot() #plot to the screen.
        
        

    def plot2NetCDF(self, cdf2, smooth = 60, full = True, save = False):
        """
        :param cdf2: a second PsiNetcdf object
         :param smooth: integer. The number of seconds to average values over. The default is 60, so that average value over 1 minute is plotted against time.
        :param full: boolean. If true the entire dataset is included in one plot. Default is True
        :param save: boolean. If true the plot is saved as a pdf. Default is false.
        :return: None
        """
        return
    
