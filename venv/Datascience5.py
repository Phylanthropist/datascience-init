import json
import pandas as pd

df = pd.read_html('https://en.wikipedia.org/w/index.php?title=Fortune_Global_500&oldid=855890446', header=0)[0]
fortune_500 = json.loads(df.to_json(orient="records"))
print(df)
print(fortune_500)

other_data = [
    {"name": "Walmart",
     "employees": 2300000,
     "year founded": 1962
     },
    {"name": "State Grid Corporation of China",
     "employees": 927839,
     "year founded": 2002},
    {"name": "China Petrochemical Corporation",
     "employees": 358571,
     "year founded": 1998
     },
    {"name": "China National Petroleum Corporation",
     "employees": 1636532,
     "year founded": 1988},
    {"name": "Toyota Motor Corporation",
     "employees": 364445,
     "year founded": 1937},
    {"name": "Volkswagen AG",
     "employees": 642292,
     "year founded": 1937},
    {"name": "Royal Dutch Shell",
     "employees": 92000,
     "year founded": 1907},
    {"name": "Berkshire Hathaway Inc.",
     "employees": 377000,
     "year founded": 1839},
    {"name": "Apple Inc.",
     "employees": 123000,
     "year founded": 1976},
    {"name": "Exxon Mobile Corporation",
     "employees": 69600,
     "year founded": 1999},
    {"name": "BP plc",
     "employees": 74000,
     "year founded": 1908}
]

