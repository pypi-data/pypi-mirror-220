"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块路由分发
"""
from django.urls import re_path

from .apis.thread_add import ThreadAdd
from .apis.thread_category_apis import ThreadCategoryApis
from .apis.thread_category_tree import ThreadCategoryTreeAPIView
from .apis.thread_classify_apis import ThreadClassifyApis
from .apis.thread_classify_tree import ThreadClassifyTreeAPIView
from .apis.thread_item import ThreadItemAPI
from .apis.thread_list import ThreadListAPIView
from .apis.thread_other_list import AuthListAPIView, ShowListAPIView, ThreadExtendFieldList
from .apis.thread_statistic import ThreadStaticAPIView
from .apis.thread_tags_apis import ThreadTagAPIView

# 应用名称
# app_name = 'thread'

urlpatterns = [
    re_path(r'^category_add/?$', ThreadCategoryApis.add, name='category_add'),  # 类别列表
    re_path(r'^category_del/?(?P<pk>[-_\w]+)?', ThreadCategoryApis.delete, name='category_del'),  # 类别列表
    re_path(r'^category_edit/?(?P<pk>[-_\w]+)?', ThreadCategoryApis.edit, name='category_edit'),  # 类别列表
    re_path(r'^category_list/?(?P<category_value>[-_\w]+)?/?$', ThreadCategoryApis.list, name='category_list'),  # 类别列表
    re_path(r'^category_tree/?(?P<category_value>[-_\w]+)?/?$', ThreadCategoryTreeAPIView.as_view(), name='thread_category_tree'),
    re_path(r'^user_category_tree$', ThreadCategoryTreeAPIView.get_category_tree_by_user, name='thread_category_tree_v2'),

    re_path(r'^classify_list/?(?P<classify_value>[-_\w]+)?/?$', ThreadClassifyApis.list, name='classify_list'),  # 分类列表
    re_path(r'^classify_add/?$', ThreadClassifyApis.add, name='classify_list'),  # 分类列表
    re_path(r'^classify_edit/?$', ThreadClassifyApis.edit, name='classify_list'),  # 分类列表
    re_path(r'^classify_del/?$', ThreadClassifyApis.delete, name='classify_list'),  # 分类列表
    re_path(r'^classify_tree/?(?P<classify_value>[-_\w]+)?/?$', ThreadClassifyTreeAPIView.as_view(), name='thread_classify_tree'),

    re_path(r'^show_list/?$', ShowListAPIView.as_view(), name='show_list'),  # 展示类型列表
    re_path(r'^show/?(?P<show_value>[-_\w]+)?/?$', ShowListAPIView.as_view(), name='show_list'),  # 展示类型列表

    re_path(r'^list/?(?P<category_value>[-_\w]+)?/?$', ThreadListAPIView.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item_add/?$', ThreadAdd.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item/(?P<pk>\d+)?/?$', ThreadItemAPI.as_view(), name='detail'),  # 信息单挑操作：详情/编辑/删除
    # 列表 信息相关
    re_path(r'^auth[_/]list/?$', AuthListAPIView.as_view(), name='auth_list'),  # 权限列表
    re_path(r'^extend_field_list/?$', ThreadExtendFieldList.as_view(), name='extend_field_list'),  # 展示类型列表
    re_path(r'^statistic/?$', ThreadStaticAPIView.as_view(), name='statistic'),  # 计数统计，前端埋点接口

    # 标签相关接口
    re_path(r'^tag_list/?$', ThreadTagAPIView.tag_list),  # 展示类型列表
    re_path(r'^add_tag/?$', ThreadTagAPIView.add_tag),  # 展示类型列表
    re_path(r'^del_tag/?(?P<pk>[-_\w]+)?/?$', ThreadTagAPIView.del_tag),  # 展示类型列表
    re_path(r'^top_tags/?$', ThreadTagAPIView.get_top_tags),  # 展示类型列表
    re_path(r'^add_tag_map/?$', ThreadTagAPIView.add_tag_map),  # 展示类型列表
    re_path(r'^del_tag_map/?$', ThreadTagAPIView.del_tag_map),  # 展示类型列表
    re_path(r'^tag_thread/?$', ThreadTagAPIView.tag_thread),  # 展示类型列表
]
