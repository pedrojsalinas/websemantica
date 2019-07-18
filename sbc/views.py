from django.shortcuts import render
from django.views.generic import TemplateView
# Spacy, Rdflib librerias
import spacy
import es_core_news_sm
import rdflib
from rdflib.serializer import Serializer
from .forms import SbcForm
from collections import OrderedDict
import itertools
from SPARQLWrapper import SPARQLWrapper, JSON

class IndexView(TemplateView):
    '''Metodo que renderiza la plantilla index.html'''
    template_name = 'sbc/index.html'

    def get(self, request):
        form = SbcForm()
        args = {"form": form}
        return render(request, self.template_name, args)

    def post(self, request):
        form = SbcForm(request.POST)
        if form.is_valid():
            # obtiene datos del formulario
            text = form.cleaned_data['consulta']
            # asigan texto inicial a variable
            initTexto = text
            print('---'*10)
            print(initTexto)
            print('---'*10)
            # token = Tokenizador()
            semantico = Semantico()
            # datos = token.limpiezaDatos(text)
            datosTest = semantico.consultaVirutoso(text)
            # print(datosTest)
            form = SbcForm()
            args = {"datos": datosTest, "form": form, "texto": initTexto}
        return render(request, self.template_name, args)


class Tokenizador():
    '''Clase que analiza el texto ingresado por formulario, reconoce entidades y hace consulta sparql por cada entidad encontrada.'''
    def limpiezaDatos(self, text):
        # libreria spacy
        nlp = es_core_news_sm.load()
        text = nlp(text)
        tokenized_sentences = [sentence.text for sentence in text.sents]
        g = rdflib.Graph()
        # nombre del archivo
        g.parse("mydataset.rdf")
        datos = []

        for sentence in tokenized_sentences:
            for entity in nlp(sentence).ents:
                consulta = 'SELECT ?s ?p ?o  WHERE { ?s ?p ?o .FILTER regex(str(?s), "%s") .}' % (
                    entity.text)
                for row in g.query(consulta):
                    tripleta = []
                    predicado = row.p.split("/")
                    objeto = row.o.split("/")
                    predicado = predicado[len(predicado)-1]
                    objeto = objeto[len(objeto)-1]
                    tripleta.append(entity.text)
                    tripleta.append(predicado)
                    tripleta.append(objeto)
                    datos.append(tripleta)
        # elimina duplicados 
        datos = OrderedDict((tuple(x), x) for x in datos).values()
        lista = [] 
        for i in datos:
            lista.append(i)
        return lista


class Semantico():
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")
    nlp = es_core_news_sm.load()

    def consultaVirutoso(self, texto):
        text = self.nlp(texto)
        tokenized_sentences = [sentence.text for sentence in text.sents]
        datos = []
        for sentence in tokenized_sentences:
            for entity in self.nlp(sentence).ents:
                consulta = """
                SELECT ?s ?p ?o
                    WHERE 
                        { 
                            ?s ?p ?o .FILTER regex(str(?s), "%s") .
                        }
                        """ % (entity.text)
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
        return datos

    def consultaPorUri(self, uri):
        consulta = """
                    SELECT ?p ?o
                        WHERE
                        {
                            <%s> ?p  ?o
                        }
                """ % (uri)
        self.sbcEndpoint.setQuery(consulta)
        self.sbcEndpoint.setReturnFormat(JSON)
        results = self.sbcEndpoint.query().convert()
        return results["results"]["bindings"]
