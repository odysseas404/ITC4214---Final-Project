# Imports the custom permission functions used by the custom admin panel.
from .permissions import (
    can_view_custom_admin,
    can_manage_catalogue,
    can_manage_borrowing,
)


# Makes custom admin permission variables available in all templates.
# This is used mainly by the navbar and custom admin templates.
def custom_admin_access(request):
    return {
        # True if the user can see the Admin Panel button.
        "can_view_custom_admin": can_view_custom_admin(request.user),

        # True if the user can manage camera listings.
        "can_manage_catalogue": can_manage_catalogue(request.user),

        # True if the user can manage borrow requests.
        "can_manage_borrowing": can_manage_borrowing(request.user),
    }