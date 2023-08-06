# pypi-packages
Python util functions
# pypi-packages
Python util functions

`pip3 install aggdirect-job-report-utility` to install packages


## What is it

Support for coolmap path jobs report api,This packages will help the end user to optimized the code redundancy.This class has two memeber function prepare_task_status_data and prepare_driver_data which will return modfied data.


    Coolmap(<jobs_report_dataframe>)




## Usage/Examples

```python
from aggdirect-job-report-utility import Coolmap

job_obj = Coolmap(<jobs_report_dataframe>)

```
## Method to get the jobs task status data

```python
job_obj.prepare_task_status_data(<column_lst>)



Example:
    
    Input:

    >>cool_obj.prepare_task_status_data(['order_number', 'job_id','project',etc...])

    Output:

    >>{    
         {  'order_number': 11261,
            'job_id': 'e4e33b0838554e8d920de29a03465556',
            'project': 'Watkins Mill - Hourly',
            'unit': 'Hourly',
            'customer_name': 'G.A. & F.C. Wagman, Inc.',
            'customer_contact': '(717) 764-8521',
            'material': 'Dump Truck',
            'pickup_location': 'Watkins Mills Rd 270 job - West Side',
            'pickup_lat': 39.1554374774,
            'pickup_lon': -77.2275807503,
            'delivery_location': 'Aggregate Rockville',
            'delivery_lat': 0.0,
            'delivery_lon': -77.2197253233,
            'delivery_contact': '',
            'Incomplete': 0,
            'Open': 1,
            'Ongoing': 1,
            'Done': 8,
            'Total': 10},
        {
            'order_number': 11529,
            'job_id': '63d998e59e3940bcbcf7032e1ccf5d8f',
            'project': 'CSO 19',
            'unit': 'Load',
            'customer_name': 'Salini Impregilo Healy JC NEBT',
            'customer_contact': '2027877672',
            'material': 'DT Mud',
            'pickup_location': 'CSO 19 (RFK)',
            'pickup_lat': 38.883644679,
            'pickup_lon': -76.9719445825,
            'delivery_location': 'Sands Road',
            'delivery_lat': 38.8369976593,
            'delivery_lon': -76.6873279545,
            'delivery_contact': '',
            'Incomplete': 13,
            'Open': 45,
            'Ongoing': 4,
            'Done': 26,
            'Total': 88
        }
    }

```
## Method to get the jobs driver data

```python
job_obj.prepare_driver_data(<column_lst>)



Example:
    
    Input:

    >>cool_obj.prepare_driver_data(['order_number', 'trucking_company', 'trucking_company',etc...])

    Output:

    >>{[
            {
                'trucking_company': '103 transport LLC.',
                'trucking_company_phone': '',
                'driver_name': 'Celio Gautreaux',
                'driver_phone': 2402867307.0
            },
            {
                'trucking_company': 'Bo-Bo & BabyGirl Trucking',
                'trucking_company_phone': '',
                'driver_name': 'Andre Wilson',
                'driver_phone': 2408326461.0
            }
            .
            .
            .
            .
        ]
    }

