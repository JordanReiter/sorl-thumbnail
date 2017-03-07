# encoding=utf-8
from django.template import Library

from .thumbnail import resolution, thumbnail, is_portrait, margin, \
    background_margin, text_filter, markdown_thumbnails, html_thumbnails

register = Library()

register.filter('resolution', resolution)
register.tag('thumbnail', thumbnail)
register.filter('is_portrait', is_portrait)
register.filter('margin', margin)
register.filter('background_margin', background_margin)
register.filter('markdown_thumbnails', markdown_thumbnails)
register.filter('html_thumbnails', html_thumbnails)
