from typing import Any

from fastadmin.models.base import ModelAdmin


def register_admin_model(admin_model_class: type[ModelAdmin], model_classes: list[Any]):
    """This method is used to register an admin model.

    :params admin_model_class: a class of admin model.
    :params model_classes: a list of model classes.
    :return: None.
    """
    from fastadmin.fastapi import admin_models

    for model_class in model_classes:
        admin_models[model_class] = admin_model_class


def unregister_admin_model(model_classes: list[Any]):
    """This method is used to unregister an admin model.

    :params admin_model_class: a class of admin model.
    :params model_classes: a list of model classes.
    :return: None.
    """
    from fastadmin.fastapi import admin_models

    for model_class in model_classes:
        if model_class in admin_models:
            del admin_models[model_class]


def get_admin_models() -> dict[Any, type[ModelAdmin]]:
    """This method is used to get a dict of admin models.

    :return: A dict of admin models.
    """
    from fastadmin.fastapi import admin_models

    return admin_models


def get_admin_model(model_name: str) -> ModelAdmin | None:
    """This method is used to get an admin model by model name.

    :params model_name: a name of model.
    :return: An admin model or None.
    """
    from fastadmin.fastapi import admin_models

    for model, admin_model_class in admin_models.items():
        if model.__name__ == model_name:
            return admin_model_class(model)
    return None
