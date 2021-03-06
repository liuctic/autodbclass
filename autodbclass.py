#/usr/bin/env python
# -*- coding: utf-8 -*-

import time

def getCommentStr(lang, ver):
    s = (" \n"
         " This file is auto generated by autodbclass tool.\n"
         " You can/should always change the code below.\n"
         " \n"
         " Target Language: " + lang + "\n"
         " Generator Version: " + ver + "\n"
         " Gen Time: " + time.strftime("%Y-%m-%d %H:%M:%S") + "\n"
         " Author: liuctic.1@gmail.com\n"
        )
    return s
    
def GenPHP(tbname, primk, primIsAuto, mustk, ordk, headRequires=""):
    GenPHPVersion = "0.1.1"
    cmt = getCommentStr("PHP", GenPHPVersion)

    print "Table:        ", tbname
    print "Primary Key:  ", primk
    print "Auto Primary: ", primIsAuto
    print "Must Keys:    ",
    print mustk
    print "Ordinary Keys:",
    print ordk

    allkeys = []
    allkeys.append(primk)
    for k in mustk:
        allkeys.append(k)
    for k in ordk:
        allkeys.append(k)

    oFileName = tbname+".class.auto.php"
    try:
        ofile = open(oFileName, "w")
        ofile.write("<?php\n\n")
        
        #comment
        ofile.write("/*\n"+cmt+"\n*/\n\n")
        #headRequireFiles
        ofile.write(headRequires+"\n")
        #class tup
        ofile.write("class " + tbname + "_tup {\n")
        for k in allkeys:
            ofile.write("    public $"+k+";\n")
        ofile.write("    public function __construct($dupObj) {\n")
        for k in allkeys:
            ofile.write("        $this->"+k+" = $dupObj->" + k + ";\n")
        ofile.write("    }\n")
        ofile.write("};\n\n")

        #class db_wrapper
        ofile.write("class "+ tbname + "_db_wrapper {\n");
        ofile.write("    private $_count;\n"
                    "    private $_changed;\n"
                    "    private $_data;\n"
                    "    private $_keys;\n"
                    "    private $_primary_key;\n"
                    "    private $_insert_must_keys;\n"
                    "    private $_primary_key_auto_inc;\n"
                    "    private $_tbname;\n"
                    "\n"
                    "    public function __construct() {\n"
                    "        $this->_count = 0;\n"
                    "        $this->_changed = false;\n"
                    "        $this->_data = array();\n"
                    "        $this->_primary_key = '"+primk+"';\n"
                    "        $this->_tbname = '" + tbname + "';\n"
                    "        $this->_insert_must_keys = array("
                    "'"+ "','".join(mustk) + "'"
                    ");\n"
                    "        $this->_keys = array("
                    "'" + "','".join(allkeys) + "'"
                    ");\n"
                    )

        ofile.write("        $this->_primary_key_auto_inc = ")
        if primIsAuto:
            ofile.write("true")
        else:
            ofile.write("false")
        ofile.write(";\n")
        ofile.write("    }\n\n")
        ofile.write("    public function __destruct() {\n"
                    "    }\n"
                    "    public function count() {\n"
                    "        return $this->_count;\n"
                    "    }\n"
                    "    public function checkPrimaryKey($kv) {\n"
                    "        if(array_key_exists($this->_primary_key, $kv)) return true;\n"
                    "        else return false;\n"
                    "    }\n"
                    "    public function checkInsertMustKeys($kv) {\n"
                    "        foreach($this->_insert_must_keys as $mustk) {\n"
                    "            if(!array_key_exists($mustk, $kv)) return false;\n"
                    "        }\n"
                    "        return true;\n"
                    "    }\n"
                    "\n"
                    "    public function select($wherekv) {\n"
                    "        $dbh = $GLOBALS['g_pdo'];\n"
                    "        $sql = 'SELECT ';\n"
                    "        $keycnt = 0;\n"
                    "        foreach($this->_keys as $dbkey) {\n"
                    "            if($keycnt == 0) {\n"
                    "                $sql = $sql.' ';\n"
                    "            }\n"
                    "            else {\n"
                    "                $sql = $sql.',';\n"
                    "            }\n"
                    "            $sql = $sql . '`' . $dbkey . '`';\n"
                    "            $keycnt++;\n"
                    "        }\n"
                    "        $sql .= \" FROM `" + tbname + "` WHERE \";\n"
                    "        $params = array();\n"
                    "        $paramcnt = 0;\n"
                    "        foreach($wherekv as $key => $value) {\n"
                    "            if($paramcnt > 0) $sql .= \" AND \";\n"
                    "            $sql = $sql . \" $key ?\";\n"
                    "            $params[] = $value;\n"
                    "            $paramcnt++;\n"
                    "        }\n"
                    "        $sth = $dbh->prepare($sql);\n"
                    "        $sth->execute($params);\n"
                    "        $this->_count = 0;\n"
                    "        $this->_data=array();\n"
                    "        while($result = $sth->fetch(PDO::FETCH_OBJ)) {\n"
                    "            $x = new " + tbname + "_tup($result);\n"
                    "            $this->_data[] = $x;\n"
                    "            $this->_count += 1;\n"
                    "        }\n"
                    "        return $this->_data;\n"
                    "    }\n"
                    "\n" 
                    "    public function update($wherekv, $updkv) {\n"
                    "        $dbh = $GLOBALS['g_pdo'];\n"
                    "        $params = array();\n"
                    "        $sql = 'UPDATE `" + tbname + "` ';\n"
                    "        $sqlset = '';\n"
                    "        foreach($updkv as $updKey => $updValue) {\n"
                    "            if($sqlset!='') $sqlset .= ',';\n"
                    "            $paramKey = \":upd_\".$updKey;\n"
                    "            $sqlset = $sqlset . $updKey . \" = \" . $paramKey;\n"
                    "            $params[$paramKey] = $updValue;\n"
                    "        }\n"
                    "        $sqlwhere = '';\n"
                    "        $wkeyId = 0;\n"
                    "        foreach($wherekv as $wk => $wv) {\n"
                    "            if($sqlwhere!='') $sqlwhere .= \" AND \";\n"
                    "            $paramKey = \":wk_\".$wkeyId;\n"
                    "            $sqlwhere = $sqlwhere . $wk . \" \" . $paramKey;\n"
                    "            $params[$paramKey] = $wv;\n"
                    "            $wkeyId++;\n"
                    "        }\n"
                    "        $sql = $sql . \" SET \" . $sqlset . \" WHERE \" . $sqlwhere;\n"
                    "        $sth = $dbh->prepare($sql);\n"
                    "        return $sth->execute($params); // bool\n"
                    "    }\n"
                    "\n"
                    "    public function insertOne($inskv) {\n"
                    "        if(!$this->_primary_key_auto_inc && !$this->checkPrimaryKey($inskv)) return false;\n"
                    "        if(!$this->checkInsertMustKeys($inskv)) return false;\n"
                    "        $dbh = $GLOBALS['g_pdo'];\n"
                    "        $keys = array_keys($inskv);\n"
                    "        $fields = '`'.implode('`, `', $keys).'`';\n"
                    "        $placeholder = '';\n"
                    "        $params = array();\n"
                    "        foreach($keys as $k) {\n"
                    "            if($placeholder!='') $placeholder.=',';\n"
                    "            $pkey = \":\".$k;\n"
                    "            $placeholder .= $pkey;\n"
                    "            $params[$pkey] = $inskv[$k];\n"
                    "        }\n"
                    "        $sql = \"INSERT INTO `" + tbname + "` ($fields) VALUES ($placeholder)\";\n"
                    "        $sth = $dbh->prepare($sql);\n"
                    "        return $sth->execute($params); // bool\n"
                    "    }\n"
                    "\n" 
                    "    public function delete($wherekv) {\n"
                    "        $dbh = $GLOBALS['g_pdo'];\n"
                    "        $sql = \"DELETE FROM `" + tbname + "` WHERE \";\n"
                    "        $params = array();\n"
                    "        $paramcnt = 0;\n"
                    "        foreach($wherekv as $key => $value) {\n"
                    "            if($paramcnt > 0) $sql .= \" AND \";\n"
                    "            $sql = $sql . \" $key ?\";\n"
                    "            $params[] = $value;\n"
                    "            $paramcnt++;\n"
                    "        }\n"
                    "        $sth = $dbh->prepare($sql);\n"
                    "        return $sth->execute($params); // bool\n"
                    "    }\n"
                    )

        ofile.write("};\n\n")
        ofile.write("?>\n")
        ofile.close()
        print "Written to", oFileName, "\n\n"
    except Exception, e:
        print e

if __name__ == "__main__":
    print "DO NOT RUN THIS FILE."
    print "Please run:  python genClass.py"
    exit(-1)
