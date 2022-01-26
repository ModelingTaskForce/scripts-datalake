import os
import pathlib
from datetime import datetime
import requests
from tqdm import tqdm


# set folders
datalake = '/media/fabio/19940C2755DB566F/PAMepi/datalake'
raw = 'raw_data_covid19_version-' + datetime.now().strftime('%Y-%m-%d')

urls = {
    'mobility': [
        'https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv',
        os.path.join(datalake, raw, 'data-google_mobility/'),
    ],
    'wcota': [
        'https://github.com/wcota/covid19br/raw/master/cases-brazil-cities-time.csv.gz',
        os.path.join(datalake, raw, 'data-wesley_cota/'),
    ]
}


for url in urls.keys():
    url, output = urls[url][0], urls[url][1]

    file_csv = requests.get(url, stream=True)
    name = ''.join(url.split('/')[-1:])

    pathlib.Path(output).mkdir(parents=True, exist_ok=True)

    with open(os.path.join(output, name), 'wb') as f, tqdm(
         desc=name,
         total=int(file_csv.headers['Content-Length']),
         unit='iB',
         unit_scale=True,
         unit_divisor=1024
     ) as bar:
         # iterating chunk and writing on file opened
         for content in file_csv.iter_content(chunk_size=1024):
             size = f.write(content)
             # updating progress bar
             bar.update(size)
     
     
     
