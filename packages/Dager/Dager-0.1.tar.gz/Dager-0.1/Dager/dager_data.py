import pymongo
import pandas as pd
import gridfs
import json
import io

Dager_client = "mongodb://DaggerData_rw:eEsQcKvMgKfH5Di@p1ir1mon019.ger.corp.intel.com:7174,p2ir1mon019.ger.corp.intel.com:7174,p3ir1mon019.ger.corp.intel.com:7174/DaggerData?ssl=true&replicaSet=mongo7174"
Dager_conn = 'DaggerData'

ConnectionStringDager = pymongo.MongoClient(Dager_client)
DatabaseDager = ConnectionStringDager[Dager_conn]

class Database:
    def pull_data(self, lot, indicator, operation, output_format='json', file_path=None):
        """ Pull Data e.g.lot_indicator_operation 422200000_132324_Binning"""

        name = f"{lot}_{operation}_{indicator}"
        db = DatabaseDager
        fs = gridfs.GridFS(db)

        # download
        data = db.fs.files.find_one({'filename':name})
        if data:
            pulled_data = fs.get(data['_id']).read().decode()
            data_buffer = io.StringIO(pulled_data).getvalue()
            json_data = json.loads(data_buffer.replace("'", '"'))    
            print(type(json_data))
            print('Download Completed')
        else:
            json_data = None

        # Process data based on user preference
        if output_format == 'dataframe':
            df = pd.DataFrame(data=json_data['data'], columns=json_data['columns'])
            df.index = json_data['index']
            return df
        elif output_format == 'file':
            if file_path is not None:
                df = pd.DataFrame(data=json_data['data'], columns=json_data['columns'])
                df.index = json_data['index']
                df.to_csv(file_path, index=False)
                print(f"Data saved to {file_path}")
            else:
                print("Error: Please provide a valid file path to save the data.")
                return None
        else:  # Default is JSON
            return json_data
