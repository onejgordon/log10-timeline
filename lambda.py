#!/usr/bin/python
# -*- coding: utf-8 -*-

from logtimeline import LogTimeline


def generate(event, context):
    timeline = LogTimeline(data=event, s3_bucket='log-timelines')
    timeline.generate()