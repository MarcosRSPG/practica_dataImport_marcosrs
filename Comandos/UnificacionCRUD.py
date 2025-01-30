from Comandos.CRUDMongo import MongoCRUD
from Comandos.CRUDMySQL import MySQLCRUD
from Comandos.CRUDNeo4J import Neo4jCRUD
from Comandos.CRUDApi import ApiCRUD
class Unificador():
    def __init__(self):
        self.mc= MongoCRUD()
        self.sc= MySQLCRUD()
        self.nc= Neo4jCRUD()
        self.ac= ApiCRUD()
    def Ejercicio1(self, nombreEmpresa):
        return self.nc.leerPersonasDeEmpresa(nombreEmpresa)
    def Ejercicio2(self):
        return self.nc.rolesDiferentes()
    def Ejercicio3(self):
        return self.nc.mismaEmpresa()
    def Ejercicio4(self, nombreEquipo):
        pipeline = [{"$match": {"name": nombreEquipo}}, {"$unwind": "$trabajadores"}, {"$project": {"trabajadores": 1, "_id": 0}}]
        idPersonas= []
        roles= []
        for i in self.mc.generarPipeline(pipeline):
            idPersonas.append(i['trabajadores']['person_id'])
            roles.append(i['trabajadores']['rol'])
        nombres= self.nc.equipoEspecifico(idPersonas)
        resultados={}
        for i in range(len(nombres)):
            resultados[nombres[i]]= roles[i]
        return resultados
    def Ejercicio5(self):
        pipeline = [{"$unwind": "$trabajadores"}, {"$group": {"_id": "$team_id", "trabajadoresPorGrupo": {"$sum": 1}}}]
        return self.mc.generarPipeline(pipeline)
    def Ejercicio6(self):
        pipeline = [{"$group": {"_id": "$team_id", "project_id": {"$sum": 1}}}]
        return self.mc.generarPipeline(pipeline)
    def Ejercicio7(self, nivelProeficiencia):
        skills= self.sc.DesdeProeficiencia(nivelProeficiencia)
        return skills 
    def Ejercicio8(self):
        idPersonas= self.sc.skillsComunes()
        return self.nc.equipoEspecifico(idPersonas)
    def Ejercicio9(self):
        pipeline = [{"$unwind": "$trabajadores"}, {"$group": {"_id": "$team_id", "idTrabajadores": {"$push": "$trabajadores.person_id"}}}]
        idTrabajadores= self.mc.generarPipeline(pipeline)
        equipos={}
        
        for i in idTrabajadores:
            equipos[i['team_id']]=i['trabajadoresPorGrupo']
        tiposEquipos= {}
        for x in equipos:
            for trabajadores in x["idTrabajadores"]:
                pipeline = [{"$unwind": "$trabajadores"}, {"$group": {"_id": "$team_id", "idTrabajadores": {"$push": "$trabajadores.person_id"}}}]
                idPokemons = self.mc.generarPipeline(pipeline)


        
    
    