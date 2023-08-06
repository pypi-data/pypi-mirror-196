from .profile_data import ProfileDataType


class Message(ProfileDataType):
    def __init__(self, message=''):
        ProfileDataType.__init__(self)
        self.message = message

    def get_type(self):
        return ProfileDataType.TYPE_MESSAGE

    def print_description(self):
        print(' ' * (self.parent_index + 4), 'Message', self.parent_index , self.index, self.message)
