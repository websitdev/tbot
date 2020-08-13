"""
This module contains all admin related commands
"""


class Admin_handler:
    def __init__(self,app,message):
        self.app                  = app
        self.message              = message
        self.chat_id              = message.chat.id
        self.user_id              = message.from_user.id
        #self.admin, self.can_kick = is_admin(self.chat_id, self.user_id)
        self.user                 = app.get_chat_member(self.chat_id, self.user_id)
        self.bot_id               = app.get_me().id
        self.admins               = app.get_chat_administrators(self.chat_id)
        self.admin_list           = [adm.user.id for adm in self.admins]
        self.is_bot_admin         = True if self.bot_id in self.admins else False

    
    def delete_message(self):
        try:
            self.app.delete_message(self.chat_id, self.user_id)
        except:
            pass


    def bot_can_restrict_members(self):
        if self.is_bot_admin and self.admins.can_restrict_members:
            return True
        return False


    def bot_can_delete_messages(self):
        if self.is_bot_admin and self.admins.can_delete_messages:
            return True
        return False


    def bot_can_pin_messages(self):
        if self.is_bot_admin and self.admins.can_pin_messages:
            return True
        return False


    def is_admin(self):
        user = self.app.get_chat_member(self.chat_id, self.user_id)
        user_type = user.status

        if user_type == "creator":
            return (True, True)

        elif user_type == "administrator":
            return (True, False)

        return (False, False)



'''
    def restrict_user(self, user_id, until_date, *args):
        self.app.restrict_chat_member(
            user_id=user_id,
            chat_id=self.chat_id,
            can_send_messages="mute" in args,
            can_add_web_page_previews=True,
            can_invite_users="no_invite" in args,
            can_send_media_messages="no_media" in args,
            can_send_other_messages="no_msg" in args,
        )
'''