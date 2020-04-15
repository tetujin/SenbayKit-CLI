#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 17:46:48 2017

BaseX for Python

@author: Yuuki Nishiyama
"""
import math
import copy

class BaseX:

    PN = 0; # Positional Notation (2-122)

    TABLE = [   1, 2, 3, 4,
             5,   6,  7,  8,  9,
             10,  11,  12,  13,  14,
             15,  16,  17,  18,  19,
             20,  21,  22,  23,  24,
             25,  26,  27,  28,  29,
             30,  31,  32,  33,  34,
             35,  36,  37,  38,
             40,  41,  42,  43,
                     47,  48,  49,
             50,  51,  52,  53,  54,
             55,  56,  57,       59,
             60,  61,  62,  63,  64,
             65,  66,  67,  68,  69,
             70,  71,  72,  73,  74,
             75,  76,  77,  78,  79,
             80,  81,  82,  83,  84,
             85,  86,  87,  88,  89,
             90,  91,  92,  93,  94,
             95,  96,  97,  98,  99,
             100,  101,  102,  103,  104,
             105,  106,  107,  108,  109,
             110,  111,  112,  113,  114,
             115,  116,  117,  118,  119,
             120,  121,  122,  123,  124,
             125,  126,  127];

    REVERSE_TABLE =  [ 0,  0,  1,  2,  3,
                       4,  5,  6,  7,  8,
                       9,  10,  11,  12,  13,
                       14,  15,  16,  17,  18,
                       19,  20,  21,  22,  23,
                       24,  25,  26,  27,  28,
                       29,  30, 31,  32,  33,
                       34,  35,  36,  37, 0,
                       38,  39,  40,  41, 0,
                        0,  0,  42, 43, 44,
                       45,  46,  47,  48,  49,
                       50,  51,  52,   0,   53,
                       54,  55,  56,  57,  58,
                       59,  60,  61,  62,  63,
                       64,  65,  66,  67,  68,
                       69,  70,  71,  72,  73,
                       74,  75,  76,  77,  78,
                       79,  80,  81,  82,  83,
                       84,  85,  86,  87,  88,
                       89,  90,  91,  92,  93,
                       94,  95,  96,  97,  98,
                       99,  100,  101,  102,  103,
                       104,  105,  106,  107,  108,
                       109,  110,  111,  112,  113,
                       114,  115,  116,  117,  118,
                       119,  120,  121];

    def __init__(self, positionalNotation=121):
        """
        @param: Positional notation
        """
        if positionalNotation > len(self.TABLE) or positionalNotation < 2 :
            print("shinsu must be 2-%ld", str(len(self.TABLE)));
        else:
            self.PN = positionalNotation;
        #    print("A positional notation is " + str(self.PN));


    def encodeLongValue(self, lVal):
        """
        @param: A value with a long format
        """
        # マイナスの値の場合は、プラスに変換
        isNegative = False;
        if lVal < 0:
            isNegative = True;
            lVal *= -1;

        #X進数変換を行う
        places = [];
        if lVal == 0:
            places.append(0);
        else:
            while lVal > 0:
                # NSLog(@"%ld / %d  = %ld ... %d", (long)value, shinsu, ((long)value/(int)shinsu), (int)fmod(value, shinsu));
                remainder = int(math.fmod(lVal, self.PN));
                places.append(self.TABLE[remainder]);
                lVal = int(int(lVal) / self.PN);
                # print(lVal, self.PN);

        '''
        0x31 -> 16進数表記の1 (ascii文字)
        49   -> 10進数表記の1 (ascii文字)
        '''
        muString = "";
        for number, place in enumerate(places):
            # https://python.civic-apps.com/char-ord/
            # print(place);
            muString = chr(place) + muString
            # [muString insertString:[NSString stringWithFormat:@"%c",ellipsis] atIndex:0];

        '''
        for(NSNumber* number in ketas){
            char ellipsis = [number floatValue];
            //NSLog(@"%@", [NSString stringWithFormat:@"=> %@", number]);
            //NSLog(@"%@", [NSString stringWithFormat:@"=== %c === %@",ellipsis, number]);
            [muString insertString:[NSString stringWithFormat:@"%c",ellipsis] atIndex:0];
            }
        '''
        if isNegative:
            return "-" + muString
        else:
            return muString


    def encodeDoubleValue(self, dVal):
        """
        @param: A value with a double format
        """
        isNegative = False;
        if dVal < 0:
            isNegative = True;
            dVal *= -1;

        # double -> string に変換の際に、余計な0を表示しないようにする処理
        strVal = str(dVal);
        vals = strVal.split(".");

        # 整数部分の計算
        strIntVal = self.encodeLongValue(int(vals[0]));
        if len(vals) == 1:
            if isNegative:
                return "-"+strIntVal;
            else:
                return strIntVal;

        # 小数部分の計算
        # print(vals)
        strDecVal = self.encodeLongValue(int(vals[1]));
        # print(strDecVal)

        # ゼロのカウント
        zeros = "";
        aZero = self.encodeLongValue(0);
        for i,aVal in enumerate(vals[1]):
            #print(aVal);
            if aVal=="0":
                zeros = zeros + aZero;

        # print("hello world!");
        if isNegative:
            return "-"+strIntVal+"."+zeros+strDecVal;
        else:
            return strIntVal+"."+zeros+strDecVal;


    def decodeLongValue(self, sVal):
        """
        @param: Positional notation
        """
        isNegative = False;
        if sVal[0:1] == "-":
            isNegative = True;

        totalVal = 0;
        for i in reversed(range(len(sVal))):
            v = math.pow(self.PN, len(sVal)-i-1) * int(self.REVERSE_TABLE[ord(sVal[i])]);
            totalVal += v;
            # print( math.pow(self.PN, len(sVal)) * self.REVERSE_TABLE[ord(v)] );

        if isNegative:
            return int(totalVal) * -1;
        else:
            return int(totalVal);


    def decodeDoubleValue(self, sVal):
        """
        @param: A value with a string format
        """
        isNegative = False;
        if sVal[0:1] == "-":
            isNegative = True;

        ## split a value at a dot.
        vals = sVal.split(".");
        if len(vals) == 1:
            intVal = self.decodeLongValue(vals[0]);
        elif len(vals) == 2:
            intVal = self.decodeLongValue(vals[0]);
            ### generate zeors
            aZero = self.encodeLongValue(0);
            zeros = "";
            for aVal in list(vals[1]):
                if aVal == aZero:
                    zeros +="0";
                else:
                    break;
            #decVal = vals[1][len(zeros):];
            decVal = self.decodeLongValue(vals[1][len(zeros):]);

            if isNegative and intVal >= 0:
                return float("-"+str(intVal)+"."+zeros+str(decVal));
            else:
                return float(str(intVal)+"."+zeros+str(decVal));

        else:
            return self.decodeLongValue(sVal);

class SenbayFormat:
    RESERVED_KEYS =  {"TIME":"0","LONG":"1","LATI":"2",
                      "ALTI":"3","ACCX":"4","ACCY":"5",
                      "ACCZ":"6","YAW":"7" ,"ROLL":"8",
                      "PITC":"9","HEAD":"A","SPEE":"B",
                      "BRIG":"C","AIRP":"D","HTBT":"E"};

    PN = 121;
    basex = None;

    def __init__(self, positionalNotation=121):
        self.PN = positionalNotation;
        self.basex = BaseX(self.PN);

    def getReservedShortKey(self, key):
        for k,v in self.RESERVED_KEYS.items():
            if k==key:
                return v;
        return "";

    def getReservedOriginalKey(self, key):
        for k,v in self.RESERVED_KEYS.items():
            if v==key:
                return k;
        return "";


    def encode(self, text):
        encodedText = "";
        elements = text.split(",");
        count = 0;

        for element in elements:
            #print(element);
            contents = element.split(":");
            if len(contents)>1:
                key = contents[0];
                val = ""
                for con in contents[1:]:
                    if val == "":
                        val = con;
                    else:
                        val = val + ":" + con;
                #print(val)
                ## key
                reservedKey = self.getReservedShortKey(key)
                isReservedKey = False;
                if len(reservedKey) != 0:
                    isReservedKey = True;
                    key = reservedKey;
                ## val
                if len(val) > 0:
                    if val[:1] != "'":
                        if isReservedKey:
                            encodedText = '%s%s%s' % (encodedText,key,self.basex.encodeDoubleValue(float(val)));
                        else:
                            encodedText = '%s%s:%s' % (encodedText,key,self.basex.encodeDoubleValue(float(val)));
                    else:
                        if isReservedKey:
                            encodedText = '%s%s%s' % (encodedText,key,val);
                        else:
                            encodedText = '%s%s:%s' % (encodedText,key,val);
            if count<len(elements)-1:
                count = count + 1;
                encodedText = encodedText + ",";
        return encodedText;

    def decode(self, text):
        decodedText = "";
        count = 0;
        elements = text.split(",");
        for element in elements:
            key = "";
            val = "";
            contents = element.split(":");
            if len(contents) > 1: ## compressed
                key = contents[0];
                for con in contents[1:]:
                    if val == "":
                        val = con;
                    else:
                        val = val + ":" + con;
                #print(val)

            else: ## uncpressed
                key = contents[0][:1];
                val = contents[0][1:];


            ## key
            reservedKey = self.getReservedOriginalKey(key);
            if len(reservedKey) != 0:
                key = reservedKey;

            if val[:1] != "'":
                decodedText = '%s%s:%s' % (decodedText,key,self.basex.decodeDoubleValue(val));
            else:
                decodedText = '%s%s:%s' % (decodedText,key,val);

            if count<len(elements)-1:
                count = count + 1;
                decodedText = decodedText + ",";
        return decodedText;

class SenbayData:
    senbayData = {};
    PN = 121;
    SF = SenbayFormat();

    def __init__(self, pn=121):
        self.PN = pn;
        self.SF = SenbayFormat(pn);
        # print("init the SenbayData library");

    def add_number(self, key, value):
        #self.senbayData.update({key:value});
        if key is not None and value is not None:
            self.senbayData[key] = value;

    def add_text(self, key, value):
        if key is not None and value is not None:
            self.senbayData[key] = "'"+value+"'";

    def clear(self):
        self.senbayData = {};

    def encode(self, compress=False):
        formattedData = "";
        count = 0;
        for k,v in self.senbayData.items():
            formattedData = '%s%s:%s' % (formattedData,k,v);
            if count<len(self.senbayData)-1:
                count = count + 1;
                formattedData = formattedData + ",";
        #print("-->" + formattedData)
        if compress:
            return "V:4,"+self.SF.encode(formattedData);
        else:
            return "V:3,"+formattedData;

    def decode(self,text):
        senbayDict = {};
        elements = text.split(",");
        isCompress = False
        for element in elements:
            contents = element.split(":")
            if len(contents)>1 and contents[0]=='V' and contents[1]=='4':
                isCompress = True;
                break;
        if isCompress:
            text = self.SF.decode(text);

        elements = text.split(",");
        #print(text)
        # i = 0
        #for element in elements:
        #    print(i, element)
        #    i = i + 1;
        try:
            for element in elements:
                # print(element)
                contents = element.split(":")
                if len(contents)>1:
                    #print(contents)
                    key = contents[0];
                    value = "";
                    for con in contents[1:]:
                        if value == "":
                            value = con;
                        else:
                            value = value +":"+ con;
                        #print(value);

                    # print("k:" + key + ",v:" + value)
                    if value is None:
                        print("The value is None!");
                    if key != 'V':
                        if value != "None":
                            if value[:1] == "'":
                                senbayDict[key] = value[1:len(value)-1];
                            else:
                                #if value is not None or key is not None:
                                senbayDict[key] = float(value);
        except ValueError:
            print("error");
        return senbayDict;
