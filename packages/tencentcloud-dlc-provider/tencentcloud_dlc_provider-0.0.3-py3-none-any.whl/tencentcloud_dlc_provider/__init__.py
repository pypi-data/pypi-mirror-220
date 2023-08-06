from tencentcloud_dlc_provider.hooks.dlc_hook import DLCHook


def get_provider_info():
    return {
        "package-name": "tencentcloud-dlc-provider",
        "name": "tencentcloud dlc provider",
        "description": "tencentcloud dlc provider",
        "hook-class-names": [
            "tencentcloud_dlc_provider.hooks.dlc_hook.DLCHook",
        ],
    }
