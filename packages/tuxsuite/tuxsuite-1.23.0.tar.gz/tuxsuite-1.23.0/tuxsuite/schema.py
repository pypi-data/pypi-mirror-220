# -*- coding: utf-8 -*-

import re
from voluptuous import Any, Optional, Required, Schema, Url, Invalid, All

SchemaError = Invalid


def plan():
    return Schema(
        {
            Required("version"): 1,
            Optional("name"): str,
            Optional("description"): str,
            Required("jobs"): [
                Any(
                    {Optional("name"): str, Required("build"): dict},
                    {
                        Optional("name"): str,
                        Required("build"): dict,
                        Required("test"): dict,
                    },
                    {
                        Optional("name"): str,
                        Required("build"): dict,
                        Required("tests"): list,
                    },
                    {Optional("name"): str, Required("builds"): list},
                    {
                        Optional("name"): str,
                        Required("builds"): list,
                        Required("test"): dict,
                    },
                    {
                        Optional("name"): str,
                        Required("builds"): list,
                        Required("tests"): list,
                    },
                    {Optional("name"): str, Required("tests"): list},
                    {Optional("name"): str, Required("test"): dict},
                )
            ],
        },
        extra=True,
    )


def bake_plan():
    return Schema(
        {
            Optional("common"): dict,
            Required("version"): 1,
            Optional("name"): str,
            Optional("description"): str,
            Required("jobs"): [
                Any(
                    {Optional("name"): str, Required("bake"): dict},
                    {Optional("name"): str, Required("bakes"): list},
                )
            ],
        },
        extra=True,
    )


def validate_git_url(url):
    git_url_pattern = r"^(https?|git)://"
    if not re.match(git_url_pattern, url):
        raise Invalid("Invalid url")
    return url


def tuxtrigger_config():
    return Schema(
        {
            Required("repositories"): [
                {
                    Optional("branches"): [
                        {
                            Required("name"): str,
                            Required("plan"): str,
                            Optional("squad_project"): str,
                        }
                    ],
                    Required("url"): All(Url(), validate_git_url),
                    Required("squad_group"): str,
                    Optional("regex"): str,
                    Optional("default_plan"): str,
                    Optional("squad_project_prefix"): str,
                }
            ]
        },
        extra=True,
    )
