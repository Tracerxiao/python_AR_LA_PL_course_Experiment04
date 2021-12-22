#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def OSM2SQLite_database(osm_handler,db_fp,epsg=None): 
    from sqlalchemy import create_engine    
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String,Integer,Text,Float,Boolean,Date,DateTime,Time
    
    import os,shapely
    import pandas as pd
    import numpy as np
    import geopandas as gpd
    
    osm_columns=['type','geometry','id','version','visible','ts','uid','user','changeset','tagLen','tags']
    # print([len(i) for i in osm_handler.osm_node])
    # print(osm_handler.osm_node[10:13])
    # print(list(osm_handler.osm_node[10][1].coords)[0])
    
    if epsg is not None:
        crs_target={'init': 'epsg:%d'%epsg}
        
    crs={'init': 'epsg:4326'}    
    if epsg is not None:
        osm_node_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_node,columns=osm_columns,crs=crs).to_crs(epsg=epsg))
        # print("+"*50)
        # print(osm_node_db)
    else:
        osm_node_db=pd.DataFrame(osm_handler.osm_node,columns=osm_columns)
    
    osm_node_db.geometry=osm_node_db.geometry.apply(lambda row:str(row.coords[0]))
    osm_node_db.tags=osm_node_db.tags.apply(lambda row:str(row))

    # osm_node_db=osm_node_db.astype({'type':'str',
    #                                 'geometry':'',
    #                                 'id',
    #                                 'version',
    #                                 'visible',
    #                                 'ts',
    #                                 'uid',
    #                                 'user',
    #                                 'changeset',
    #                                 'tagLen',
    #                                 'tags'})
    # osm_node_db['ts']=osm_node_db.ts.astype('object')    
    # print(osm_node_db)
    # print(osm_node_db.dtypes)

    if epsg is not None:
        osm_way_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_way,columns=osm_columns,crs=crs).to_crs(epsg=epsg)) 
    else:
        osm_way_db=pd.DataFrame(osm_handler.osm_way,columns=osm_columns)    
    osm_way_db.geometry=osm_way_db.geometry.apply(lambda row:str(list(row.coords)))    
    osm_way_db.tags=osm_way_db.tags.apply(lambda row:str(row))
    # print(osm_way_db.geometry)
    
    if epsg is not None:
        osm_area_db=pd.DataFrame(gpd.GeoDataFrame(osm_handler.osm_area,columns=osm_columns,crs=crs).to_crs(epsg=epsg)) 
    else:         
        osm_area_db=pd.DataFrame(osm_handler.osm_area,columns=osm_columns) 
    osm_area_db.geometry=osm_area_db.geometry.apply(lambda row:str([list(r.exterior.coords) for r in row] ))  
    osm_area_db.tags=osm_area_db.tags.apply(lambda row:str(row))
    #print(osm_area_db)      
    
    engine=create_engine('sqlite:///'+'\\\\'.join(db_fp.split('\\')),echo=True)  
    print(engine)
    '''
    Base = declarative_base()
    class node(Base):
        __tablename__='node'
        __table_args__ = {'extend_existing': True}
        type_=Column(String(20))
        geometry=Column(Text)
        id_=Column(Integer,primary_key=True)
        version=Column(Integer)
        visible=Column(Boolean)
        ts=Column(DateTime)
        uid=Column(Integer)
        user=Column(String(100))
        changeset=Column(Integer)
        taglen=Column(Integer)
        tags=Column(Text)
        
        def __repr__(self):
            return '<node %s>'%self.id_
    print(node.__table__)

    Base.metadata.create_all(engine, checkfirst=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all(osm_handler.osm_node)
    session.commit()
    '''
    try:
        osm_node_db.to_sql('node',con=engine,if_exists='replace') #if_exists='append'        
    except:
        print("_"*50,'\n','the node table has been existed...')       
    try:    
        osm_way_db.to_sql('way',con=engine,)
    except:
        print("_"*50,'\n','the way table has been existed...')    
    try:    
        osm_area_db.to_sql('area',con=engine,)
    except:
        print("_"*50,'\n','the way table has been existed...')    
osm_Chicago_fp=r"./map.osm"
import util_pyd
osm_handler=util_pyd.osmHandler() #实例化类osmHandler()
osm_handler.apply_file(osm_Chicago_fp,locations=True) #调用 class osmium.SimpleHandler的apply_file方法

OSM_db_fp=r'./ex_04_OSM.sqlite'
epsg=32616
OSM2SQLite_database(osm_handler,OSM_db_fp,epsg=32616)
