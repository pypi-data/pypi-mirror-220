CACHE_SIZE = 256

DRIVER = 'driver'

NAMED_REGEX = r':[\w|\d]*'

MAPPER_PATH = "mapper_path"

MYSQL_COLUMN_SQL = '''SELECT GROUP_CONCAT(CONCAT("`",column_name,"`") SEPARATOR ",") 
                        FROM information_schema.columns WHERE table_schema = (SELECT DATABASE()) AND table_name = ? LIMIT ?'''

POSTGRES_COLUMN_SQL = '''SELECT array_to_string(array_agg(column_name),',') as column_name FROM information_schema.columns 
                          WHERE table_schema='public' and table_name = ? LIMIT ?'''
