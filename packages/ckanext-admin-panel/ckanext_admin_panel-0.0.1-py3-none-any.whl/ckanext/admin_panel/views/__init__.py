from ckanext.admin_panel.views.basic import ap_basic
from ckanext.admin_panel.views.config import ap_config_list
from ckanext.admin_panel.views.user import ap_user


def get_blueprints():
    return [ap_basic, ap_config_list, ap_user]
