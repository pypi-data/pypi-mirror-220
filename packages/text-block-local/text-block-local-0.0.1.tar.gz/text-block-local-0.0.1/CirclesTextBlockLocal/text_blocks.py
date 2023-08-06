from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python import database 
from logger_local_python_package.localLogger import _local_logger as logger_local

import re

class TextBlocks:

  def __init__(self, text_blocks=None):
    if text_blocks is None:
      #use text blocks in text_block_table
      self.text_blocks = self.get_text_blocks()
    else:
      #use user_input for text_blocks
      self.text_blocks = text_blocks
      
  # Connect to the database
  def db_connection(self):
    database_conn = database.database()
    db = database_conn.connect_to_database()
    return db
    
  def get_block_fields(self, block_type_id):
    logger_local.start("Getting regex and field_id from block_id ...")
    
    conn = self.db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT regex, field_id FROM field.block_type_field_table WHERE block_type_id = %s OR block_type_id IS NULL" % block_type_id)
    block_fields = dict ((regex, field_id) for regex, field_id in cursor.fetchall())

    cursor.close()
    conn.close()
    logger_local.end("Regex and field ids retrieved")    
    return block_fields

  def get_fields(self):
    logger_local.start("Getting field ids and names ...")    

    conn = self.db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name FROM field.field_table")
    fields = dict ((id, name) for id, name in cursor.fetchall())

    cursor.close()
    conn.close()
    logger_local.end("Field names and ids retrieved")    
    return fields

  def get_block_types(self):
    logger_local.start("Getting block type ids and names ...")    

    conn = self.db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name, block_type_id FROM block_type.block_type_ml_table")
    block_types = dict ((id, name) for name, id in cursor.fetchall())

    cursor.close()
    conn.close()
    logger_local.end("Block types retrieved")    
    return block_types

  def get_text_blocks(self):
    logger_local.start("Getting text blocks from text_block_table ...")    

    conn = self.db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT text_block_type_id, text FROM text_block.text_block_table")
    text_blocks = cursor.fetchall()

    cursor.close()
    conn.close()
    logger_local.end("Text blocks retrieved")    
    return text_blocks

  def extract_fields(self):
    logger_local.start("Beginning text-block extracting process ...")    
    
    fields_dict = {}

    #get dictionary of field ids and names
    fields = self.get_fields()

    #loop through set of text blocks
    for block in self.text_blocks:
      (block_id , text) = (block[0], block[1])

      #reformat text 
      text = text.replace("\n", " ")

      #get block id and corresponding regex/fields 
      block_fields = self.get_block_fields(block_id)

      #extract fields for each regex expression 
      for regex in block_fields:
        if regex:    
          #check the regex is valid    
          try: 
            re.compile(regex)
            matches = re.findall(regex, text)
            if matches and block_fields[regex] != 0:
              fields_dict.setdefault(fields[block_fields[regex]], []).extend(matches)
      
          #print error if regex is invalid
          except re.error as e: 
            st = "Invalid regex: ", regex
            logger_local.exception(st, object=e)

    logger_local.end("Finished extracting all fields") 
    return fields_dict   
