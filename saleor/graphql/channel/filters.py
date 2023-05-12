from typing import Dict


def get_channel_slug_from_filter_data(filter_data: Dict):
    return str(filter_data["channel"])
