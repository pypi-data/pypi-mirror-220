"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaobject.activity import Status
from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase.mockmongo import MockMongoManager
from heaserver.activity import service
from heaobject.user import NONE_USER
from heaobject.project import AWSS3Project
from heaserver.service.testcase.expectedvalues import Action


db_store = {
    service.MONGODB_DESKTOP_OBJECT_ACTION_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'action': 'GET',
        'status': Status.SUCCEEDED.name,
        'arn': 'a:1323444',
        'user_id': 'user-a',
        'source': None,
        'type': 'heaobject.activity.DesktopObjectAction',
        'old_object_uri': None,
        'new_object_uri': None,
        'old_object_type_name': AWSS3Project.get_type_name(),
        'new_object_type_name': AWSS3Project.get_type_name(),
        'old_object_id': '666f6f2d6261722d71757578',
        'new_object_id': '666f6f2d6261722d71757578'
    },
    {
        'id': '0123456789ab0123456789ab',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Luximus',
        'invites': [],
        'modified': None,
        'name': 'luximus',
        'owner': NONE_USER,
        'action': 'GET',
        'status': Status.IN_PROGRESS.name,
        'arn': 'a:1323444',
        'user_id': 'user-a',
        'source': None,
        'type': 'heaobject.activity.DesktopObjectAction',
        'old_object_uri': None,
        'new_object_uri': None,
        'old_object_type_name': AWSS3Project.get_type_name(),
        'new_object_type_name': AWSS3Project.get_type_name(),
        'old_object_id': '0123456789ab0123456789ab',
        'new_object_id': '0123456789ab0123456789ab'
    }],
    'recentlyaccessedviews': [{
        'id': '666f6f2d6261722d71757578',
        'accessed': '2022-05-17T00:00:00-06:00',
        'actual_object_id': '666f6f2d6261722d71757578',
        'actual_object_type_name': 'heaobject.project.AWSS3Project',
        'actual_object_uri': None,
        'type': 'heaobject.activity.RecentlyAccessedView',
        'created': None,
        'modified': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'name': None,
        'display_name': 'Untitled RecentlyAccessedView',
        'invites': [],
        'owner': 'user-a',
        'shares': [],
        'source': None
    },
    {
        'id': '0123456789ab0123456789ab',
        'accessed': '2022-05-17T00:00:00-06:00',
        'actual_object_id': '0123456789ab0123456789ab',
        'actual_object_type_name': 'heaobject.project.AWSS3Project',
        'actual_object_uri': None,
        'type': 'heaobject.activity.RecentlyAccessedView',
        'created': None,
        'modified': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'name': None,
        'display_name': 'Untitled RecentlyAccessedView',
        'invites': [],
        'owner': 'user-a',
        'shares': [],
        'source': None
    }
    ]}


RecentlyAccessedViewsByTypeTestCase = get_test_case_cls_default(coll='recentlyaccessedviews',
                                                         wstl_package=service.__package__,
                                                         href='http://localhost:8080/recentlyaccessedviews/bytype/heaobject.project.AWSS3Project',
                                                         fixtures=db_store,
                                                         db_manager_cls=MockMongoManager,
                                                         get_all_actions=[Action(name='heaserver-activity-recentlyaccessed-get-actual',
                                                             url='{+actual_object_uri}',
                                                             rel=['hea-actual'])])


TestCase = get_test_case_cls_default(coll=service.MONGODB_DESKTOP_OBJECT_ACTION_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/desktopobjectactions',
                                     fixtures=db_store,
                                     db_manager_cls=MockMongoManager,
                                     get_actions=[Action(name='heaserver-activity-desktopobjectaction-get-properties',
                                                         rel=['hea-properties']),
                                                  Action(name='heaserver-activity-desktopobjectaction-get-self',
                                                         url='http://localhost:8080/desktopobjectactions/{id}',
                                                         rel=['self']),
                                                  Action(name='heaserver-activity-desktopobjectaction-get-old-object-uri',
                                                         url='http://localhost:8080{+old_object_uri}',
                                                         rel=['hea-desktop-object'],
                                                         itemif='old_object_uri is not None and new_object_uri is None'),
                                                  Action(name='heaserver-activity-desktopobjectaction-get-new-object-uri',
                                                         url='http://localhost:8080{+new_object_uri}',
                                                         rel=['hea-desktop-object'],
                                                         itemif='new_object_uri is not None')
                                                  ],
                                     get_all_actions=[Action(name='heaserver-activity-desktopobjectaction-get-properties',
                                                             rel=['hea-properties']),
                                                      Action(name='heaserver-activity-desktopobjectaction-get-self',
                                                             url='http://localhost:8080/desktopobjectactions/{id}',
                                                             rel=['self']),
                                                      Action(name='heaserver-activity-desktopobjectaction-get-old-object-uri',
                                                             url='http://localhost:8080{+old_object_uri}',
                                                             rel=['hea-desktop-object'],
                                                             itemif='old_object_uri is not None and new_object_uri is None'),
                                                      Action(name='heaserver-activity-desktopobjectaction-get-new-object-uri',
                                                             url='http://localhost:8080{+new_object_uri}',
                                                             rel=['hea-desktop-object'],
                                                             itemif='new_object_uri is not None')])
