"""
Created on Mar 12 08:23:02 2026
@author: Olivia
Description: Global config singleton. Filled when test initiates(in common_hooks.py)
            usage in other modules:

            import base.config as global_config
            url = global_config.config["base_url"]

# 其他模块直接 import 这个模块来访问配置

"""

config: dict = {}