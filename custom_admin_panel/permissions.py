# Group names used for custom admin access.
ADMINISTRATOR_GROUP = "Administrator"
BORROWING_MANAGER_GROUP = "Borrowing Manager"
CATALOGUE_MANAGER_GROUP = "Catalogue Manager"

# Checks whether the user belongs to a specific group.
def user_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Checks whether the user can see the custom admin panel.
def can_view_custom_admin(user):
    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or user_in_group(user, ADMINISTRATOR_GROUP)
        or user_in_group(user, BORROWING_MANAGER_GROUP)
        or user_in_group(user, CATALOGUE_MANAGER_GROUP)
    )

# Checks whether the user can manage borrow requests.
def can_manage_borrowing(user):
    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or user_in_group(user, ADMINISTRATOR_GROUP)
        or user_in_group(user, BORROWING_MANAGER_GROUP)
    )

# Checks whether the user can manage catalogue items.
def can_manage_catalogue(user):
    if not user.is_authenticated:
        return False

    return (
        user.is_superuser
        or user_in_group(user, ADMINISTRATOR_GROUP)
        or user_in_group(user, CATALOGUE_MANAGER_GROUP)
    )