import mongoengine as me


me.connect(host="mongodb+srv://krutsvitya:vitya091003@krutsvitya.plhxk.mongodb.net/test?retryWrites=true&w=majority"
                "&appName=krutsvitya")


class Author(me.Document):
    fullname = me.StringField(required=True)
    born_date = me.StringField()
    born_location = me.StringField()
    description = me.StringField()


class Quote(me.Document):
    tags = me.ListField(me.StringField())
    author = me.ReferenceField(Author, reverse_delete_rule=me.CASCADE)
    quote = me.StringField(required=True)


class Contact(me.Document):
    fullname = me.StringField(required=True)
    email = me.EmailField(required=True)
    message_sent = me.BooleanField(default=False)
    phone = me.StringField()
