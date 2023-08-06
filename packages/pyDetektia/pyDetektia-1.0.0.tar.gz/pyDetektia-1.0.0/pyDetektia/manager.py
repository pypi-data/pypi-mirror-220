###--------------------------###
###----- manager module -----###
###--------------------------###

'''
This module contains two classes:
    - ApiUser: Parent class
    - ApiAdmin: Child class, inherits from ApiUser

These classes are used for interacting with the database through the API.
'''

### load modules
import json
import datetime as dt
from copy import deepcopy

import requests


#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#

###-------------------------###
###----- ApiUser class -----###

class ApiUser:

    def __init__(self, username, password, ip):
        self._user = username
        self._password = password
        self._ip = ip

        self._token, self._headers, self._organization = self._get_token()
        
    def _get_token(self):

        ret = requests.post(
            f"http://{self._ip}/auth/token",
            data={
                "username": self._user,
                "password": self._password
            }
        )
        response = ret.json()
        token = response["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        organization = response["organization"]
    
        return (token, headers, organization)
    

    def _get_datasetname(self, title, scenario, user=None):
        '''
        Returns the datasetname of the given title and scenario.
        '''

        if user is None:
            user = self._user

        params = {
            "title": title,
            "scenario": scenario
        }

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasetname",
            params = params,
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret['datasetname']
    

    def _select_datasetname(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Checks if dataset is None, if so, it returns the datasetname of the given title and scenario.
        '''
        if dataset is None:
            if (title is not None) and (scenario is not None):
                return self._get_datasetname(title, scenario, user)
            else:
                raise ValueError("Either 'dataset' or both 'title' and 'scenario' are needed.")
        else:
            return dataset



    ###----------------------º
    ##--------------------
    #--- usable methods
    def get_metadata_all(self, user=None):
        '''
        Returns a list of metadata dictionaries.
        '''

        if user is None:
            user = self._user
        
        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret

    
    def get_tables_scheme(self, user=None):
        '''
        Returns a dictionary with all the point and polygons scenarios and datasets.
        '''

        if user is None:
            user = self._user

        scenarios_list = self.list_scenarios(user)
        polygons_scenarios_list = self.list_polygons_scenarios(user)

        tables_dict = {'points': {}, 'polygons': {}}
        
        for scenario in scenarios_list:
            tables_dict['points'][scenario] = []
            
            for dataset in self.list_datasets(scenario, user):
                tables_dict['points'][scenario].append(dataset)

        for polygons_scenario in polygons_scenarios_list:
            tables_dict['polygons'][polygons_scenario] = []
            
            for polygons_dataset in self.list_polygons_datasets(polygons_scenario, user):
                tables_dict['polygons'][polygons_scenario].append(polygons_dataset) 

        return tables_dict


    ###----------------------------------###
    ###----- points dataset methods -----###
    def list_scenarios(self, user=None):
        '''
        Returns a list of scenarios names.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        scenario_list = list(set([data['scenario'] for data in jsonret]))

        return scenario_list


    def list_datasets(self, scenario, user=None):
        '''
        Returns a list of dataset names.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        dataset_list = list(set([data['datasetname'] for data in jsonret if data['scenario'] == scenario]))

        return dataset_list


    def get_metadata(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns the metadata of the dataset.
        '''

        if user is None:
            user = self._user
            
        dataset = self._select_datasetname(dataset, title, scenario, user)
        
        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets/{dataset}/metadata",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    #-----------------------#
    #--- manage datasets ---#
    def add_dataset(self, dataset_json, title=None, scenario=None, organization=None):
        '''
        This method adds new dataset data and metadata tables from the dataset_json object.
        '''

        if organization is None:
            organization = self._organization

        dataset_json['metadata']['title'] = title
        dataset_json['metadata']['scenario'] = scenario
        
        ret = requests.put(
            f"http://{self._ip}/organizations/{organization}/datasets",
            json=dataset_json,
            headers=self._headers
        )

        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return ret.status_code
    

    def change_title(self, new_title, dataset, organization=None):
        """
        This method changes the title of the dataset.
        """
        
        if organization is None:
            organization = self._organization

        ret = requests.post(
            f"http://{self._ip}/organizations/{organization}/datasets/{dataset}",
            json={'new_title': new_title},
            headers=self._headers
        )

        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return {"status_code" :ret.status_code, "detail": ret.json()}    



    ###------------------------------###
    ###----- point data methods -----###
    def get_dates(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns a dictionary with the dates.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)
        
        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets/{dataset}/metadata",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        days_list = jsonret['dates']
        dates_dict = {(dt.date(1, 1, 1) + dt.timedelta(days=int(days)-365)).strftime("%Y-%m-%d"): days for days in days_list}

        return dates_dict


    def get_data(self, dataset=None, title=None, scenario=None, polygon=None, date_span=None, user=None):
        '''
        Returns data in a json object including velocities and the displacements within the date span, limits are included.
            - date_span has to be a list of the form [date_start, date_end].
                If date_span is None, the whole dataset is returned.
                If date_span is not None, the velocities are recalculated for the given date span.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        if date_span is None:
            dates = self.get_metadata(dataset=dataset, user=user)['dates']
            params = {'date_span': (dates[0], dates[-1])}
        else:
            params = {'date_span': (date_span[0], date_span[1])}

        if polygon is not None:
            params['polygon'] = json.dumps(polygon)

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets/{dataset}",
            headers=self._headers,
            params = params
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    def get_complete_json(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns data (with all dates) and metadata together in a json.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)
        
        metadata = self.get_metadata(dataset=dataset, user=user)

        dates = metadata['dates']
        date_span = [dates[0], dates[-1]]

        data = self.get_data(dataset, date_span=date_span, user=user)

        complete_json = json.loads(json.dumps({"metadata": metadata, "data": data}))

        return complete_json


    def get_velocities(self, dataset=None, title=None, scenario=None, polygon=None, extended=False, user=None):
        '''
        Returns data in a json format with the velocities stored in the database.
            - polygon: if not None, set the polygon to filter the data spatially.
            - extended: if True, returns the velocities of the points together with the extended values.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)
        
        params = {}
        if polygon is not None:
            params['polygon'] = json.dumps(polygon)

        if extended:
            params['extended'] = extended

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets/{dataset}",
            headers=self._headers,
            params = params
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    def get_point_ids(self, dataset=None, title=None, scenario=None, polygon=None, user=None):
        '''
        Returns points ids of the given dataset.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        if polygon is None:
            ret = requests.get(
                f"http://{self._ip}/users/{user}/datasets/{dataset}",
                headers=self._headers
            )
        else: 
            ret = requests.get(
                f"http://{self._ip}/users/{user}/datasets/{dataset}",
                headers=self._headers,
                params={'polygon': polygon}
            )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        point_ids = [point['id'] for point in jsonret['features']]

        return point_ids


    def get_data_details(self, ids, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns details of the data points labelled the given ids.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)
        
        if len(ids) != 0:
            params = {"ids": ids}

            ret = requests.get(
                f"http://{self._ip}/users/{user}/datasets/{dataset}/details",
                headers=self._headers,
                params=params
            )
            jsonret = ret.json()

            if ret.status_code != 200:
                raise ValueError(jsonret['detail'])

            return jsonret
        
        else:
            raise ValueError("No point id is provided")


    #----------------------#
    #--- manage plugins ---#
    def get_extended_metadata(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns the extended metadata table of a given dataset.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        ret = requests.get(
            f"http://{self._ip}/users/{user}/extended/{dataset}/metadata",
            headers=self._headers,
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])
        
        return jsonret


    def get_extended_names(self, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns the list of the extended keys.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        jsonret = self.get_extended_metadata(dataset, user=user)
        
        return [metadata['key'] for metadata in jsonret]


    def get_extended(self, key, dataset=None, title=None, scenario=None, user=None):
        '''
        Returns extended values with indices in a json format.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        ret = requests.get(
            f"http://{self._ip}/users/{user}/datasets/{dataset}/extended",
            params={'key': key},
            headers=self._headers,
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])
        
        return jsonret


    #------------------------#
    #--- polygons methods ---#
    def list_polygons_scenarios(self, user=None):
        '''
        Returns a list of scenarios names.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/polygons",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        scenario_list = [data['scenario'] for data in jsonret]

        return scenario_list


    def list_polygons_datasets(self, scenario, user=None):
        '''
        Returns a list of the loaded polygons metadata in this user and scenario.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/polygons",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        dataset_list = [data['datasetname'] for data in jsonret if data['scenario'] == scenario]

        return dataset_list


    def get_polygons(self, polygon_dataset, user=None):
        '''
        Returns a json object with the polygons and indices loaded in dataset_name.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/polygons/{polygon_dataset}",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    def get_polygons_metadata(self, polygon_dataset, user=None):
        '''
        Returns a json object with the polygons metadata loaded in dataset_name.
        '''

        if user is None:
            user = self._user

        ret = requests.get(
            f"http://{self._ip}/users/{user}/polygons/{polygon_dataset}/metadata",
            headers=self._headers
        )
        jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    def get_indices_metadata(self, polygon_dataset, index_types=None, date_span=None, user=None):
        """
        Returns the indices metadata of polygon_dataset and user
        """

        if user is None:
            user = self._user

        if date_span is not None:
            params = {'date_span': (date_span[0], date_span[1])}

            if index_types is not None:
                params['index_types'] = index_types

            ret = requests.get(
                f"http://{self._ip}/users/{user}/indices/{polygon_dataset}/metadata",
                headers=self._headers,
                params=params
            )
            jsonret = ret.json()

        else:
            if index_types is not None:
                params = {'index_types': index_types}

                ret = requests.get(
                    f"http://{self._ip}/users/{user}/indices/{polygon_dataset}/metadata",
                    headers=self._headers,
                    params=params
                )
                jsonret = ret.json()

            else:
                ret = requests.get(
                    f"http://{self._ip}/users/{user}/indices/{polygon_dataset}/metadata",
                    headers=self._headers
                )
                jsonret = ret.json()

        if ret.status_code != 200:
            raise ValueError(jsonret['detail'])

        return jsonret


    def get_polygons_time_series(self, polygon_dataset, ids, index_types=None, date_span=None, user=None):
        '''
        Returns polygons time series of type 'index_type' labelled by the given ids in between the dates in 'date_span'.
        '''

        if user is None:
            user = self._user
        
        if len(ids) != 0:
            indices_json_list = self.get_indices_metadata(polygon_dataset, index_types=index_types, date_span=date_span, user=user)
            if index_types is None: # if is None, then get all the index_types 
                index_types = list(set(row['index_type'] for row in indices_json_list))

            #--- index dict
            index_dict = {}
            for index_type in index_types:
                index_dict[index_type] = {}

            for indices_json in indices_json_list:
                index = indices_json['index']
                index_dict[indices_json['index_type']][index] = indices_json['date']

            #--- empty response
            response = {
                'type': 'FeatureCollection',
                'features': [],
                'bbox': None
            }

            #--- loop over index types
            for index_type in index_types:

                #--- query
                params = {"ids": ids, "indices": list(index_dict[index_type].keys())}

                ret = requests.get(
                    f"http://{self._ip}/users/{user}/polygons/{polygon_dataset}/details",
                    headers=self._headers,
                    params=params
                )
                jsonret = ret.json()

                if ret.status_code != 200:
                    raise ValueError(jsonret['detail'])

                #--- rename indices
                for js in jsonret['features']:
                    properties = js['properties']
                    id = properties['id']

                    properties = {str(v): properties[k] for k, v in index_dict[index_type].items()}
                    js['properties'] = properties
                    js['id'] = id
                    js['index_type'] = index_type

                    response['features'].append(js)

            return response
            
        else:
            raise ValueError("No polygon id is provided")


    #-------------------#
    #--- use plugins ---#
    def use_plugin(self, plugin_name, parameters_dict, dataset=None, title=None, scenario=None, user=None):
        '''
        Uses the plugin "plugin_name" which requires the parameters "parameters_dict" in a dictionary form.
        '''

        if user is None:
            user = self._user

        dataset = self._select_datasetname(dataset, title, scenario, user)

        ret = requests.put(
            f"http://{self._ip}/users/{user}/datasets/{dataset}/process",
            headers=self._headers,
            json={
                "name": plugin_name,
                "data": parameters_dict
            }
        )
        jsonret = ret.json()
        
        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return jsonret



#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#

###--------------------------###
###----- ApiAdmin class -----###


class ApiAdmin(ApiUser):
    '''
    This class can be created only as a admin user.
    '''

    def __init__(self, username, password, ip):
        super().__init__(username, password, ip)

        self._token, self._headers, self._organization = self._get_token()

        if isinstance(self.get_users_info(), dict):
            raise ValueError("User is not admin")


    def _reformat_polygons(self, polygons_json):
        """
        This function checks if the polygon json has the right format, if not is is modified as needed.
        """

        reformated_polygons_json = deepcopy(polygons_json)

        for i, d in enumerate(reformated_polygons_json['data']['features']):
            if 'id' in d['properties'].keys():
                d['properties']['id'] = int(d['properties']['id']) # make sure that 'id' in 'properties' is an integer.
            else:
                d['properties']['id'] = i

            if 'uid' not in d['properties'].keys():
                d['properties']['uid'] = d['properties']['id']
            
            if d['geometry']['type'] == 'MultiPolygon':
                d['geometry']['type'] = 'Polygon'
                d['geometry']['coordinates'] = d['geometry']['coordinates'][0]
                
        return reformated_polygons_json


    ###----------------------
    ##--------------------
    #--- usable methods

    #--------------------#
    #--- manage users ---#
    def get_users_info(self):
        '''
        Returns a list of dictionaries. Each dictionary has the information.
        '''
        
        ret = requests.get(
            f"http://{self._ip}/users",
            headers=self._headers
        )
        jsonret = ret.json()

        return jsonret


    def get_users_list(self):
        '''
        Returns a list with all the user names.
        '''

        ret = requests.get(
            f"http://{self._ip}/users",
            headers=self._headers,
        )
        jsonret = ret.json()

        user_list = [user['name'] for user in jsonret]

        return user_list


    def create_user(self, organization, new_user, new_pwd, e_mail=None, _is_admin=False):
        '''
        This mehotd creates a new user.
        '''

        is_admin = "TRUE" if _is_admin else "FALSE" 
        email = e_mail or f"{new_user}@detektia.com"

        ret = requests.post(
            f"http://{self._ip}/users",
            json={
                "organization": organization,
                "name": new_user,
                "password": new_pwd,
                "email": email,
                "is_admin": is_admin,
            },
            headers=self._headers,
        )

        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return ret.status_code


    def delete_user(self, user_to_delete):
        '''
        This mehotd deletes user.
        '''

        ret = requests.delete(
            f"http://{self._ip}/users/{user_to_delete}", 
            headers=self._headers
        )

        if ret.status_code != 204:
            raise ValueError(ret.json()['detail'])

        return ret.status_code


    #-----------------------#
    #--- manage datasets ---#
    def delete_dataset(self, dataset, organization):
        '''
        This method deletes a complete dataset.
        '''

        ret = requests.delete(
            f"http://{self._ip}/organizations/{organization}/datasets/{dataset}", 
            headers=self._headers
        )

        if ret.status_code != 204:
            raise ValueError(ret.json()['detail'])

        return ret.status_code


    #-----------------------#
    #--- manage extended ---#
    def add_extended(self, dataset, extended_dict, organization):
        '''
        This methods adds an extended_dict in the extended table of dataset.
        '''

        ret = requests.patch(
            f"http://{self._ip}/organizations/{organization}/datasets/{dataset}/extended",
            json=extended_dict,
            headers=self._headers
        )

        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return ret.status_code
    
    
    def delete_extended(self, dataset, key, organization):
        '''
        This method deletes the extended values with key 'key' in the dataset 'dataset'.
        '''
        
        ret = requests.delete(
            f"http://{self._ip}/organizations/{organization}/datasets/{dataset}/extended",
            params={'key': key},
            headers=self._headers
        )

        if ret.status_code != 204:
            raise ValueError(ret.json()['detail'])

        return ret.status_code
        

    #-----------------------#
    #--- manage polygons ---#
    def add_polygons(self, polygons_dataset, polygons_json, organization):
        '''
        This method adds polygons to the dataset with name dataset_name.
        '''

        polygons_json = self._reformat_polygons(polygons_json)

        ret = requests.put(
            f"http://{self._ip}/organizations/{organization}/polygons/{polygons_dataset}",
            json=polygons_json,
            headers=self._headers
        )

        if ret.status_code != 200:
            raise ValueError(ret.json()['detail'])

        return ret.status_code


    def delete_polygons(self, polygons_dataset, organization):
        '''
        This method delete polygons of dataset with name polygons_dataset.
        '''

        ret = requests.delete(
            f"http://{self._ip}/organizations/{organization}/polygons/{polygons_dataset}",
            headers=self._headers
        )

        if ret.status_code != 204:
            raise ValueError(ret.json()['detail'])

        return ret.status_code
