from wh_app.supporting import functions
from wh_app.sql.sql_constant import sql_consts_dict

functions.info_string(__name__)


def sql_update_point(point_id:str, point_name: str, point_address: str) -> str:
    """Returns the query string to update point information """

    query = """UPDATE %(workspoints)s SET %(point_name)s = '{0}', %(point_address)s = '{1}' 
    WHERE %(point_id)s = '{2}';""" % sql_consts_dict

    return query.format(point_name,
                        point_address,
                        point_id)


def sql_inverse_points_status(point_id:str) -> str:
    """Return the query string to invert is_work section"""

    query = """UPDATE %(workspoints)s SET %(is_work)s = NOT %(is_work)s WHERE %(point_id)s = '{0}';""" % sql_consts_dict
    print(query)

    return query.format(point_id)

