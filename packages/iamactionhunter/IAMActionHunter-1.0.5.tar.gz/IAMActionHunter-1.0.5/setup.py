# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'IAMActionHunter', 'configs': 'IAMActionHunter/configs'}

packages = \
['IAMActionHunter',
 'IAMActionHunter.configs',
 'IAMActionHunter.lib',
 'configs',
 'lib']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.87,<2.0.0',
 'colorama>=0.4.6,<0.5.0',
 'pandas>=2.0.0,<3.0.0',
 'policyuniverse>=1.5.0.20220613,<2.0.0.0']

entry_points = \
{'console_scripts': ['IAMActionHunter = IAMActionHunter.IAMActionHunter:main',
                     'iamactionhunter = IAMActionHunter.IAMActionHunter:main']}

setup_kwargs = {
    'name': 'iamactionhunter',
    'version': '1.0.5',
    'description': 'A query tool for AWS IAM policy statements.',
    'long_description': '# Description\nIAMActionHunter is an IAM policy statement parser and query tool aims to simplify the process of collecting and understanding permission policy statements for users and roles in AWS Identity and Access Management (IAM). Although its functionality is straightforward, this tool was developed in response to the need for an efficient solution during day-to-day AWS penetration testing.\n\n### Blog Post\nhttps://rhinosecuritylabs.com/aws/iamactionhunter-aws-iam-permissions/\n\n## Offensive Use\nThe tool can be utilized to search for potential privilege escalation opportunities in AWS accounts by querying various AWS IAM actions that might be exploited. While other tools perform scans to identify privilege escalation risks, this tool enables a more manual approach, allowing users to investigate permissions and quickly review the roles, users, and resources they apply to for targeted analysis.\n\n## Blue Team Use\nThis tool also offers the ability to output and save query results in a CSV format, which is beneficial for security teams seeking a high-level overview of principal permissions and resources within an AWS account. For instance, you may want to identify users and roles with `iam:put*` permissions in an account. By executing a query and generating a CSV, you can easily review all users and roles with these permissions, along with the resources they have access to.\n\n# Installation\n\nSuggested:\n```\npip3 install iamactionhunter\n```\n\nMuch of this functionality has also been implemented into https://github.com/RhinoSecurityLabs/pacu as a module, `iam__enum_action_query` if you prefer that.\n\nClone and use Poetry:\n```\ngit clone https://github.com/RhinoSecurityLabs/IAMActionHunter.git\ncd IAMActionHunter\npoetry install\niamactionhunter --help\niamactionhunter --collect --profile <some-aws-profile>\n```\n\nClone and use Pip:\n```\ngit clone https://github.com/RhinoSecurityLabs/IAMActionHunter.git\ncd IAMActionHunter\npip install .\niamactionhunter --help\niamactionhunter --collect --profile <some-aws-profile>\n```\n\n# Usage\nHelp:\n```\nusage: iamactionhunter [-h] [--profile PROFILE] [--account ACCOUNT] [--query QUERY] [--role ROLE] [--user USER]\n                          [--all-or-none] [--collect] [--list] [--csv CSV] [--config CONFIG]\n\nCollect all policies for all users/roles in an AWS account and then query the policies for permissions.\n\noptional arguments:\n  -h, --help         show this help message and exit\n  --profile PROFILE  The name of the AWS profile to use for authentication for user/role collection.\n  --account ACCOUNT  Account number to query.\n  --query QUERY      Permissions to query. A string like: s3:GetObject or s3:* or s3:GetObject,s3:PutObject\n  --role ROLE        Filter role to query.\n  --user USER        Filter user to query.\n  --all-or-none      Check if all queried actions are allowed, not just some.\n  --collect          Collect user and role policies for the account.\n  --list             List accounts available to query.\n  --csv CSV          File name for CSV report output.\n  --config CONFIG    JSON config file for preset queries.\n```\n\n## Examples\nFirst download all IAM info for users and roles:  \n`iamactionhunter --collect --profile my-aws-profile`  \n\nList any account data has been collected for:  \n`iamactionhunter --list`  \n\nThen query something:  \n`iamactionhunter --account <account_number_of_profile_above> --query iam:create*`  \n\nThen query more:  \n`iamactionhunter --account <account_number_of_profile_above> --query iam:create*,iam:put*`  \n\nQuery a particular role:  \n`iamactionhunter --account <account_number_of_profile_above> --role some_role --query iam:*`  \n\nQuery a particular user:  \n`iamactionhunter --account <account_number_of_profile_above> --user some_user --query iam:*`  \n\nOutput to a CSV:  \n`iamactionhunter --account <account_number_of_profile_above> --query iam:* --csv report.csv`  \n\nRun a preset config:  \n`iamactionhunter --account <account_number_of_profile_above> --config dangerous_iam`\n\nRun a query which only shows the results if a user or role has all queried permissions:  \n`iamactionhunter --account <account_number_of_profile_above> --query s3:getobject,s3:listbucket --all-or-none`\n',
    'author': 'Dave Yesland with Rhino Security Labs',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
