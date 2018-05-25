
import json

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


from menu import MenuInicial,SeleccionLista



CLIENT_SECRETS_FILE = "client_id.json"

MISSING_CLIENT_SECRETS_MESSAGE = "Missing client"

YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"


class YtModifier:
    def __init__(self):
        with open("listas_de_reproduccion.json") as file:
            dict_aux = json.loads(file.read())
        self.dict_listas=dict_aux

        for nombre_lista,dict_1 in self.dict_listas["playlists"].items():

            cuantas_tracks=len(dict_1["tracks"])
            print(nombre_lista,cuantas_tracks)




        self.flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                       message=MISSING_CLIENT_SECRETS_MESSAGE,
                                       scope=YOUTUBE_READ_WRITE_SSL_SCOPE)

        self.storage = Storage(os.path.abspath("%s-oauth2.json" % sys.argv[0]))
        self.credentials = self.storage.get()

        if self.credentials is None or self.credentials.invalid:
            self.flags = argparser.parse_args()
            self.credentials = run_flow(self.flow, self.storage, self.flags)

        self.youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        http=self.credentials.authorize(httplib2.Http()))

        self.nombre_lista_elegida = ""
        self.id_lista_elegida = ""
        self.termino_busqueda = ""

        self.nombre_video_datos = ""

        self.video_comentario_elegido=""

        self.channel_id=""

        self.texto_comentario=""

        self.lista_ids_stats=[]

        self.lista_resultados_stats=[]


        self.dict_ids={}


        self.menu_inicial=MenuInicial(self.dict_listas,self)

        self.menu_inicial.show()








    def crear_lista_rep(self):
        playlists_insert_response = self.youtube.playlists().insert(
            part="snippet,status",
            body=dict(
                snippet=dict(
                    title=self.dict_listas["playlists"][self.nombre_lista_elegida]["name"],
                    description="A private playlist created with the YouTube API v3"
                ),
                status=dict(
                    privacyStatus="private"
                )
            )
        ).execute()

        self.id_lista_elegida = playlists_insert_response["id"]
        self.dict_ids.update({self.nombre_lista_elegida:{self.id_lista_elegida :{}}})
        self.channel_id=playlists_insert_response["snippet"]["channelId"]

    def youtube_search(self):


        for track in self.dict_listas["playlists"][self.nombre_lista_elegida]["tracks"]:
            self.termino_busqueda=track["name"]

            try:


                search_response=self.youtube.search().list(
                    q=self.termino_busqueda,
                    part="id,snippet",
                    maxResults=1,
                    type="video"
                ).execute()


                for search_result in search_response.get("items", []):
                    if search_result["id"]["kind"] == "youtube#video":

                        self.dict_ids[self.nombre_lista_elegida][self.id_lista_elegida].update({search_result["snippet"]["title"]:search_result["id"]["videoId"]})


            except HttpError as e:
                print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))



    def añadir_a_lista(self):
        for nombre_video,id_video in self.dict_ids[self.nombre_lista_elegida][self.id_lista_elegida].items():
            playlistitems_insert_response = self.youtube.playlistItems().insert(
                part="snippet",
                body=dict(
                    snippet=dict(
                        playlistId=self.id_lista_elegida,
                        resourceId={"kind":"youtube#video","videoId":id_video}
                    )
                )
            ).execute()


    def insert_comment(self):
        print(self.video_comentario_elegido)
        insert_result = self.youtube.commentThreads().insert(
            part="snippet",
            body=dict(
                snippet=dict(
                    channelId=self.channel_id,
                    videoId=self.video_comentario_elegido[3],
                    topLevelComment=dict(
                        snippet=dict(
                            textOriginal=self.texto_comentario
                        )
                    )
                )
            )
        ).execute()


    def get_statistics(self):
        dict_stat={}
        for id in self.lista_ids_stats:
            stats_result = self.youtube.videos().list(
                part="snippet,statistics",
                id=id

                ).execute()

            nombre=stats_result["items"][0]["snippet"]["title"]
            like=stats_result["items"][0]["statistics"].get("likeCount",0)
            dislike=stats_result["items"][0]["statistics"].get("dislikeCount",0)
            comments=stats_result["items"][0]["statistics"].get("commentCount",0)
            total=stats_result["items"][0]["statistics"].get("viewCount",0)


            self.lista_resultados_stats.append((nombre,id,like,dislike,comments,total))
        print(self.lista_resultados_stats)











