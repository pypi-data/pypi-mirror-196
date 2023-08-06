#%% Librería

# Manejo Datos
import json
import os
import time
from datetime import datetime

# Sql
import urllib
from sqlalchemy import create_engine, event
import cx_Oracle as Ora
import pandas as pd
import pyodbc

# GCP
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account

# Mail
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Datos Tabla Log


# Datos SA y Json con credenciales

#%% SQL Server y Oracle

def credenciales(path, cuenta):
    with open(path) as f:
        data = json.load(f) 
        for key in list(data.keys()):
            try:     
                return dict(key = key, cd = data[key][cuenta])
                break
            except:
                continue

def QxBI(sis,query, path):
    sis = sis.lower()
    inicio = time.time()
    db = credenciales(path, sis)
    if db != None:
        cd = db['cd']
        sistema = db['key']
    
        if sistema == 'oracle':
            db3 = Ora.makedsn(cd['host'],cd['port'], cd['sid'])
            with Ora.connect(cd['user'], cd['pass'], db3, encoding = 'UTF-8') as con:
                Res = pd.read_sql(query, con)
        elif sistema == 'mssql':
            with pyodbc.connect("Driver="+cd['driver']+";""Server="+cd['host']+";""Database="+cd['database']+";""uid="+cd['user']+";pwd="+cd['pass']+"") as con:
                Res = pd.read_sql(query, con)
        elif sistema == 'postgres':
            import psycopg2

            user = cd['user'] 
            pw = cd['pass']
            host = cd['host']
            port = cd['port']
            database = cd['database']
            with psycopg2.connect(user=user,password=pw,host=host,port=port,database=database) as con:
                Res = pd.read_sql(query , con)
        else:
            print('No corresponde a un sistema mapeado.')
            
    fin = time.time()
    
    print(f'Tiempo total query {sis}: {str(round((fin-inicio)/60,3))} minutos')
    return Res

def QxBI2(sis, query, col, df, path):
    sis = sis.lower()
    inicio = time.time()
    i = 0
    db = credenciales(path, sis)
    Res = pd.DataFrame()
    
    var = df[col].unique()
    
    cd = db['cd']
    sistema = db['key']

    if sistema == 'oracle':
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
        
            Query1000 = query + VARS1000
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            db3 = Ora.makedsn(cd['host'],cd['port'], cd['sid'])
            with Ora.connect(cd['user'], cd['pass'], db3, encoding = 'UTF-8') as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
    elif sistema == 'mssql':
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
            
            Query1000 = query + VARS1000
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            with pyodbc.connect("Driver="+cd['driver']+";""Server="+cd['host']+";""Database="+cd['database']+";""uid="+cd['user']+";pwd="+cd['pass']+"") as con:
                Res_aux = pd.read_sql(Query1000, con)
                Res = Res.append(Res_aux)
            i = j
    elif sistema == 'postgres':
        import psycopg2
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
            
            Query1000 = query + VARS1000
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            user = cd['user'] 
            pw = cd['pass']
            host = cd['host']
            port = cd['port']
            database = cd['database']
            with psycopg2.connect(user=user,password=pw,host=host,port=port,database=database) as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
    else:
        print('No corresponde a un sistema mapeado.')
            
    fin = time.time()
    
    print(f'Tiempo total query {sis}: {str(round((fin-inicio)/60,3))} minutos')
    return Res

def QxBI3(sis,query,col,query2,df, path):
    sis = sis.lower()
    inicio = time.time()
    i = 0
    db = credenciales(path, sis)
    Res = pd.DataFrame()
    
    var = df[col].unique()
    
    cd = db['cd']
    sistema = db['key']
    
    if sistema == 'oracle':
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            db3 = Ora.makedsn(cd['host'],cd['port'], cd['sid'])
            with Ora.connect(cd['user'], cd['pass'], db3, encoding = 'UTF-8') as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
            
    elif sistema == 'mssql':
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
                        
            with pyodbc.connect("Driver="+cd['driver']+";""Server="+cd['host']+";""Database="+cd['database']+";""uid="+cd['user']+";pwd="+cd['pass']+"") as con:
                Res_aux = pd.read_sql(Query1000, con)
                Res = Res.append(Res_aux)
            i = j
            
    elif sistema == 'postgres':
        import psycopg2
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            user = cd['user'] 
            pw = cd['pass']
            host = cd['host']
            port = cd['port']
            database = cd['database']
            with psycopg2.connect(user=user,password=pw,host=host,port=port,database=database) as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
            
    else:
        print('No corresponde a un sistema mapeado.')

    fin = time.time()
    
    print(f'Tiempo total query {sis}: {str(round((fin-inicio)/60,3))} minutos')
    return Res

def QxBI4(sis,query,col,query2, col2,query3, df, path):
    sis = sis.lower()
    inicio = time.time()
    i = 0
    db = credenciales(path, sis)
    Res = pd.DataFrame()
    
    var = df[col].unique()
    var2 = df[col2].unique()
    
    cd = db['cd']
    sistema = db['key']
    
    if sistema == 'oracle':
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
            VARS2000 = "(" + ','.join(["'" + str(x) + "'" for x in var2[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2 + VARS2000 + query3
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            db3 = Ora.makedsn(cd['host'],cd['port'], cd['sid'])
            with Ora.connect(cd['user'], cd['pass'], db3, encoding = 'UTF-8') as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
            
    elif sistema == 'mssql':
        
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
            VARS2000 = "(" + ','.join(["'" + str(x) + "'" for x in var2[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2 + VARS2000 + query3
                        
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            with pyodbc.connect("Driver="+cd['driver']+";""Server="+cd['host']+";""Database="+cd['database']+";""uid="+cd['user']+";pwd="+cd['pass']+"") as con:
                Res_aux = pd.read_sql(Query1000, con)
                Res = Res.append(Res_aux)
            i = j
            
    elif sistema == 'postgres':
        import psycopg2
        while i < len(var):
            if i+500 > len(var):
                j = len(var)
            else:
                j = i+500
                
            VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"
            VARS2000 = "(" + ','.join(["'" + str(x) + "'" for x in var2[i:j]]) + ")"
        
            Query1000 = query + VARS1000 + query2 + VARS2000 + query3
            
            print(f'[{str(i)} - {str(j)}] ({100*round((j)/len(var),2)}%)')
            
            user = cd['user'] 
            pw = cd['pass']
            host = cd['host']
            port = cd['port']
            database = cd['database']
            with psycopg2.connect(user=user,password=pw,host=host,port=port,database=database) as con:
                Res_aux = pd.read_sql(Query1000 , con)
                Res = Res.append(Res_aux)
            i = j
            
    else:
        print('No corresponde a un sistema mapeado.')

    fin = time.time()
    
    print(f'Tiempo total query {sis}: {str(round((fin-inicio)/60,3))} minutos')
    return Res


def QxInsert(df,tabla, base, path):
    '''
    Inserta datos en bases de SQL Server, tomando como referencia 3 parámetros:
        - df: DataFrame a insertar.
        - tabla: Nombre tabla en BBDD a insertar la información.
        - base: Nombre credencial a usar para la inserción
    '''
    try:
        db = credenciales(path, base)
        cd = db['cd']
        sistema = db['key']
        if sistema == 'mssql':
            
            quoted = urllib.parse.quote_plus("Driver="+cd['driver']+';''Server='+cd['host']+';''Database='+cd['database']+';''uid='+cd['user']+';pwd='+cd['pass']+'')
            engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))
    
            @event.listens_for(engine, 'before_cursor_execute')
            def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
                if executemany:
                    cursor.fast_executemany = True
            s = time.time()
            df.to_sql(tabla, con=engine, index=False, if_exists='append', chunksize=2000)
            engine.dispose()
            
            print('Tiempo total: ' + str(round((time.time()-s)/60,3)) + ' minutos')
            print(f'Insert realizado con exito: {len(df)} datos.')
        else:
            print(f'{sistema} no corresponde a Sql Server')
    except:
        print('Error inesperado: No se realizó la query inserta_datos')
        raise

def QxSentence(query, base, path):
    '''
    Función que permite ejecutar sentencias de SQL, principalmente diseñada para DELETE, DROP TABLE, ETC.
    '''
    try: 
        
        db = credenciales(path, base)
        cd = db['cd']
        sistema = db['key']
        
        if sistema == 'mssql':
            
            cnxn = pyodbc.connect("Driver="+cd['driver']+";""Server="+cd['host']+";""Database="+cd['database']+";""uid="+cd['user']+";pwd="+cd['pass']+"")
            cursor = cnxn.cursor()
            cursor.execute(query)
            cursor.commit()
            print('Query ejecutada.')
        else:
            print(f'{sistema} no corresponde a Sql Server')
    except:
        
        print(f'Error inesperado: No se pudo ejecutar la query: {query}')
        raise

        
#%% GCP 

def QxGCP(query,path):

    credentials = service_account.Credentials.from_service_account_file(
        path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    # print('Conectandose a proyecto: ',credentials.project_id)
    bqclient = bigquery.Client(credentials=credentials, 
                                project=credentials.project_id,)
    bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)
    # print('Realizando query: ',query)
    dataframe = (
        bqclient.query(query)
        .result()
        .to_dataframe(bqstorage_client=bqstorageclient)
    )
    # print(dataframe.info())
    
    return dataframe

def QxGCP2(query, col, df, path):

    inicio = time.time()

    i = 0
    Res = pd.DataFrame()
    
    var = df[col].unique()


    credentials = service_account.Credentials.from_service_account_file(
        path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        

    print('Conectandose a proyecto: ',credentials.project_id)
    
    
    while i < len(var):
        if i+10000 > len(var):
            j = len(var)
        else:
            j = i+10000

        var = df[col].unique()
        
        VARS1000 = "(" + ','.join(["'" + str(x) + "'" for x in var[i:j]]) + ")"

        Query1000 = query + VARS1000
        print('['+str(i) + ' - ' + str(j)+']')
        
        
        # Make clients.
        bqclient = bigquery.Client(credentials=credentials, 
                                    project=credentials.project_id,)
        
        bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)
        
        
        # print('Realizando query: ',query)
        
        
        dataframe = (
            bqclient.query(Query1000)
            .result()
            .to_dataframe(bqstorage_client=bqstorageclient)
        )

        Res = Res.append(dataframe)

        i = j
    
    print(Res.head())

    fin = time.time()
    
    print('Tiempo total: ' + str(round((fin-inicio)/60,3)) + ' minutos')
    return Res

def type_data(df):
    
    if df['type'] == 'string':
        return bigquery.enums.SqlTypeNames.STRING
    if df['type'] == 'integer':
        return bigquery.enums.SqlTypeNames.INT64
    if df['type'] == 'number':
        return bigquery.enums.SqlTypeNames.FLOAT64
    if df['type'] == 'datetime':
        return bigquery.enums.SqlTypeNames.DATETIME
    else:
        return bigquery.enums.SqlTypeNames.STRING


def QxInsertGCP(Proyecto, Dataset, Tabla, Data, path, Append = 1):
    if Append == 0:
        w = 'WRITE_TRUNCATE'
    else:
        w = 'WRITE_APPEND'
        
    TABLE_NAME = Tabla
    TABLE_ID = Proyecto + '.' + Dataset + '.' + TABLE_NAME
    credentials = service_account.Credentials.from_service_account_file(path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"])
    client = bigquery.Client(credentials=credentials, 
                            project=credentials.project_id)
    schema = pd.json_normalize(pd.io.json.build_table_schema(Data, primary_key=False, index=False, version=False), record_path=['fields'])
    schema['type_bq']=schema.apply(type_data, axis=1)
    schema_type_bq=[bigquery.SchemaField(col_name, type_bq) for col_name, type_bq in zip(schema['name'].tolist(), schema['type_bq'].tolist())]
    job_config = bigquery.LoadJobConfig(
        schema=schema_type_bq,
        write_disposition=w)
    job = client.load_table_from_dataframe(Data, TABLE_ID, job_config=job_config)
    job.result()
    print(f'Data Insertada en Tabla: {TABLE_NAME}')

def QxSentenceGCP(query, path):
    print(query)
    client = bigquery.Client.from_service_account_json(path)
    # client.query(query)
    print(client.query(query).result())
    
#%% Log

def carga_log(NOMBRE_PROCESO, ESTADO, INICIO, MENSAJE, PROJECT, DATASET, TABLE):
    '''
    Función que carga el LOG en GCP
    '''
    log = pd.DataFrame()
    log.loc[0,'NOMBRE_PROCESO'] = NOMBRE_PROCESO
    log.loc[0,'ESTADO'] =ESTADO
    log.loc[0,'INICIO'] = INICIO
    log.loc[0,'FIN'] = datetime.today()
    log.loc[0,'MENSAJE'] = MENSAJE
    
    QxInsertGCP(PROJECT, DATASET, TABLE, log)
    
#%% Mails

def enviarCorreo(asunto,msg,fro,to,path = None,file=None):
    try:
        mensaje = MIMEMultipart()
        mensaje['From']     = fro
        mensaje['To']       = ", ".join(to)
        mensaje['Subject']  = asunto
        mensaje.attach(MIMEText(msg, 'html'))

        if path and file:
            part = MIMEApplication(open(rf'{path}\{file}',"rb").read())
            part.add_header('Content-Disposition', 'attachment', filename=file)
            mensaje.attach(part)

        server = smtplib.SMTP('emailsrv.falabella.cl')
        server.starttls()
        server.sendmail(fro, to, mensaje.as_string())
    except Exception as e:
        raise e
    finally:
        server.quit()
        
def correo_log(nombre_etl,error, fro, to):
    try:
        mensaje = MIMEMultipart()
        mensaje['From']     = fro
        mensaje['To']       = ", ".join(to)
        mensaje['Subject']  = f'Log de error ETL: {nombre_etl}'
        
        msg =  f"""<h2><span style="font-size:13px"><span style="font-family:"Times New Roman", Times, serif">Estimados/as,</span></span></h2>
                   <h2><span style="font-size:13px"><span style="font-family:"Times New Roman", Times, serif">Se envía log de error del etl: {nombre_etl}.</span></span></h2>
                    
                   <div style="background-color:aliceblue;padding:25px;">
                   <p><span style="font-size:14px"><span style="font-family: Arial, Helvetica, sans-serif"> {error}</span></span></p>
                   </div>\
               """
        mensaje.attach(MIMEText(msg, 'html'))
        server = smtplib.SMTP('emailsrv.falabella.cl')
        server.starttls()
        server.sendmail(fro, to, mensaje.as_string())
    except Exception as e:
        raise e
    finally:
        server.quit()
        
def Delete_File(path, file):
    file_path = rf'{path}\{file}'
    print(file_path)    
    if os.path.isfile(file_path):
      os.remove(file_path)
      print(f'Archivo {file} eliminado.')
    else:
      print(f'Archivo {file} en path {path} no existe.')
      
#%%


def schema_gcp_tabla(Proyecto, Dataset, Tabla, path):
    
    schema = QxGCP("""SELECT * FROM """ + Proyecto +""".""" + Dataset + """.INFORMATION_SCHEMA.TABLES WHERE   table_name = '""" + Tabla+ """'""", path) 
    schema = pd.DataFrame(schema['ddl'][0].split(",")) 
    schema[0] = schema[0].str.strip() 
    schema = schema[0].str.split("(", expand = True ) 
    schema.loc[schema[1].isnull(), 1] = schema[0] 
    schema[1] = schema[1].str.strip() 
    schema = schema[1].str.split("\n", expand = True ) 
    schema  = schema[0].str.split(" ", expand = True) 
    schema.reset_index(inplace = True, drop = True) 

    return schema

def historificacion_gcp(PROJECT_NAME,DATASET_NAME,TABLE_NAME, campo_fecha_carga, ventana_respaldo, key_path ):
   
        
    TABLE_ID = PROJECT_NAME + '.' + DATASET_NAME + '.' + TABLE_NAME
    
    print("REVISION FECHA CARGA")
    fechas_cargadas = QxGCP( query = """SELECT distinct """ + campo_fecha_carga +""" FROM `""" + TABLE_ID +"""` order by """ + campo_fecha_carga, path =key_path )
    
    if len(fechas_cargadas) - ventana_respaldo>0:
        
        respaldar_borrar = fechas_cargadas.head(len(fechas_cargadas) - ventana_respaldo)
        
        listado_in = "('" + "','".join(respaldar_borrar[campo_fecha_carga].astype('str').unique()) + "')"
        
        print("EXTRACCION")
        
        data = QxGCP( query = """SELECT * FROM `""" + TABLE_ID +"""` where """ + campo_fecha_carga + """ in """ + listado_in, path =key_path )
        
        
        for year in data[campo_fecha_carga].dt.year.unique():
            print("RESPALDO: ", year)
            temp = data[data[campo_fecha_carga].dt.year == year]
            
            QxInsertGCP(Proyecto = PROJECT_NAME, Dataset=DATASET_NAME , Tabla = TABLE_NAME + '_'+str(year), Data = temp, Append = 1)
        
        print("BORRADO")
        
        QxGCP( query = """delete FROM `""" + TABLE_ID +"""` where """ + campo_fecha_carga + """ in """ + listado_in, path =key_path )
    else:
        print("RESPALDO PREVIAMENTE EFECTUADO DE ACUERDO A LA VENTANA DE RESPALDO: ",ventana_respaldo)
        
        
        
def aplicacion_formatos_gcp(Proyecto,Dataset,Tabla, Data , path):
    
    try:
        
        esquema = schema_gcp_tabla(Proyecto = Proyecto, Dataset = Dataset, Tabla = Tabla, path = path)
        print("APLICANDO FORMATO DESDE ESQUEMA DE LA TABLA EN GCP")
        for i in esquema.index:
            # print(esquema[1][i],esquema[0][i] )
            if esquema[1][i]=='STRING':            
                Data[esquema[0][i]] = Data[esquema[0][i]].astype('str')
                
            elif esquema[1][i]=='INT64':
                Data[esquema[0][i]] = Data[esquema[0][i]].fillna(0)
                Data[esquema[0][i]] = Data[esquema[0][i]].astype('int64')

            elif esquema[1][i]=='DATETIME': 
                Data[esquema[0][i]] = pd.to_datetime(Data[esquema[0][i]])

            elif esquema[1][i]=='DATE': 
                Data[esquema[0][i]] = pd.to_datetime(Data[esquema[0][i]]).dt.date
                
            elif esquema[1][i]=='FLOAT64':
                Data[esquema[0][i]] = Data[esquema[0][i]].astype('float64')
                
                
        return Data
    
    except:
        
        formatos_dataframe  = pd.DataFrame(Data.dtypes).reset_index()
        print("PRIMERA CAGAR, FIJANDO FORMATO DEL DATAFRAME")

        for i in formatos_dataframe.index:
            
            if formatos_dataframe[0][i]=='object':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('str')
                
            elif formatos_dataframe[0][i]=='int64':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')

            elif formatos_dataframe[0][i]=='int32':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')
                
            elif formatos_dataframe[0][i]=='datetime64[ns]': 
                Data[formatos_dataframe['index'][i]] = pd.to_datetime(Data[formatos_dataframe['index'][i]])
                
            elif formatos_dataframe[0][i]=='dbdate': 
                Data[formatos_dataframe['index'][i]] = pd.to_datetime(Data[formatos_dataframe['index'][i]])                        
                
                
                
                
            elif formatos_dataframe[0][i]=='float64':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                
            elif formatos_dataframe[0][i]=='Int64':
                
                if Data[formatos_dataframe['index'][i]].isna().any():
                    
                    Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                    
                else:
                
                    Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')

            elif formatos_dataframe[0][i]=='float32':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                
            elif formatos_dataframe[0][i]=='bool':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('str')
                
            else:
                for j in range(1000):
                    print("FALTA INCORPORAR EL FORMATO: ", formatos_dataframe[0][i] )
        
        return Data

def aplicacion_formatos_gcp2(Proyecto,Dataset,Tabla, Data , path):
    
    try:
        
        esquema = schema_gcp_tabla(Proyecto = Proyecto, Dataset = Dataset, Tabla = Tabla, path = path)
        
        try:
            print("APLICANDO FORMATO DESDE ESQUEMA DE LA TABLA EN GCP")
            for i in esquema.index:
                # print(esquema[1][i],esquema[0][i] )
                if esquema[1][i]=='STRING':            
                    Data[esquema[0][i]] = Data[esquema[0][i]].astype('str')
                    
                elif esquema[1][i]=='INT64':
                    Data[esquema[0][i]] = Data[esquema[0][i]].fillna(0)
                    Data[esquema[0][i]] = Data[esquema[0][i]].astype('int64')
    
                elif esquema[1][i]=='DATETIME': 
                    Data[esquema[0][i]] = pd.to_datetime(Data[esquema[0][i]])
    
                elif esquema[1][i]=='DATE': 
                    Data[esquema[0][i]] = pd.to_datetime(Data[esquema[0][i]]).dt.date
                    
                elif esquema[1][i]=='FLOAT64':
                    Data[esquema[0][i]] = Data[esquema[0][i]].astype('float64')
                else:
                    print("FORMATO DE GCP NO HA SIDO CLASIFICADO: ", esquema[1][i])
                   
                    
            return Data
        except:
            print("NO SE PUEDE ASIGNAR FORMATO DESDE GCP AL DATAFRAME A LA COLUMNA: ", esquema[0][i])
            
    except:
        
        formatos_dataframe  = pd.DataFrame(Data.dtypes).reset_index()
        print("PRIMERA CAGAR, FIJANDO FORMATO DEL DATAFRAME")

        for i in formatos_dataframe.index:
            
            if formatos_dataframe[0][i]=='object':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('str')
                
            elif formatos_dataframe[0][i]=='int64':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')

            elif formatos_dataframe[0][i]=='int32':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')
                
            elif formatos_dataframe[0][i]=='datetime64[ns]': 
                Data[formatos_dataframe['index'][i]] = pd.to_datetime(Data[formatos_dataframe['index'][i]])
                
            elif formatos_dataframe[0][i]=='dbdate': 
                Data[formatos_dataframe['index'][i]] = pd.to_datetime(Data[formatos_dataframe['index'][i]])                        
                
            elif formatos_dataframe[0][i]=='float64':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                
            elif formatos_dataframe[0][i]=='Int64':
                
                if Data[formatos_dataframe['index'][i]].isna().any():
                    
                    Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                    
                else:
                
                    Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('int64')

            elif formatos_dataframe[0][i]=='float32':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('float64')
                
            elif formatos_dataframe[0][i]=='bool':
                Data[formatos_dataframe['index'][i]] = Data[formatos_dataframe['index'][i]].astype('str')
                
            else:
                for j in range(1000):
                    print("FALTA INCORPORAR EL FORMATO: ", formatos_dataframe[0][i] )
        
        return Data