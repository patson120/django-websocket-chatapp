
import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync


class ChatWebSocket(WebsocketConsumer):

    def connect(self):
        user = self.scope['user'] # Permet d'obtenir le nom de l'utilisateur actuellement connecté ( depuis la session )
        # room_name = self.scope['url_route']['kwargs']['username'] # Je laisse l'utilisateur ici car je le prends dans la session 
        self.group_name = self.scope['url_route']['kwargs']['group']
        self.room_group_name = 'chat_%s' % self.group_name

        # other_user = User.objects.get(username__icontains=self.room_name)

        # self.thread_obj = Thread.objects.get_or_create_personal_thread(me, other_user)

        # self.thread = 'personnal_thread_{0}'.format(self.thread_obj.id)
        # print(self.thread_obj)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )
        self.accept()

        self.send(text_data=json.dumps({
            "type": "chat",
            "message": "[{0}] vous êtes connectez. chatez avec vos amis !".format(user),
            "chat_group": self.room_group_name,
            "chat_channel": self.channel_name
        }))
        print(f">>>>>>>>>>>>>>>>>>>>>>>> { user } Connected <<<<<<<<<<<<<<<<<<<<<<<<<")

    def receive(self, text_data):
        data = json.loads(text_data)

        # self.store_message(data.get('message')) # Ici c'est la méthode qui nous permet de stocker les messages en base de données 
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message', # Methode charge d'envoyer les messages aux utilisateurs 
                'message': "[{0}] => {1}".format(self.scope['user'], data.get('message', 'No message!')),
            }
        )

    def chat_message(self, text_data):
        message = text_data.get('message', 'No message!')
        self.send(text_data=json.dumps({
            'type': 'chat',
            'origin': 'Serveur',
            'message': message,
            'user': str(self.scope['user']),
            "chat_group": self.room_group_name,
            "chat_channel": self.channel_name
        }))

    # def store_message(self, text):
    #     Message.objects.create(
    #         thread=1,
    #         sender=self.scope['user'],
    #         text=text,
    #     )

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print(f">>>>>>>>>>>>>>>>>>>>>>>> { self.scope['user'] } disconnected <<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Group name was {0}".format(self.room_group_name))

class ChatAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user'] # Permet d'obtenir le nom de l'utilisateur actuellement connecté ( depuis la session )
        self.group_name = self.scope['url_route']['kwargs']['group']
        self.room_group_name = 'chat_%s' % self.group_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "chat",
            "message": "[{0}] vous êtes connectez. chatez avec vos amis !".format(user),
            "chat_group": self.room_group_name,
            "chat_channel": self.channel_name
        }))
        print(f">>>>>>>>>>>>>>>>>>>>>>>> { user } Connected <<<<<<<<<<<<<<<<<<<<<<<<<")


    async def receive(self, text_data):
        data = json.loads(text_data)

        # self.store_message(data.get('message')) # Ici c'est la méthode qui nous permet de stocker les messages en base de données 
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', # Methode charge d'envoyer les messages aux utilisateurs 
                'message': "[{0}] => {1}".format(self.scope['user'], data.get('message', 'No message!')),
            }
        )


    # Envoi du message proprement dit 
    async def chat_message(self, text_data):
        message = text_data.get('message', 'No message!')
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'origin': 'Serveur',
            'message': message,
            'user': str(self.scope['user']),
            "chat_group": self.room_group_name,
            "chat_channel": self.channel_name
        }))

    # Déconnexion des utilisateurs 
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f">>>>>>>>>>>>>>>>>>>>>>>> { self.scope['user'] } Disconnected <<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Group name was {0}".format(self.room_group_name))

