from SPARQLWrapper import SPARQLWrapper, JSON


uri = "http://data.org/PLE/resource/jorgeGlas"


class Semantico():
    sbcEndpoint = SPARQLWrapper("http://localhost:8890/sparql/")

    def consultaVirutoso(self, texto):
        consulta = """
         SELECT ?s ?p ?o
            WHERE 
                { 
                    ?s ?p ?o .FILTER regex(str(?s), "%s") .
                }
                """ % (texto)
        self.sbcEndpoint.setQuery(consulta)
        self.sbcEndpoint.setReturnFormat(JSON)
        results = self.sbcEndpoint.query().convert()
        return results["results"]["bindings"]

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

      
texto = "Odebrecht"
semantico = Semantico()
# semantico.consultaPorUri(uri)
print(semantico.consultaVirutoso(texto))
