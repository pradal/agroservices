# -*- python -*-
# -*- coding:utf-8 -*-
#
#       Copyright 2016 INRA
#
# ==============================================================================


################## Interface Python IPM using Bioservice ########################################################

from agroservice.services import REST

__all__ = ["IPM"]

class IPM(REST):
    """
    Interface to the IPM weather https://ipmdecisions.nibio.no/api

    ..doctest::
        >>> from agroservice.ipm import IPM
        >>> ipm = IPM()

        MetaDataService
        ----------------
        >>> ipm.get_parameter()
        >>> ipm.get_qc()
        >>> ipm.get_schema_weatherdata() TypeError:get_schema_weatherdata() takes 0 positional arguments but 1 was given
        >>> ipm.post_schema_weatherdata_validate() TODO
        
        WeatherAdaptaterService
        ------------------------
        >>> ipm.get_weatheradapter_fmi(ignoreErrors=True,interval= 3600,parameters=1001,timeEnd= "2020-07-03T00:00:00+03:00",timeStart= "2020-06-12T00:00:00+03:00",weatherStationId=101533)
        >>> ipm.post_weatheradapter_fmi() TODO
        >>> ipm.get_weatheradapter_fmi_forecasts(latitude=43.36, longitude=3.52)
        >>> ipm.post_weatheradapter_fmi_forecasts() TODO
        >>> ipm.get_weatheradapter_yr(altitude=56, latitude=43.36, longitude=3.52)
        >>> ipm.post_weatheradapter_yr() TODO

        WeatherDataService
        ------------------
        >>> ipm.get_weatherdatasource()
        >>> ipm.post_weatherdatasource_location(tolerence=0) TODO
        >>> ipm.get_weatherdatasource_location_point(latitude=43.36, longitude=3.52,tolerence=0)

        DSSService
        ----------
        >>> ipm.get_crop()
        >>> ipm.get_dss()
        >>> ipm.get_pest()
        >>> ipm.post_dss_location()
        >>> ipm.get_dssId()
        >>> ipm.get_cropCode()
        >>> ipm.get_dss_location_point()
        >>> ipm.get_pestCode()
        >>> ipm.get_model()

        MetaDataService
        ---------------
        >>> dss.get_schema_fieldobservation()
        >>> dss.get_schema_modeloutput()
        >>> dss.post_schema_modeloutput_validate()
    """

    _url = "https://ipmdecisions.nibio.no/api"

    def __init__(self, verbose=False, cache=False):
        """**Constructor**
        :param verbose: set to False to prevent informative messages
    
        """
        
        self.services = REST(name="IPM", url=IPM._url,
            verbose=verbose, cache=cache)
        
        self.callback = None #use in all methods)

    ########################## MetaDataService ##########################################
       
    # Parameters
    def get_parameter(self, frmt='json'):
        """
        Get a list of all the weather parameters defined in the platform

        parameters:
        -----------

        returns:
        ---------
            a list of all the weather parameters used in the platform in json format
        """    

        res = self.services.http_get("/wx/rest/parameter", frmt='json',
                headers=self.services.get_headers(content='json'),
                params={'callback':self.callback})
        return res
    
    # QC
    def get_qc(self,frmt='json'):
        """
        Get a list of QC code

        parameters:
        -----------

        returns:
        --------
            return a list of QC code used in plateform in json format
        """

        res = self.services.http_get("wx/rest/qc", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res
    
    # schema weather data

    def get_schema_weatherdata(self,frmt='json'):
        """
        Get a schema that describes the IPM Decision platform's format for exchange of weather data
        Warning: TypeError: get_schema_weatherdata() takes 0 positional arguments but 1 was given
        
        parameters:
        ------------

        returns:
        --------
            return the schema that describes the IPM Decision platform's format for exchange of weather data in json format
        """
        res = self.services.http_get("wx/rest/schema/weatherdata", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res 

    # schema weather data validate

    def post_schema_weatherdata_validate():
        '''
        Validates the posted weather data against the Json schema

        parameters:
        -----------
            data: in json format

        return:
        -------
            {"isValid":"true"} if the data is valid, {"isValid":"false"} otherwise
        '''
        res = self.services.http_post('wx/rest/schema/weatherdata/validate',frmt='json',data=None)
        return res 

    ###################### WeatherAdaptaterService #############################

    #weatheradapter_fmi

    def get_weatheradapter_fmi(self,frmt="json",ignoreErrors="ignoreErrors",interval= "interval",parameters="parameters",timeEnd= "timeEnd",timeStart= "timeStart",weatherStationId="weatherStationId"):
        """
        Get weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ Access is made through the Institute's open data API: https://en.ilmatieteenlaitos.fi/open-data
       
        parameters:
        -----------
        ignoreErrors: (Bolean) Set to "true" if you want the service to return weather data regardless of there being errors in the service
        interval: (int) he measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly)
        parameters: (string of  Comma separated list) of the requested weather parameters
        timeStart: (string) Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00)
        timeEnd: (string) End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00)
        weatherStationId: The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather

        Returns:
        --------
         weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ in json format

        """

        res = self.services.http_get("wx/rest/weatheradapter/fmi", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,
                "ignoreErrors":ignoreErrors,"interval":interval,"parameters":",".join(map(str,parameters)),"timeEnd":timeEnd,"timeStart":timeStart,"weatherStationId":weatherStationId})
        return res
    
    def post_weatheradapter_fmi():
        """
        parameters:
        -----------
        ignoreErrors: (Bolean) Set to "true" if you want the service to return weather data regardless of there being errors in the service
        interval: (int) he measuring interval in seconds. Please note that the only allowed interval in this version is 3600 (hourly)
        parameters: (list)  Comma separated list of the requested weather parameters
        timeStart: Start of weather data period (ISO-8601 Timestamp, e.g. 2020-06-12T00:00:00+03:00)
        timeEnd: End of weather data period (ISO-8601 Timestamp, e.g. 2020-07-03T00:00:00+03:00)
        weatherStationId: The weather station id (FMISID) in the open data API https://en.ilmatieteenlaitos.fi/observation-stations?filterKey=groups&filterQuery=weather

        Returns:
        --------
         weather observations in the IPM Decision's weather data format from the Finnish Meteorological Institute https://en.ilmatieteenlaitos.fi/ in json format
        """
        pass

    def get_weatheradapter_fmi_forecasts(self,frmt='json',latitude="latitude", longitude="longitude"):
        """
        Get 36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
        
        parameters:
        -----------
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
        """
        res = self.services.http_get("wx/rest/weatheradapter/fmi/forecasts", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,"latitude":latitude, "longitude":longitude})
        return res
    
    def post_weatheradapter_fmi_forecasts(self,frmt='json',latitude="latitude",longitude="longitude"):
        """
        parameters:
        -----------
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            36 hour forecasts from FMI (The Finnish Meteorological Institute), using their OpenData services at https://en.ilmatieteenlaitos.fi/open-data
            the weather forecast formatted in the IPM Decision platform's weather data format
        """
        

    # weatheradapter_yr
    def get_weatheradapter_yr(self, frmt="json",altitude=56,longitude=3.52,latitude=43.36):
        """
        Get 9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API

        parameters:
        -----------
            altitute: (double) Meters above sea level. This is used for correction of temperatures (outside of Norway, where the local topological model is used) eg:56
            latitude: (double) WGS84 Decimal degrees eg:43.36
            longitude: (double) WGS84 Decimal degrees eg:3.52
        returns:
        --------
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)
        """
        res = self.services.http_get("wx/rest/weatheradapter/yr", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback,
                "altitude":altitude,"longitude":longitude,"latitude":latitude})
        return res
    
    def post_weatheradapter_yr():
        """
        parameters:
        -----------
            altitute: (double) Meters above sea level. This is used for correction of temperatures (outside of Norway, where the local topological model is used)
            latitude: (double) WGS84 Decimal degrees
            longitude: (double) WGS84 Decimal degrees
        
        returns:
        --------
            9 day weather forecasts from The Norwegian Meteorological Institute's Locationforecast API 
            the weather forecast formatted in the IPM Decision platform's weather data format (json)
        """
        pass

    ###################### WeatherDataService ##################################

    #weatherdatasource

    def get_weatherdatasource(self,frmt='json'):
        """
        Get a list of all the available weather data sources

        parameters:
        -----------

        returns:
        --------
        return list of all the available weather data sources in json
        """
        res = self.services.http_get("wx/rest/weatherdatasource", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback})
        return res
    
    def post_weatherdatasource_location(self, frmt='json', tolerance=0):
        """
        Search for weather data sources that serve the specific location. The location can by any valid Geometry, such as Point or Polygon. Example GeoJson input 

        parameters:
        -----------
            tolerance: (double)
        returns:
        --------
            A list of all the matching weather data sources
        """
        pass

    def get_weatherdatasource_location_point(self, frmt='json', latitude="latitude", longitude="longitude", tolerance=0):
        """
        Search for weather data sources that serve the specific point.

        parameters:
        -----------
            latitude: (double) in decimal degrees (WGS84)
            longitude: (double) in decimal degrees (WGS84)
            tolerance: Add some tolerance (in meters) to allow for e.g. a point to match the location of a weather station. The default is 0 meters (no tolerance)
        
        returns:
        --------
            A list of all the matching weather data sources in json format    
        """
        res = self.services.http_get("wx/rest/weatherdatasource/location/point", frmt=frmt,
                headers=self.services.get_headers(content=frmt),
                params={'callback':self.callback, "latitude":latitude, "longitude":longitude, "tolerance":tolerance})
        return res
  
###########################   DSSService  ################################################

    def get_crop(self,frmt='json'):
        """
        Get a list of EPPO codes for all crops that the DSS models in plateform

        Parameters:
        -----------

        Returns:
        ---------
            A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all crops that the DSS models in the platform
        """

        res = self.services.http_get("dss/rest/crop",frmt='json',
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback})
        return res


    def get_dss(self,frmt='json'):
        """
        Get a list all DSSs and models available in the platform
        
        Parameters:
        -----------

        Returns:
        --------
           a list all DSSs and models available in the platform     
        """
        res = self.services.http_get("dss/rest/dss",frmt=frmt,
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback})
        return res

    def get_pest(self,frmt='json'):
        """
        Get A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.
        
        Parameters:
        -----------

        Returns:
        --------
            A list of EPPO codes https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes) for all pests that the DSS models in the platform deals with in some way.
        """
        res = self.services.http_get("dss/rest/pest",frmt=frmt,
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback})
        return res
    
    def post_dss_location():
        pass
    
    def get_dssId(self, frmt='json',DSSId='DSSId'):
        """ 
        Get all information about a specific DSS

        Parameters:
        -----------
            DSSId: (path) the id of the DSS
        
        Returns:
        --------
            DSS(JSON) the requested DSS
        """
        res = self.services.http_get("dss/rest/dss/{}".format(DSSId),frmt=frmt)
        return res
    
    def get_cropCode(self,frmt='json',cropCode='cropCode'):
        res = self.services.http_get("dss/rest/dss/crop/{}".format(cropCode),frmt=frmt)
        return res
    
    def get_dss_location_point(self, frmt='json',latitude = 'latitude', longitude= 'longitude'):
        """ 
        Search for models that are valid for the specific point

        Parameters:
        -----------
            latitude: (double) in decimal degrees (WGS84)
            longitude: (double) in decimal degrees (WGS84)
        
        Returns:
        --------
            A list of all the matching DSS models (array of DSS (JSON))
        
        """
        res = self.services.http_get("dss/rest/dss/location/point",frmt=frmt,
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback,'latitude':latitude,'longitude':longitude})
        return res
    
    def get_pestCode(self,frmt='json',pestCode='pestCode'):
        """ 
        Returns a list of models that are applicable to the given pest

        Parameters:
        -----------
            pestCode: (path) EPPO code for the pest https://www.eppo.int/RESOURCES/eppo_databases/eppo_codes
        
        Returns:
        --------
            a list of models that are applicable to the given pest (array of DSS (JSON))
        """
        res = self.services.http_get('dss/rest/dss/pest/{}'.format(pestCode),frmt='json')
        return res
        
    def get_model(self,frmt='json',DSSId='DSSId',ModelId='ModelId'):
        """ 
        Get all information about a specific DSS model

        Parameters:
        -----------
            DSSId: (path) The id of the DSS containing the model
            ModelId: (path) The id of the DSS model requested
        
        Returns:
        --------
            The requested DSS model (DSSModel (JSON))
        
        """
        res = self.services.http_get("dss/rest/model/{}/{}".format(DSSId,ModelId),frmt=frmt)
        return res

###############################  DSSMetaDataService ##############################################

    def get_schema_fieldobservation(self, frmt='json'):
        """
        Get the generic schema for field observations, containing the common properties for field observations. 
        These are location (GeoJson), time (ISO-8859 datetime), EPPO Code for the pest and crop. 
        In addition, quantification information must be provided. 
        This is specified in a custom schema, which must be a part of the input_schema property in the DSS model metadata. 

        Parameters:
        -----------

        Returns:
        --------
            The generic schema for field observations (object(JSON))
        """
        res = self.services.http_get("/dss/rest/schema/fieldobservation",frmt=frmt,
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback})
        return res

    def get_schema_modeloutput(self, frmt='json'):
        """
        Get The Json Schema for the platform's standard for DSS model output

        Parameters:
        -----------

        Returns:
        --------
            The Json Schema for the platform's standard for DSS model output (object (JSON))
        """
        res = self.services.http_get("/dss/rest/schema/modeloutput",frmt=frmt,
                                    headers=self.services.get_headers(content=frmt),
                                    params={'callback':self.callback})
        return res
    
    def post_schema_modeloutput_validate():
        pass