NAME_PARAMETER = {
    "default": None,
    "doc": "An Idem name of the resource",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

RESOURCE_ID_PARAMETER = {
    "default": None,
    "doc": "An identifier of the resource in the provider",
    "param_type": "str",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

OLD_TAGS_PARAMETER = {
    "default": None,
    "doc": "Dict in the format of {tag-key: tag-value}",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

NEW_TAGS_PARAMETER = {
    "default": None,
    "doc": "Dict in the format of {tag-key: tag-value}",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

TAGS_PARAMETER = {
    "default": None,
    "doc": "The tags to apply to the resource. Defaults to None.",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}

RAW_RESOURCE_PARAMETER = {
    "default": None,
    "doc": "The raw representation of the resource in the provider",
    "param_type": "dict",
    "required": True,
    "target": "hardcoded",
    "target_type": "arg",
}
