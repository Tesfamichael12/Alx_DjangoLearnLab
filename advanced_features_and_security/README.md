## Permissions and Groups Setup

- **Groups Created:**
  - Editors: Can create and edit books.
  - Viewers: Can view books.
  - Admins: Can view, create, edit, and delete books.

- **Permissions Defined in `Book` Model:**
  - can_view: Can view books
  - can_create: Can create books
  - can_edit: Can edit books
  - can_delete: Can delete books

- **Views Protected:**
  - `edit_book` view: Requires `can_edit` permission.
