import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-waypoint",
    "version": "0.0.0",
    "description": "Prebuilt waypoint Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-waypoint.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-waypoint.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_waypoint",
        "cdktf_cdktf_provider_waypoint._jsii",
        "cdktf_cdktf_provider_waypoint.auth_method",
        "cdktf_cdktf_provider_waypoint.config_source",
        "cdktf_cdktf_provider_waypoint.data_waypoint_app",
        "cdktf_cdktf_provider_waypoint.data_waypoint_auth_method",
        "cdktf_cdktf_provider_waypoint.data_waypoint_project",
        "cdktf_cdktf_provider_waypoint.data_waypoint_runner_profile",
        "cdktf_cdktf_provider_waypoint.project",
        "cdktf_cdktf_provider_waypoint.provider",
        "cdktf_cdktf_provider_waypoint.runner_profile"
    ],
    "package_data": {
        "cdktf_cdktf_provider_waypoint._jsii": [
            "provider-waypoint@0.0.0.jsii.tgz"
        ],
        "cdktf_cdktf_provider_waypoint": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.17.0, <0.18.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.84.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
