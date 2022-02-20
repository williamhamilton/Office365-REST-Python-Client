import sys
from datetime import datetime, timedelta

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.fields.field_user_value import FieldUserValue
from office365.sharepoint.listitems.listitem import ListItem
from tests import test_team_site_url, test_client_credentials, test_user_principal_name

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

list_tasks = ctx.web.lists.get_by_title("Tasks")
items = list_tasks.items.get().top(1).execute_query()
if len(items) == 0:
    sys.exit("No items for update found")


item_to_update = items[0]  # type: ListItem
author = ctx.web.site_users.get_by_email(test_user_principal_name)

modified_date = datetime.utcnow() - timedelta(days=3)
result = item_to_update.validate_update_list_item({
    "Title": "Task (updated)",
    "Author": FieldUserValue.from_user(author),
    "Modified": modified_date
}).execute_query()

print("Item has been updated successfully")

