import subprocess as sp

from .handler import *

__all__ = ['version', 'info', 'stats', 'main']

clean() # clean temp file not cleaned to prevent error.

def version(name: str = None, url: str = None):
    '''
        Note: please use "info" instead to ensure result accuracy.
        only use this if your preference is speed.
    '''
    try:
        if name != None:
            url = f'https://pypi.org/project/{name}'
            
        module_name = url.split('/')

        module_name = [name for name in module_name if len(name) != 0][-1]

        wget.download(url, filename, None)

        with open(filename, 'r', errors='ignore') as file:
            file = file.readlines()
            
            line = [line for line in file if f"{module_name} " in line and "title" not in line]
            line = line[0].strip()
            version = line.split()[-1]

        clean()
        return module_name, version
    except:
        ...


class stats:
    def __init__(self, name: str = None, url: str = None):
        dataset['with_mirrors'] = scan_stats(name, url, mode='a')
        clean()
        dataset['without_mirrors'] = scan_stats(name, url, mode='s')
        clean()
        
    def get_total(self):
        return get_total()
    
    def dataset(self):
        return dataset


def info(name: str = None, url: str = None):
    try:
        package_name(name, url)
        get_info()
    except:
        ...

    return info_data


def make_table(date,details):
    name = []

    last_day = []
    last_seven_days = []
    last_thirty_days = []

    total = []

    marker = []

    def make_table_value(details):
        max = 0
        for detail in details:
            if len(detail) > max:
                max = len(detail)

        marker.append(f'{"—" * (max + 2)}+')

        def data(val):
            return f'{(" " * ((max + 1) - len(val))) + val} |'

        def handle_name(val):
            remainder = max - len(val)
            space_value = int(remainder / 2)
            space_value = " " * space_value
            value = f'{space_value}{val}{space_value}'

            return f' {" " * (max - len(value))}{value} |'


        name.append(handle_name(details[0]))

        last_day.append(data(details[1]))
        last_seven_days.append(data(details[2]))
        last_thirty_days.append(data(details[3]))

        total.append(data(details[4]))

    for detail in details:
        make_table_value(detail)

    table = f'''
+——————————————+{''.join(marker)}
|    Name(s)   |{''.join(name)}
+——————————————+{''.join(marker)}
|  {date[0]}  |{''.join(last_day)}
| Last 07 Days |{''.join(last_seven_days)}
| Last 30 Days |{''.join(last_thirty_days)}
+——————————————+{''.join(marker)}
|   Total(s)   |{''.join(total)}
+——————————————+{''.join(marker)}'''

    return table

def main():
    try:
        package_name = input('Package Name(s): ')
        
        package_names = package_name.split(',')
        
        date = ['']

        def get_stats(name):
            name = name.strip()

            statistics = stats(name)
            set = statistics.dataset()
            
            set_one = set['with_mirrors']
            # set_two = set['without_mirrors']

            dates = set_one['dates']
            date[0] = [dates[-1]]

            downloads = set_one['downloads']

            day = f"{downloads[-1]:,}"
        
            week = 0
            for i in downloads[-7:]:
                week += i
            else:
                week = f"{week:,}"

            month = 0
            for i in downloads[-30:]:
                month += i
            else:
                month = f"{month:,}"

            return [name, day, week, month, f'{statistics.get_total():,}']
        
        # data = []

        # for i in trange(len(package_names)):
        #     data.append(get_stats(package_names[i]))

        data = [get_stats(name) for name in package_names] 
        print(make_table(date[0], data))
    except:
        print('No Result...')
        
if __name__ == '__main__':
    main()