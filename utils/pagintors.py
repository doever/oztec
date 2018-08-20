#!/usr/bin/python3
# -*- coding:utf-8 -*-
__author__ = 'doever'
__date__ = '2018/8/20 22:16'

from django.conf import settings


class PaginatorMiXin():
    @staticmethod
    def get_pagination_data(paginator, page_obj, arround_page=settings.ARROUND_PAGE) -> dict:
        '''分页'''
        current_page = page_obj.number
        num_pages = paginator.num_pages
        left_has_more = False
        right_has_more = False
        if current_page <= arround_page+2:
            left_pages = range(1, current_page)
        else:
            left_has_more = True
            left_pages = range(current_page-arround_page, current_page)
        if current_page >= num_pages-arround_page-1:
            right_pages = range(current_page+1, num_pages+1)
        else:
            right_has_more = True
            right_pages = range(current_page+1, current_page+arround_page+1)
        return {
            "current_page": current_page,
            "left_pages": left_pages,
            "right_pages": right_pages,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "num_pages": num_pages
        }