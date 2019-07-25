import spacy
import es_core_news_sm
import rdflib
from rdflib.serializer import Serializer
from collections import OrderedDict
from SPARQLWrapper import SPARQLWrapper, JSON

# libreria spacy
nlp = es_core_news_sm.load()
# texto a tokenizar
text = """El caso Arroz Verde es una investigación publicada por el portal digital Mil Hojas. 
El portal digital reveló un correo electrónico recibido por Pamela Martínez supuesta asesora del expresidente Rafael Correa según Mil Hoja con un documento titulado Receta de Arroz Verde 502.  Según la investigación, el remitente del correo electrónico sería Geraldo Luiz Pereira de Souza- encargado de la administración y finanzas de Odebrecht en Ecuador. El mail demuestra presuntos aportes entregados por empresas multinacionales como Odebrecht al movimiento Alianza País desde noviembre de 2013 a febrero de 201 periodo en el que el expresidente Rafael Correa lideraba esa organización política. Según Mil Hojas, las donaciones alcanzarían los 11,6 millones de dólares. Las empresas que habrían realizado los aportes son: Constructora Norberto Odebrecht, SK Engineering & Construction, Sinohydro Corporation, Grupo Azul, Telconet, China International Water & Electric Corp-CWE."""

class Semantico():
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    nlp = es_core_news_sm.load()

    def consultaVirutoso(self, texto):
        text = self.nlp(texto)
        tokenized_sentences = [sentence.text for sentence in text.sents]
        datos = []
        for sentence in tokenized_sentences:
            for entity in self.nlp(sentence).ents:
                palabra = self.limpiarDatos(entity)
                consulta = """
                SELECT ?s ?p ?o
                    WHERE 
                        { 
                            ?s ?p ?o .FILTER regex(str(?s), "%s") .
                        }
                        """ % (palabra)
                self.sbcEndpoint.setQuery(consulta)
                self.sbcEndpoint.setReturnFormat(JSON)
                results = self.sbcEndpoint.query().convert()
                for result in results["results"]["bindings"]:
                    lista = []
                    listaS = result["s"]["value"]
                    listaP = result["p"]["value"]
                    listaO = result["o"]["value"]
                    lista.append(listaS)
                    lista.append(listaP)
                    lista.append(listaO)
                    datos.append(lista)
        datos = OrderedDict((tuple(x), x) for x in datos).values()
        return datos
    def limpiarDatos(self,palabra):
        palabra = str(palabra)
        print('***'*10)
        print(palabra)
        palabra = palabra.replace(' ','_')
        palabra = palabra.replace('á','a')
        palabra = palabra.replace('é','e')
        palabra = palabra.replace('í','i')
        palabra = palabra.replace('ó','o')
        palabra = palabra.replace('ú','u')
        print(palabra)
        print('***'*10)
        return palabra

s = Semantico()
print(s.consultaVirutoso(text))
