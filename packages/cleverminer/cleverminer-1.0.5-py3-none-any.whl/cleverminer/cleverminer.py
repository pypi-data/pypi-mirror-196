import sys #line:31
import time #line:32
import copy #line:33
from time import strftime #line:35
from time import gmtime #line:36
import pandas as pd #line:38
import numpy #line:39
from pandas .api .types import CategoricalDtype #line:40
class cleverminer :#line:42
    version_string ="1.0.5"#line:44
    def __init__ (O0OOOO0O0O00O0OO0 ,**O0O000OO0O0O0OOOO ):#line:46
        O0OOOO0O0O00O0OO0 ._print_disclaimer ()#line:47
        O0OOOO0O0O00O0OO0 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:56
        O0OOOO0O0O00O0OO0 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True }#line:62
        O0OOOO0O0O00O0OO0 .kwargs =None #line:63
        if len (O0O000OO0O0O0OOOO )>0 :#line:64
            O0OOOO0O0O00O0OO0 .kwargs =O0O000OO0O0O0OOOO #line:65
        O0OOOO0O0O00O0OO0 .verbosity ={}#line:66
        O0OOOO0O0O00O0OO0 .verbosity ['debug']=False #line:67
        O0OOOO0O0O00O0OO0 .verbosity ['print_rules']=False #line:68
        O0OOOO0O0O00O0OO0 .verbosity ['print_hashes']=True #line:69
        O0OOOO0O0O00O0OO0 .verbosity ['last_hash_time']=0 #line:70
        O0OOOO0O0O00O0OO0 .verbosity ['hint']=False #line:71
        if "opts"in O0O000OO0O0O0OOOO :#line:72
            O0OOOO0O0O00O0OO0 ._set_opts (O0O000OO0O0O0OOOO .get ("opts"))#line:73
        if "opts"in O0O000OO0O0O0OOOO :#line:74
            if "verbose"in O0O000OO0O0O0OOOO .get ('opts'):#line:75
                O000OOOO0OO00OOO0 =O0O000OO0O0O0OOOO .get ('opts').get ('verbose')#line:76
                if O000OOOO0OO00OOO0 .upper ()=='FULL':#line:77
                    O0OOOO0O0O00O0OO0 .verbosity ['debug']=True #line:78
                    O0OOOO0O0O00O0OO0 .verbosity ['print_rules']=True #line:79
                    O0OOOO0O0O00O0OO0 .verbosity ['print_hashes']=False #line:80
                    O0OOOO0O0O00O0OO0 .verbosity ['hint']=True #line:81
                elif O000OOOO0OO00OOO0 .upper ()=='RULES':#line:82
                    O0OOOO0O0O00O0OO0 .verbosity ['debug']=False #line:83
                    O0OOOO0O0O00O0OO0 .verbosity ['print_rules']=True #line:84
                    O0OOOO0O0O00O0OO0 .verbosity ['print_hashes']=True #line:85
                    O0OOOO0O0O00O0OO0 .verbosity ['hint']=True #line:86
                elif O000OOOO0OO00OOO0 .upper ()=='HINT':#line:87
                    O0OOOO0O0O00O0OO0 .verbosity ['debug']=False #line:88
                    O0OOOO0O0O00O0OO0 .verbosity ['print_rules']=False #line:89
                    O0OOOO0O0O00O0OO0 .verbosity ['print_hashes']=True #line:90
                    O0OOOO0O0O00O0OO0 .verbosity ['last_hash_time']=0 #line:91
                    O0OOOO0O0O00O0OO0 .verbosity ['hint']=True #line:92
                elif O000OOOO0OO00OOO0 .upper ()=='DEBUG':#line:93
                    O0OOOO0O0O00O0OO0 .verbosity ['debug']=True #line:94
                    O0OOOO0O0O00O0OO0 .verbosity ['print_rules']=True #line:95
                    O0OOOO0O0O00O0OO0 .verbosity ['print_hashes']=True #line:96
                    O0OOOO0O0O00O0OO0 .verbosity ['last_hash_time']=0 #line:97
                    O0OOOO0O0O00O0OO0 .verbosity ['hint']=True #line:98
        O0OOOO0O0O00O0OO0 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:99
        if not (O0OOOO0O0O00O0OO0 ._is_py310 ):#line:100
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:101
        else :#line:102
            if (O0OOOO0O0O00O0OO0 .verbosity ['debug']):#line:103
                print ("Python 3.10+ detected.")#line:104
        O0OOOO0O0O00O0OO0 ._initialized =False #line:105
        O0OOOO0O0O00O0OO0 ._init_data ()#line:106
        O0OOOO0O0O00O0OO0 ._init_task ()#line:107
        if len (O0O000OO0O0O0OOOO )>0 :#line:108
            if "df"in O0O000OO0O0O0OOOO :#line:109
                O0OOOO0O0O00O0OO0 ._prep_data (O0O000OO0O0O0OOOO .get ("df"))#line:110
            else :#line:111
                print ("Missing dataframe. Cannot initialize.")#line:112
                O0OOOO0O0O00O0OO0 ._initialized =False #line:113
                return #line:114
            OO000OOO00OOO0O00 =O0O000OO0O0O0OOOO .get ("proc",None )#line:115
            if not (OO000OOO00OOO0O00 ==None ):#line:116
                O0OOOO0O0O00O0OO0 ._calculate (**O0O000OO0O0O0OOOO )#line:117
            else :#line:119
                if O0OOOO0O0O00O0OO0 .verbosity ['debug']:#line:120
                    print ("INFO: just initialized")#line:121
        O0OOOO0O0O00O0OO0 ._initialized =True #line:122
    def _set_opts (O0OO0O00O000O0OOO ,O000000O0OOO0OOO0 ):#line:124
        if "no_optimizations"in O000000O0OOO0OOO0 :#line:125
            O0OO0O00O000O0OOO .options ['optimizations']=not (O000000O0OOO0OOO0 ['no_optimizations'])#line:126
            print ("No optimization will be made.")#line:127
        if "max_rules"in O000000O0OOO0OOO0 :#line:128
            O0OO0O00O000O0OOO .options ['max_rules']=O000000O0OOO0OOO0 ['max_rules']#line:129
        if "max_categories"in O000000O0OOO0OOO0 :#line:130
            O0OO0O00O000O0OOO .options ['max_categories']=O000000O0OOO0OOO0 ['max_categories']#line:131
            if O0OO0O00O000O0OOO .verbosity ['debug']==True :#line:132
                print (f"Maximum number of categories set to {O0OO0O00O000O0OOO.options['max_categories']}")#line:133
        if "no_automatic_data_conversions"in O000000O0OOO0OOO0 :#line:134
            O0OO0O00O000O0OOO .options ['automatic_data_conversions']=not (O000000O0OOO0OOO0 ['no_automatic_data_conversions'])#line:135
            print ("No automatic data conversions will be made.")#line:136
    def _init_data (OOOO0O00OOOO0OOO0 ):#line:139
        OOOO0O00OOOO0OOO0 .data ={}#line:141
        OOOO0O00OOOO0OOO0 .data ["varname"]=[]#line:142
        OOOO0O00OOOO0OOO0 .data ["catnames"]=[]#line:143
        OOOO0O00OOOO0OOO0 .data ["vtypes"]=[]#line:144
        OOOO0O00OOOO0OOO0 .data ["dm"]=[]#line:145
        OOOO0O00OOOO0OOO0 .data ["rows_count"]=int (0 )#line:146
        OOOO0O00OOOO0OOO0 .data ["data_prepared"]=0 #line:147
    def _init_task (OO00OOO00O000OOO0 ):#line:149
        if "opts"in OO00OOO00O000OOO0 .kwargs :#line:151
            OO00OOO00O000OOO0 ._set_opts (OO00OOO00O000OOO0 .kwargs .get ("opts"))#line:152
        OO00OOO00O000OOO0 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:162
        OO00OOO00O000OOO0 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:166
        OO00OOO00O000OOO0 .rulelist =[]#line:167
        OO00OOO00O000OOO0 .stats ['total_cnt']=0 #line:169
        OO00OOO00O000OOO0 .stats ['total_valid']=0 #line:170
        OO00OOO00O000OOO0 .stats ['control_number']=0 #line:171
        OO00OOO00O000OOO0 .result ={}#line:172
        OO00OOO00O000OOO0 ._opt_base =None #line:173
        OO00OOO00O000OOO0 ._opt_relbase =None #line:174
        OO00OOO00O000OOO0 ._opt_base1 =None #line:175
        OO00OOO00O000OOO0 ._opt_relbase1 =None #line:176
        OO00OOO00O000OOO0 ._opt_base2 =None #line:177
        OO00OOO00O000OOO0 ._opt_relbase2 =None #line:178
        OO00O0O00O0O0O0OO =None #line:179
        if not (OO00OOO00O000OOO0 .kwargs ==None ):#line:180
            OO00O0O00O0O0O0OO =OO00OOO00O000OOO0 .kwargs .get ("quantifiers",None )#line:181
            if not (OO00O0O00O0O0O0OO ==None ):#line:182
                for O0OO00O0OO0000OO0 in OO00O0O00O0O0O0OO .keys ():#line:183
                    if O0OO00O0OO0000OO0 .upper ()=='BASE':#line:184
                        OO00OOO00O000OOO0 ._opt_base =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:185
                    if O0OO00O0OO0000OO0 .upper ()=='RELBASE':#line:186
                        OO00OOO00O000OOO0 ._opt_relbase =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:187
                    if (O0OO00O0OO0000OO0 .upper ()=='FRSTBASE')|(O0OO00O0OO0000OO0 .upper ()=='BASE1'):#line:188
                        OO00OOO00O000OOO0 ._opt_base1 =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:189
                    if (O0OO00O0OO0000OO0 .upper ()=='SCNDBASE')|(O0OO00O0OO0000OO0 .upper ()=='BASE2'):#line:190
                        OO00OOO00O000OOO0 ._opt_base2 =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:191
                    if (O0OO00O0OO0000OO0 .upper ()=='FRSTRELBASE')|(O0OO00O0OO0000OO0 .upper ()=='RELBASE1'):#line:192
                        OO00OOO00O000OOO0 ._opt_relbase1 =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:193
                    if (O0OO00O0OO0000OO0 .upper ()=='SCNDRELBASE')|(O0OO00O0OO0000OO0 .upper ()=='RELBASE2'):#line:194
                        OO00OOO00O000OOO0 ._opt_relbase2 =OO00O0O00O0O0O0OO .get (O0OO00O0OO0000OO0 )#line:195
            else :#line:196
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:197
        else :#line:198
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:199
    def mine (OOO0O0OO00OOOO0O0 ,**OO000O000000OO00O ):#line:202
        if not (OOO0O0OO00OOOO0O0 ._initialized ):#line:203
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:204
            return #line:205
        OOO0O0OO00OOOO0O0 .kwargs =None #line:206
        if len (OO000O000000OO00O )>0 :#line:207
            OOO0O0OO00OOOO0O0 .kwargs =OO000O000000OO00O #line:208
        OOO0O0OO00OOOO0O0 ._init_task ()#line:209
        if len (OO000O000000OO00O )>0 :#line:210
            O0OO00OOO0O0OO0O0 =OO000O000000OO00O .get ("proc",None )#line:211
            if not (O0OO00OOO0O0OO0O0 ==None ):#line:212
                OOO0O0OO00OOOO0O0 ._calc_all (**OO000O000000OO00O )#line:213
            else :#line:214
                print ("Rule mining procedure missing")#line:215
    def _get_ver (O00OO00OO00O00OOO ):#line:218
        return O00OO00OO00O00OOO .version_string #line:219
    def _print_disclaimer (OO0OO0OO0000OO000 ):#line:221
        print (f"Cleverminer version {OO0OO0OO0000OO000._get_ver()}.")#line:223
    def _automatic_data_conversions (OOOO0O0OO000O0OOO ,O0000O00OOOOO0O0O ):#line:229
        print ("Automatically reordering numeric categories ...")#line:230
        for O0OOOOO0OOOOOOO00 in range (len (O0000O00OOOOO0O0O .columns )):#line:231
            if OOOO0O0OO000O0OOO .verbosity ['debug']:#line:232
                print (f"#{O0OOOOO0OOOOOOO00}: {O0000O00OOOOO0O0O.columns[O0OOOOO0OOOOOOO00]} : {O0000O00OOOOO0O0O.dtypes[O0OOOOO0OOOOOOO00]}.")#line:233
            try :#line:234
                O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]]=O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]].astype (str ).astype (float )#line:235
                if OOOO0O0OO000O0OOO .verbosity ['debug']:#line:236
                    print (f"CONVERTED TO FLOATS #{O0OOOOO0OOOOOOO00}: {O0000O00OOOOO0O0O.columns[O0OOOOO0OOOOOOO00]} : {O0000O00OOOOO0O0O.dtypes[O0OOOOO0OOOOOOO00]}.")#line:237
                O000OO00O0000OO0O =pd .unique (O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]])#line:238
                O0000O0OO0O000OOO =True #line:239
                for O0OO00O00O0O0O0O0 in O000OO00O0000OO0O :#line:240
                    if O0OO00O00O0O0O0O0 %1 !=0 :#line:241
                        O0000O0OO0O000OOO =False #line:242
                if O0000O0OO0O000OOO :#line:243
                    O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]]=O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]].astype (int )#line:244
                    if OOOO0O0OO000O0OOO .verbosity ['debug']:#line:245
                        print (f"CONVERTED TO INT #{O0OOOOO0OOOOOOO00}: {O0000O00OOOOO0O0O.columns[O0OOOOO0OOOOOOO00]} : {O0000O00OOOOO0O0O.dtypes[O0OOOOO0OOOOOOO00]}.")#line:246
                OO00OOOO0000O0OOO =pd .unique (O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]])#line:247
                OOO0000OO000000O0 =CategoricalDtype (categories =OO00OOOO0000O0OOO .sort (),ordered =True )#line:248
                O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]]=O0000O00OOOOO0O0O [O0000O00OOOOO0O0O .columns [O0OOOOO0OOOOOOO00 ]].astype (OOO0000OO000000O0 )#line:249
                if OOOO0O0OO000O0OOO .verbosity ['debug']:#line:250
                    print (f"CONVERTED TO CATEGORY #{O0OOOOO0OOOOOOO00}: {O0000O00OOOOO0O0O.columns[O0OOOOO0OOOOOOO00]} : {O0000O00OOOOO0O0O.dtypes[O0OOOOO0OOOOOOO00]}.")#line:251
            except :#line:253
                if OOOO0O0OO000O0OOO .verbosity ['debug']:#line:254
                    print ("...cannot be converted to int")#line:255
        print ("Automatically reordering numeric categories ...done")#line:256
    def _prep_data (OOO0OO0OOO0O0OOOO ,OOO0O000OO0O0O000 ):#line:258
        print ("Starting data preparation ...")#line:259
        OOO0OO0OOO0O0OOOO ._init_data ()#line:260
        OOO0OO0OOO0O0OOOO .stats ['start_prep_time']=time .time ()#line:261
        if OOO0OO0OOO0O0OOOO .options ['automatic_data_conversions']:#line:262
            OOO0OO0OOO0O0OOOO ._automatic_data_conversions (OOO0O000OO0O0O000 )#line:263
        OOO0OO0OOO0O0OOOO .data ["rows_count"]=OOO0O000OO0O0O000 .shape [0 ]#line:264
        for O000OOOO0000O0000 in OOO0O000OO0O0O000 .select_dtypes (exclude =['category']).columns :#line:265
            OOO0O000OO0O0O000 [O000OOOO0000O0000 ]=OOO0O000OO0O0O000 [O000OOOO0000O0000 ].apply (str )#line:266
        try :#line:267
            O0O0OOO0OOO00O0O0 =pd .DataFrame .from_records ([(OOO0000OOO00OO000 ,OOO0O000OO0O0O000 [OOO0000OOO00OO000 ].nunique ())for OOO0000OOO00OO000 in OOO0O000OO0O0O000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:269
        except :#line:270
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:271
            OO0OOOO0OO00O0O0O =""#line:272
            try :#line:273
                for O000OOOO0000O0000 in OOO0O000OO0O0O000 .columns :#line:274
                    OO0OOOO0OO00O0O0O =O000OOOO0000O0000 #line:275
                    print (f"...column {O000OOOO0000O0000} has {int(OOO0O000OO0O0O000[O000OOOO0000O0000].nunique())} values")#line:276
            except :#line:277
                print (f"... detected : column {OO0OOOO0OO00O0O0O} has unsupported type: {type(OOO0O000OO0O0O000[O000OOOO0000O0000])}.")#line:278
                exit (1 )#line:279
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:280
            exit (1 )#line:281
        if OOO0OO0OOO0O0OOOO .verbosity ['hint']:#line:284
            print ("Quick profile of input data: unique value counts are:")#line:285
            print (O0O0OOO0OOO00O0O0 )#line:286
            for O000OOOO0000O0000 in OOO0O000OO0O0O000 .columns :#line:287
                if OOO0O000OO0O0O000 [O000OOOO0000O0000 ].nunique ()<OOO0OO0OOO0O0OOOO .options ['max_categories']:#line:288
                    OOO0O000OO0O0O000 [O000OOOO0000O0000 ]=OOO0O000OO0O0O000 [O000OOOO0000O0000 ].astype ('category')#line:289
                else :#line:290
                    print (f"WARNING: attribute {O000OOOO0000O0000} has more than {OOO0OO0OOO0O0OOOO.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:291
                    del OOO0O000OO0O0O000 [O000OOOO0000O0000 ]#line:292
        print ("Encoding columns into bit-form...")#line:293
        OOO00OOOO0O0OO000 =0 #line:294
        O0O0O0000OOOO00O0 =0 #line:295
        for O000OOOOOOO0O0OO0 in OOO0O000OO0O0O000 :#line:296
            if OOO0OO0OOO0O0OOOO .verbosity ['debug']:#line:298
                print ('Column: '+O000OOOOOOO0O0OO0 )#line:299
            OOO0OO0OOO0O0OOOO .data ["varname"].append (O000OOOOOOO0O0OO0 )#line:300
            O00O0O0OOO00O0000 =pd .get_dummies (OOO0O000OO0O0O000 [O000OOOOOOO0O0OO0 ])#line:301
            O000O0000O0OO0OO0 =0 #line:302
            if (OOO0O000OO0O0O000 .dtypes [O000OOOOOOO0O0OO0 ].name =='category'):#line:303
                O000O0000O0OO0OO0 =1 #line:304
            OOO0OO0OOO0O0OOOO .data ["vtypes"].append (O000O0000O0OO0OO0 )#line:305
            O0O00O0O0OOOOOO0O =0 #line:308
            O000O00O00OOOOO0O =[]#line:309
            O0O00000OO0OO000O =[]#line:310
            for OO00O0O00OO0O0OO0 in O00O0O0OOO00O0000 :#line:312
                if OOO0OO0OOO0O0OOOO .verbosity ['debug']:#line:314
                    print ('....category : '+str (OO00O0O00OO0O0OO0 )+" @ "+str (time .time ()))#line:315
                O000O00O00OOOOO0O .append (OO00O0O00OO0O0OO0 )#line:316
                OOO00OOO0O0O0O000 =int (0 )#line:317
                OOO00000OOO00OO0O =O00O0O0OOO00O0000 [OO00O0O00OO0O0OO0 ].values #line:318
                O00O000OO0O0OOO0O =numpy .packbits (OOO00000OOO00OO0O ,bitorder ='little')#line:320
                OOO00OOO0O0O0O000 =int .from_bytes (O00O000OO0O0OOO0O ,byteorder ='little')#line:321
                O0O00000OO0OO000O .append (OOO00OOO0O0O0O000 )#line:322
                O0O00O0O0OOOOOO0O +=1 #line:340
                O0O0O0000OOOO00O0 +=1 #line:341
            OOO0OO0OOO0O0OOOO .data ["catnames"].append (O000O00O00OOOOO0O )#line:343
            OOO0OO0OOO0O0OOOO .data ["dm"].append (O0O00000OO0OO000O )#line:344
        print ("Encoding columns into bit-form...done")#line:346
        if OOO0OO0OOO0O0OOOO .verbosity ['hint']:#line:347
            print (f"List of attributes for analysis is: {OOO0OO0OOO0O0OOOO.data['varname']}")#line:348
            print (f"List of category names for individual attributes is : {OOO0OO0OOO0O0OOOO.data['catnames']}")#line:349
        if OOO0OO0OOO0O0OOOO .verbosity ['debug']:#line:350
            print (f"List of vtypes is (all should be 1) : {OOO0OO0OOO0O0OOOO.data['vtypes']}")#line:351
        OOO0OO0OOO0O0OOOO .data ["data_prepared"]=1 #line:353
        print ("Data preparation finished.")#line:354
        if OOO0OO0OOO0O0OOOO .verbosity ['debug']:#line:355
            print ('Number of variables : '+str (len (OOO0OO0OOO0O0OOOO .data ["dm"])))#line:356
            print ('Total number of categories in all variables : '+str (O0O0O0000OOOO00O0 ))#line:357
        OOO0OO0OOO0O0OOOO .stats ['end_prep_time']=time .time ()#line:358
        if OOO0OO0OOO0O0OOOO .verbosity ['debug']:#line:359
            print ('Time needed for data preparation : ',str (OOO0OO0OOO0O0OOOO .stats ['end_prep_time']-OOO0OO0OOO0O0OOOO .stats ['start_prep_time']))#line:360
    def _bitcount (OO0OOO0000O0O00O0 ,OOO0000O0OO00000O ):#line:362
        O0O0OO0O0OOO000OO =None #line:363
        if (OO0OOO0000O0O00O0 ._is_py310 ):#line:364
            O0O0OO0O0OOO000OO =OOO0000O0OO00000O .bit_count ()#line:365
        else :#line:366
            O0O0OO0O0OOO000OO =bin (OOO0000O0OO00000O ).count ("1")#line:367
        return O0O0OO0O0OOO000OO #line:368
    def _verifyCF (O0OO00O00OO00OOO0 ,_OOOO000O0OOO0OOOO ):#line:371
        O0OOO000OOO0O0OOO =O0OO00O00OO00OOO0 ._bitcount (_OOOO000O0OOO0OOOO )#line:372
        OOO000O0O0OO0OO0O =[]#line:373
        OOOOO000OO00OOOOO =[]#line:374
        OO0O0O0O0000O0OO0 =0 #line:375
        O0O0O0000O00O0O00 =0 #line:376
        OO000OO000OO0O0OO =0 #line:377
        O0OO0O000O00OOOO0 =0 #line:378
        OOO0000O00O000000 =0 #line:379
        O0OO0O00OO00O00OO =0 #line:380
        O00O0OO0O0OO000OO =0 #line:381
        OO0O00O0000OO0O00 =0 #line:382
        O0OO0O0OOOO000000 =0 #line:383
        O00O000OOO0O00O00 =0 #line:384
        OOOO000OO0O000OOO =0 #line:385
        O0000O00O0O00000O =[]#line:386
        if ('aad_weights'in O0OO00O00OO00OOO0 .quantifiers ):#line:387
            O00O000OOO0O00O00 =1 #line:388
            O00OOO00OO00O000O =[]#line:389
            O0000O00O0O00000O =O0OO00O00OO00OOO0 .quantifiers .get ('aad_weights')#line:390
        OOO00OOOO000OOOO0 =O0OO00O00OO00OOO0 .data ["dm"][O0OO00O00OO00OOO0 .data ["varname"].index (O0OO00O00OO00OOO0 .kwargs .get ('target'))]#line:391
        for O0OOO00O0O0000OOO in range (len (OOO00OOOO000OOOO0 )):#line:392
            O0O0O0000O00O0O00 =OO0O0O0O0000O0OO0 #line:394
            OO0O0O0O0000O0OO0 =O0OO00O00OO00OOO0 ._bitcount (_OOOO000O0OOO0OOOO &OOO00OOOO000OOOO0 [O0OOO00O0O0000OOO ])#line:395
            OOO000O0O0OO0OO0O .append (OO0O0O0O0000O0OO0 )#line:396
            if O0OOO00O0O0000OOO >0 :#line:397
                if (OO0O0O0O0000O0OO0 >O0O0O0000O00O0O00 ):#line:398
                    if (OO000OO000OO0O0OO ==1 ):#line:399
                        OO0O00O0000OO0O00 +=1 #line:400
                    else :#line:401
                        OO0O00O0000OO0O00 =1 #line:402
                    if OO0O00O0000OO0O00 >O0OO0O000O00OOOO0 :#line:403
                        O0OO0O000O00OOOO0 =OO0O00O0000OO0O00 #line:404
                    OO000OO000OO0O0OO =1 #line:405
                    O0OO0O00OO00O00OO +=1 #line:406
                if (OO0O0O0O0000O0OO0 <O0O0O0000O00O0O00 ):#line:407
                    if (OO000OO000OO0O0OO ==-1 ):#line:408
                        O0OO0O0OOOO000000 +=1 #line:409
                    else :#line:410
                        O0OO0O0OOOO000000 =1 #line:411
                    if O0OO0O0OOOO000000 >OOO0000O00O000000 :#line:412
                        OOO0000O00O000000 =O0OO0O0OOOO000000 #line:413
                    OO000OO000OO0O0OO =-1 #line:414
                    O00O0OO0O0OO000OO +=1 #line:415
                if (OO0O0O0O0000O0OO0 ==O0O0O0000O00O0O00 ):#line:416
                    OO000OO000OO0O0OO =0 #line:417
                    O0OO0O0OOOO000000 =0 #line:418
                    OO0O00O0000OO0O00 =0 #line:419
            if (O00O000OOO0O00O00 ):#line:421
                OO00O0OOOO0OO0O0O =O0OO00O00OO00OOO0 ._bitcount (OOO00OOOO000OOOO0 [O0OOO00O0O0000OOO ])#line:422
                O00OOO00OO00O000O .append (OO00O0OOOO0OO0O0O )#line:423
        if (O00O000OOO0O00O00 &sum (OOO000O0O0OO0OO0O )>0 ):#line:425
            for O0OOO00O0O0000OOO in range (len (OOO00OOOO000OOOO0 )):#line:426
                if O00OOO00OO00O000O [O0OOO00O0O0000OOO ]>0 :#line:427
                    if OOO000O0O0OO0OO0O [O0OOO00O0O0000OOO ]/sum (OOO000O0O0OO0OO0O )>O00OOO00OO00O000O [O0OOO00O0O0000OOO ]/sum (O00OOO00OO00O000O ):#line:429
                        OOOO000OO0O000OOO +=O0000O00O0O00000O [O0OOO00O0O0000OOO ]*((OOO000O0O0OO0OO0O [O0OOO00O0O0000OOO ]/sum (OOO000O0O0OO0OO0O ))/(O00OOO00OO00O000O [O0OOO00O0O0000OOO ]/sum (O00OOO00OO00O000O ))-1 )#line:430
        OO0O00OOO0OOO0OO0 =True #line:433
        for OOOOOO0OO0OO0O0O0 in O0OO00O00OO00OOO0 .quantifiers .keys ():#line:434
            if OOOOOO0OO0OO0O0O0 .upper ()=='BASE':#line:435
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=O0OOO000OOO0O0OOO )#line:436
            if OOOOOO0OO0OO0O0O0 .upper ()=='RELBASE':#line:437
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=O0OOO000OOO0O0OOO *1.0 /O0OO00O00OO00OOO0 .data ["rows_count"])#line:438
            if OOOOOO0OO0OO0O0O0 .upper ()=='S_UP':#line:439
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=O0OO0O000O00OOOO0 )#line:440
            if OOOOOO0OO0OO0O0O0 .upper ()=='S_DOWN':#line:441
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=OOO0000O00O000000 )#line:442
            if OOOOOO0OO0OO0O0O0 .upper ()=='S_ANY_UP':#line:443
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=O0OO0O000O00OOOO0 )#line:444
            if OOOOOO0OO0OO0O0O0 .upper ()=='S_ANY_DOWN':#line:445
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=OOO0000O00O000000 )#line:446
            if OOOOOO0OO0OO0O0O0 .upper ()=='MAX':#line:447
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=max (OOO000O0O0OO0OO0O ))#line:448
            if OOOOOO0OO0OO0O0O0 .upper ()=='MIN':#line:449
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=min (OOO000O0O0OO0OO0O ))#line:450
            if OOOOOO0OO0OO0O0O0 .upper ()=='RELMAX':#line:451
                if sum (OOO000O0O0OO0OO0O )>0 :#line:452
                    OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=max (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O ))#line:453
                else :#line:454
                    OO0O00OOO0OOO0OO0 =False #line:455
            if OOOOOO0OO0OO0O0O0 .upper ()=='RELMAX_LEQ':#line:456
                if sum (OOO000O0O0OO0OO0O )>0 :#line:457
                    OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )>=max (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O ))#line:458
                else :#line:459
                    OO0O00OOO0OOO0OO0 =False #line:460
            if OOOOOO0OO0OO0O0O0 .upper ()=='RELMIN':#line:461
                if sum (OOO000O0O0OO0OO0O )>0 :#line:462
                    OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=min (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O ))#line:463
                else :#line:464
                    OO0O00OOO0OOO0OO0 =False #line:465
            if OOOOOO0OO0OO0O0O0 .upper ()=='RELMIN_LEQ':#line:466
                if sum (OOO000O0O0OO0OO0O )>0 :#line:467
                    OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )>=min (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O ))#line:468
                else :#line:469
                    OO0O00OOO0OOO0OO0 =False #line:470
            if OOOOOO0OO0OO0O0O0 .upper ()=='AAD':#line:471
                OO0O00OOO0OOO0OO0 =OO0O00OOO0OOO0OO0 and (O0OO00O00OO00OOO0 .quantifiers .get (OOOOOO0OO0OO0O0O0 )<=OOOO000OO0O000OOO )#line:472
        O00OOO0O0OO000O0O ={}#line:474
        if OO0O00OOO0OOO0OO0 ==True :#line:475
            O0OO00O00OO00OOO0 .stats ['total_valid']+=1 #line:477
            O00OOO0O0OO000O0O ["base"]=O0OOO000OOO0O0OOO #line:478
            O00OOO0O0OO000O0O ["rel_base"]=O0OOO000OOO0O0OOO *1.0 /O0OO00O00OO00OOO0 .data ["rows_count"]#line:479
            O00OOO0O0OO000O0O ["s_up"]=O0OO0O000O00OOOO0 #line:480
            O00OOO0O0OO000O0O ["s_down"]=OOO0000O00O000000 #line:481
            O00OOO0O0OO000O0O ["s_any_up"]=O0OO0O00OO00O00OO #line:482
            O00OOO0O0OO000O0O ["s_any_down"]=O00O0OO0O0OO000OO #line:483
            O00OOO0O0OO000O0O ["max"]=max (OOO000O0O0OO0OO0O )#line:484
            O00OOO0O0OO000O0O ["min"]=min (OOO000O0O0OO0OO0O )#line:485
            if sum (OOO000O0O0OO0OO0O )>0 :#line:488
                O00OOO0O0OO000O0O ["rel_max"]=max (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O )#line:489
                O00OOO0O0OO000O0O ["rel_min"]=min (OOO000O0O0OO0OO0O )*1.0 /sum (OOO000O0O0OO0OO0O )#line:490
            else :#line:491
                O00OOO0O0OO000O0O ["rel_max"]=0 #line:492
                O00OOO0O0OO000O0O ["rel_min"]=0 #line:493
            O00OOO0O0OO000O0O ["hist"]=OOO000O0O0OO0OO0O #line:494
            if O00O000OOO0O00O00 :#line:495
                O00OOO0O0OO000O0O ["aad"]=OOOO000OO0O000OOO #line:496
                O00OOO0O0OO000O0O ["hist_full"]=O00OOO00OO00O000O #line:497
                O00OOO0O0OO000O0O ["rel_hist"]=[O00O00000O000O0OO /sum (OOO000O0O0OO0OO0O )for O00O00000O000O0OO in OOO000O0O0OO0OO0O ]#line:498
                O00OOO0O0OO000O0O ["rel_hist_full"]=[O0O00OO0OO0O0OO00 /sum (O00OOO00OO00O000O )for O0O00OO0OO0O0OO00 in O00OOO00OO00O000O ]#line:499
        return OO0O00OOO0OOO0OO0 ,O00OOO0O0OO000O0O #line:501
    def _verifyUIC (OOOO00OO0000O000O ,_OO00OOOO0OO0OO00O ):#line:503
        O0OOO0OOO000000OO ={}#line:504
        O00O0OOOO000000OO =0 #line:505
        for OOO0OO00OO0OO0O00 in OOOO00OO0000O000O .task_actinfo ['cedents']:#line:506
            O0OOO0OOO000000OO [OOO0OO00OO0OO0O00 ['cedent_type']]=OOO0OO00OO0OO0O00 ['filter_value']#line:508
            O00O0OOOO000000OO =O00O0OOOO000000OO +1 #line:509
        OOO0O0O0OO0OO000O =OOOO00OO0000O000O ._bitcount (_OO00OOOO0OO0OO00O )#line:511
        O0O0OOO0OO000000O =[]#line:512
        O0O000OO00OO00OO0 =0 #line:513
        O00OO0OOOO000O00O =0 #line:514
        OOOOOOO0O0O0000OO =0 #line:515
        O000O000O00O0O0O0 =[]#line:516
        OO0OOOOOO0O0000O0 =[]#line:517
        if ('aad_weights'in OOOO00OO0000O000O .quantifiers ):#line:518
            O000O000O00O0O0O0 =OOOO00OO0000O000O .quantifiers .get ('aad_weights')#line:519
            O00OO0OOOO000O00O =1 #line:520
        OOO0O00OOOO00O0OO =OOOO00OO0000O000O .data ["dm"][OOOO00OO0000O000O .data ["varname"].index (OOOO00OO0000O000O .kwargs .get ('target'))]#line:521
        for O0OO00OO0O0O00OO0 in range (len (OOO0O00OOOO00O0OO )):#line:522
            O0000OOO000O0OOOO =O0O000OO00OO00OO0 #line:524
            O0O000OO00OO00OO0 =OOOO00OO0000O000O ._bitcount (_OO00OOOO0OO0OO00O &OOO0O00OOOO00O0OO [O0OO00OO0O0O00OO0 ])#line:525
            O0O0OOO0OO000000O .append (O0O000OO00OO00OO0 )#line:526
            OO00OO000OOOO0000 =OOOO00OO0000O000O ._bitcount (O0OOO0OOO000000OO ['cond']&OOO0O00OOOO00O0OO [O0OO00OO0O0O00OO0 ])#line:529
            OO0OOOOOO0O0000O0 .append (OO00OO000OOOO0000 )#line:530
        if (O00OO0OOOO000O00O &sum (O0O0OOO0OO000000O )>0 ):#line:532
            for O0OO00OO0O0O00OO0 in range (len (OOO0O00OOOO00O0OO )):#line:533
                if OO0OOOOOO0O0000O0 [O0OO00OO0O0O00OO0 ]>0 :#line:534
                    if O0O0OOO0OO000000O [O0OO00OO0O0O00OO0 ]/sum (O0O0OOO0OO000000O )>OO0OOOOOO0O0000O0 [O0OO00OO0O0O00OO0 ]/sum (OO0OOOOOO0O0000O0 ):#line:536
                        OOOOOOO0O0O0000OO +=O000O000O00O0O0O0 [O0OO00OO0O0O00OO0 ]*((O0O0OOO0OO000000O [O0OO00OO0O0O00OO0 ]/sum (O0O0OOO0OO000000O ))/(OO0OOOOOO0O0000O0 [O0OO00OO0O0O00OO0 ]/sum (OO0OOOOOO0O0000O0 ))-1 )#line:537
        OOO000O000OO0O0O0 =True #line:540
        for O00O0O00000O00O00 in OOOO00OO0000O000O .quantifiers .keys ():#line:541
            if O00O0O00000O00O00 .upper ()=='BASE':#line:542
                OOO000O000OO0O0O0 =OOO000O000OO0O0O0 and (OOOO00OO0000O000O .quantifiers .get (O00O0O00000O00O00 )<=OOO0O0O0OO0OO000O )#line:543
            if O00O0O00000O00O00 .upper ()=='RELBASE':#line:544
                OOO000O000OO0O0O0 =OOO000O000OO0O0O0 and (OOOO00OO0000O000O .quantifiers .get (O00O0O00000O00O00 )<=OOO0O0O0OO0OO000O *1.0 /OOOO00OO0000O000O .data ["rows_count"])#line:545
            if O00O0O00000O00O00 .upper ()=='AAD_SCORE':#line:546
                OOO000O000OO0O0O0 =OOO000O000OO0O0O0 and (OOOO00OO0000O000O .quantifiers .get (O00O0O00000O00O00 )<=OOOOOOO0O0O0000OO )#line:547
        OOO0OOOOO00OO0O00 ={}#line:549
        if OOO000O000OO0O0O0 ==True :#line:550
            OOOO00OO0000O000O .stats ['total_valid']+=1 #line:552
            OOO0OOOOO00OO0O00 ["base"]=OOO0O0O0OO0OO000O #line:553
            OOO0OOOOO00OO0O00 ["rel_base"]=OOO0O0O0OO0OO000O *1.0 /OOOO00OO0000O000O .data ["rows_count"]#line:554
            OOO0OOOOO00OO0O00 ["hist"]=O0O0OOO0OO000000O #line:555
            OOO0OOOOO00OO0O00 ["aad_score"]=OOOOOOO0O0O0000OO #line:557
            OOO0OOOOO00OO0O00 ["hist_cond"]=OO0OOOOOO0O0000O0 #line:558
            OOO0OOOOO00OO0O00 ["rel_hist"]=[OO00O00000O000O0O /sum (O0O0OOO0OO000000O )for OO00O00000O000O0O in O0O0OOO0OO000000O ]#line:559
            OOO0OOOOO00OO0O00 ["rel_hist_cond"]=[O00OOO0O000O0O0OO /sum (OO0OOOOOO0O0000O0 )for O00OOO0O000O0O0OO in OO0OOOOOO0O0000O0 ]#line:560
        return OOO000O000OO0O0O0 ,OOO0OOOOO00OO0O00 #line:562
    def _verify4ft (OOO0OO00OO00OO000 ,_O00O00O000O0O000O ):#line:564
        O00OOOO000OOO000O ={}#line:565
        OO0OO000OO0OO00O0 =0 #line:566
        for O00OOO00OOOO000OO in OOO0OO00OO00OO000 .task_actinfo ['cedents']:#line:567
            O00OOOO000OOO000O [O00OOO00OOOO000OO ['cedent_type']]=O00OOO00OOOO000OO ['filter_value']#line:569
            OO0OO000OO0OO00O0 =OO0OO000OO0OO00O0 +1 #line:570
        OO0OOOO0OOOOO0OOO =OOO0OO00OO00OO000 ._bitcount (O00OOOO000OOO000O ['ante']&O00OOOO000OOO000O ['succ']&O00OOOO000OOO000O ['cond'])#line:572
        OO0OO00000O0OO000 =None #line:573
        OO0OO00000O0OO000 =0 #line:574
        if OO0OOOO0OOOOO0OOO >0 :#line:583
            OO0OO00000O0OO000 =OOO0OO00OO00OO000 ._bitcount (O00OOOO000OOO000O ['ante']&O00OOOO000OOO000O ['succ']&O00OOOO000OOO000O ['cond'])*1.0 /OOO0OO00OO00OO000 ._bitcount (O00OOOO000OOO000O ['ante']&O00OOOO000OOO000O ['cond'])#line:584
        OO0O0O0O000000O0O =1 <<OOO0OO00OO00OO000 .data ["rows_count"]#line:586
        OOOO00OO0000OOOOO =OOO0OO00OO00OO000 ._bitcount (O00OOOO000OOO000O ['ante']&O00OOOO000OOO000O ['succ']&O00OOOO000OOO000O ['cond'])#line:587
        O00O0OOO00O000000 =OOO0OO00OO00OO000 ._bitcount (O00OOOO000OOO000O ['ante']&~(OO0O0O0O000000O0O |O00OOOO000OOO000O ['succ'])&O00OOOO000OOO000O ['cond'])#line:588
        O00OOO00OOOO000OO =OOO0OO00OO00OO000 ._bitcount (~(OO0O0O0O000000O0O |O00OOOO000OOO000O ['ante'])&O00OOOO000OOO000O ['succ']&O00OOOO000OOO000O ['cond'])#line:589
        O0O00OOOO0000OOO0 =OOO0OO00OO00OO000 ._bitcount (~(OO0O0O0O000000O0O |O00OOOO000OOO000O ['ante'])&~(OO0O0O0O000000O0O |O00OOOO000OOO000O ['succ'])&O00OOOO000OOO000O ['cond'])#line:590
        O0000OOO00OOOOOOO =0 #line:591
        if (OOOO00OO0000OOOOO +O00O0OOO00O000000 )*(OOOO00OO0000OOOOO +O00OOO00OOOO000OO )>0 :#line:592
            O0000OOO00OOOOOOO =OOOO00OO0000OOOOO *(OOOO00OO0000OOOOO +O00O0OOO00O000000 +O00OOO00OOOO000OO +O0O00OOOO0000OOO0 )/(OOOO00OO0000OOOOO +O00O0OOO00O000000 )/(OOOO00OO0000OOOOO +O00OOO00OOOO000OO )-1 #line:593
        else :#line:594
            O0000OOO00OOOOOOO =None #line:595
        OO00O00O0O00OO0O0 =0 #line:596
        if (OOOO00OO0000OOOOO +O00O0OOO00O000000 )*(OOOO00OO0000OOOOO +O00OOO00OOOO000OO )>0 :#line:597
            OO00O00O0O00OO0O0 =1 -OOOO00OO0000OOOOO *(OOOO00OO0000OOOOO +O00O0OOO00O000000 +O00OOO00OOOO000OO +O0O00OOOO0000OOO0 )/(OOOO00OO0000OOOOO +O00O0OOO00O000000 )/(OOOO00OO0000OOOOO +O00OOO00OOOO000OO )#line:598
        else :#line:599
            OO00O00O0O00OO0O0 =None #line:600
        OOOO00OOOOO00OO00 =True #line:601
        for OOOO00O0O0OO0O00O in OOO0OO00OO00OO000 .quantifiers .keys ():#line:602
            if OOOO00O0O0OO0O00O .upper ()=='BASE':#line:603
                OOOO00OOOOO00OO00 =OOOO00OOOOO00OO00 and (OOO0OO00OO00OO000 .quantifiers .get (OOOO00O0O0OO0O00O )<=OO0OOOO0OOOOO0OOO )#line:604
            if OOOO00O0O0OO0O00O .upper ()=='RELBASE':#line:605
                OOOO00OOOOO00OO00 =OOOO00OOOOO00OO00 and (OOO0OO00OO00OO000 .quantifiers .get (OOOO00O0O0OO0O00O )<=OO0OOOO0OOOOO0OOO *1.0 /OOO0OO00OO00OO000 .data ["rows_count"])#line:606
            if (OOOO00O0O0OO0O00O .upper ()=='PIM')or (OOOO00O0O0OO0O00O .upper ()=='CONF'):#line:607
                OOOO00OOOOO00OO00 =OOOO00OOOOO00OO00 and (OOO0OO00OO00OO000 .quantifiers .get (OOOO00O0O0OO0O00O )<=OO0OO00000O0OO000 )#line:608
            if OOOO00O0O0OO0O00O .upper ()=='AAD':#line:609
                if O0000OOO00OOOOOOO !=None :#line:610
                    OOOO00OOOOO00OO00 =OOOO00OOOOO00OO00 and (OOO0OO00OO00OO000 .quantifiers .get (OOOO00O0O0OO0O00O )<=O0000OOO00OOOOOOO )#line:611
                else :#line:612
                    OOOO00OOOOO00OO00 =False #line:613
            if OOOO00O0O0OO0O00O .upper ()=='BAD':#line:614
                if OO00O00O0O00OO0O0 !=None :#line:615
                    OOOO00OOOOO00OO00 =OOOO00OOOOO00OO00 and (OOO0OO00OO00OO000 .quantifiers .get (OOOO00O0O0OO0O00O )<=OO00O00O0O00OO0O0 )#line:616
                else :#line:617
                    OOOO00OOOOO00OO00 =False #line:618
            O00000000OO00OO00 ={}#line:619
        if OOOO00OOOOO00OO00 ==True :#line:620
            OOO0OO00OO00OO000 .stats ['total_valid']+=1 #line:622
            O00000000OO00OO00 ["base"]=OO0OOOO0OOOOO0OOO #line:623
            O00000000OO00OO00 ["rel_base"]=OO0OOOO0OOOOO0OOO *1.0 /OOO0OO00OO00OO000 .data ["rows_count"]#line:624
            O00000000OO00OO00 ["conf"]=OO0OO00000O0OO000 #line:625
            O00000000OO00OO00 ["aad"]=O0000OOO00OOOOOOO #line:626
            O00000000OO00OO00 ["bad"]=OO00O00O0O00OO0O0 #line:627
            O00000000OO00OO00 ["fourfold"]=[OOOO00OO0000OOOOO ,O00O0OOO00O000000 ,O00OOO00OOOO000OO ,O0O00OOOO0000OOO0 ]#line:628
        return OOOO00OOOOO00OO00 ,O00000000OO00OO00 #line:632
    def _verifysd4ft (O000OO0O0O00000O0 ,_O00OOOO0O0O00OOOO ):#line:634
        O000O000OOO0OOO00 ={}#line:635
        O00OOOO000OOOOO0O =0 #line:636
        for O000OOO0000O0OOOO in O000OO0O0O00000O0 .task_actinfo ['cedents']:#line:637
            O000O000OOO0OOO00 [O000OOO0000O0OOOO ['cedent_type']]=O000OOO0000O0OOOO ['filter_value']#line:639
            O00OOOO000OOOOO0O =O00OOOO000OOOOO0O +1 #line:640
        OO0O0OO000OOO0OOO =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:642
        OOO00O000OOOO0OO0 =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:643
        O0O00OO0OO0OOOO0O =None #line:644
        O0OO000OOOO0O00OO =0 #line:645
        O000000O0000OO0OO =0 #line:646
        if OO0O0OO000OOO0OOO >0 :#line:655
            O0OO000OOOO0O00OO =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])*1.0 /O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:656
        if OOO00O000OOOO0OO0 >0 :#line:657
            O000000O0000OO0OO =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])*1.0 /O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:658
        OO0O0000OOOOO0O00 =1 <<O000OO0O0O00000O0 .data ["rows_count"]#line:660
        O0OO00OOOO0000O0O =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:661
        OO000OO0000O0OO00 =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['succ'])&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:662
        OO0OOO0O0O00OO0OO =O000OO0O0O00000O0 ._bitcount (~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['ante'])&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:663
        O00OO0000O0O0O000 =O000OO0O0O00000O0 ._bitcount (~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['ante'])&~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['succ'])&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['frst'])#line:664
        O00000O00O00000O0 =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:665
        O0000O00O0OOO0O00 =O000OO0O0O00000O0 ._bitcount (O000O000OOO0OOO00 ['ante']&~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['succ'])&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:666
        O0OO0O000O0000OO0 =O000OO0O0O00000O0 ._bitcount (~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['ante'])&O000O000OOO0OOO00 ['succ']&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:667
        OO0OOOOOOO0OO000O =O000OO0O0O00000O0 ._bitcount (~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['ante'])&~(OO0O0000OOOOO0O00 |O000O000OOO0OOO00 ['succ'])&O000O000OOO0OOO00 ['cond']&O000O000OOO0OOO00 ['scnd'])#line:668
        O0O000OO00OOOOO00 =True #line:669
        for OO0OO00000OO0O000 in O000OO0O0O00000O0 .quantifiers .keys ():#line:670
            if (OO0OO00000OO0O000 .upper ()=='FRSTBASE')|(OO0OO00000OO0O000 .upper ()=='BASE1'):#line:671
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=OO0O0OO000OOO0OOO )#line:672
            if (OO0OO00000OO0O000 .upper ()=='SCNDBASE')|(OO0OO00000OO0O000 .upper ()=='BASE2'):#line:673
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=OOO00O000OOOO0OO0 )#line:674
            if (OO0OO00000OO0O000 .upper ()=='FRSTRELBASE')|(OO0OO00000OO0O000 .upper ()=='RELBASE1'):#line:675
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=OO0O0OO000OOO0OOO *1.0 /O000OO0O0O00000O0 .data ["rows_count"])#line:676
            if (OO0OO00000OO0O000 .upper ()=='SCNDRELBASE')|(OO0OO00000OO0O000 .upper ()=='RELBASE2'):#line:677
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=OOO00O000OOOO0OO0 *1.0 /O000OO0O0O00000O0 .data ["rows_count"])#line:678
            if (OO0OO00000OO0O000 .upper ()=='FRSTPIM')|(OO0OO00000OO0O000 .upper ()=='PIM1')|(OO0OO00000OO0O000 .upper ()=='FRSTCONF')|(OO0OO00000OO0O000 .upper ()=='CONF1'):#line:679
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=O0OO000OOOO0O00OO )#line:680
            if (OO0OO00000OO0O000 .upper ()=='SCNDPIM')|(OO0OO00000OO0O000 .upper ()=='PIM2')|(OO0OO00000OO0O000 .upper ()=='SCNDCONF')|(OO0OO00000OO0O000 .upper ()=='CONF2'):#line:681
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=O000000O0000OO0OO )#line:682
            if (OO0OO00000OO0O000 .upper ()=='DELTAPIM')|(OO0OO00000OO0O000 .upper ()=='DELTACONF'):#line:683
                O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=O0OO000OOOO0O00OO -O000000O0000OO0OO )#line:684
            if (OO0OO00000OO0O000 .upper ()=='RATIOPIM')|(OO0OO00000OO0O000 .upper ()=='RATIOCONF'):#line:687
                if (O000000O0000OO0OO >0 ):#line:688
                    O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )<=O0OO000OOOO0O00OO *1.0 /O000000O0000OO0OO )#line:689
                else :#line:690
                    O0O000OO00OOOOO00 =False #line:691
            if (OO0OO00000OO0O000 .upper ()=='RATIOPIM_LEQ')|(OO0OO00000OO0O000 .upper ()=='RATIOCONF_LEQ'):#line:692
                if (O000000O0000OO0OO >0 ):#line:693
                    O0O000OO00OOOOO00 =O0O000OO00OOOOO00 and (O000OO0O0O00000O0 .quantifiers .get (OO0OO00000OO0O000 )>=O0OO000OOOO0O00OO *1.0 /O000000O0000OO0OO )#line:694
                else :#line:695
                    O0O000OO00OOOOO00 =False #line:696
        O0OOOOOOO00O000O0 ={}#line:697
        if O0O000OO00OOOOO00 ==True :#line:698
            O000OO0O0O00000O0 .stats ['total_valid']+=1 #line:700
            O0OOOOOOO00O000O0 ["base1"]=OO0O0OO000OOO0OOO #line:701
            O0OOOOOOO00O000O0 ["base2"]=OOO00O000OOOO0OO0 #line:702
            O0OOOOOOO00O000O0 ["rel_base1"]=OO0O0OO000OOO0OOO *1.0 /O000OO0O0O00000O0 .data ["rows_count"]#line:703
            O0OOOOOOO00O000O0 ["rel_base2"]=OOO00O000OOOO0OO0 *1.0 /O000OO0O0O00000O0 .data ["rows_count"]#line:704
            O0OOOOOOO00O000O0 ["conf1"]=O0OO000OOOO0O00OO #line:705
            O0OOOOOOO00O000O0 ["conf2"]=O000000O0000OO0OO #line:706
            O0OOOOOOO00O000O0 ["deltaconf"]=O0OO000OOOO0O00OO -O000000O0000OO0OO #line:707
            if (O000000O0000OO0OO >0 ):#line:708
                O0OOOOOOO00O000O0 ["ratioconf"]=O0OO000OOOO0O00OO *1.0 /O000000O0000OO0OO #line:709
            else :#line:710
                O0OOOOOOO00O000O0 ["ratioconf"]=None #line:711
            O0OOOOOOO00O000O0 ["fourfold1"]=[O0OO00OOOO0000O0O ,OO000OO0000O0OO00 ,OO0OOO0O0O00OO0OO ,O00OO0000O0O0O000 ]#line:712
            O0OOOOOOO00O000O0 ["fourfold2"]=[O00000O00O00000O0 ,O0000O00O0OOO0O00 ,O0OO0O000O0000OO0 ,OO0OOOOOOO0OO000O ]#line:713
        return O0O000OO00OOOOO00 ,O0OOOOOOO00O000O0 #line:717
    def _verifynewact4ft (OO00OOO00O00OO0OO ,_O000O00OOO00O0000 ):#line:719
        OOO0OOOO0O000OO0O ={}#line:720
        for O000OO0000OO00OO0 in OO00OOO00O00OO0OO .task_actinfo ['cedents']:#line:721
            OOO0OOOO0O000OO0O [O000OO0000OO00OO0 ['cedent_type']]=O000OO0000OO00OO0 ['filter_value']#line:723
        OOOO0O000O0O00O00 =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond'])#line:725
        OO0OOO000000O00OO =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond']&OOO0OOOO0O000OO0O ['antv']&OOO0OOOO0O000OO0O ['sucv'])#line:726
        OOOO000000O0O000O =None #line:727
        O0O000OO0OO0OO0O0 =0 #line:728
        O0OOO00OOO0O0OO0O =0 #line:729
        if OOOO0O000O0O00O00 >0 :#line:738
            O0O000OO0OO0OO0O0 =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond'])*1.0 /OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['cond'])#line:739
        if OO0OOO000000O00OO >0 :#line:740
            O0OOO00OOO0O0OO0O =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond']&OOO0OOOO0O000OO0O ['antv']&OOO0OOOO0O000OO0O ['sucv'])*1.0 /OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['cond']&OOO0OOOO0O000OO0O ['antv'])#line:742
        O00OO000O000000OO =1 <<OO00OOO00O00OO0OO .rows_count #line:744
        OOO00OO0O0OO0O00O =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond'])#line:745
        OOOOO0O00000O00OO =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&~(O00OO000O000000OO |OOO0OOOO0O000OO0O ['succ'])&OOO0OOOO0O000OO0O ['cond'])#line:746
        OO0OO0O0OO0O0000O =OO00OOO00O00OO0OO ._bitcount (~(O00OO000O000000OO |OOO0OOOO0O000OO0O ['ante'])&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond'])#line:747
        O00O0OOO00000OOOO =OO00OOO00O00OO0OO ._bitcount (~(O00OO000O000000OO |OOO0OOOO0O000OO0O ['ante'])&~(O00OO000O000000OO |OOO0OOOO0O000OO0O ['succ'])&OOO0OOOO0O000OO0O ['cond'])#line:748
        O0OOOO0OO00O0O0O0 =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond']&OOO0OOOO0O000OO0O ['antv']&OOO0OOOO0O000OO0O ['sucv'])#line:749
        OOO0O000000OOO0O0 =OO00OOO00O00OO0OO ._bitcount (OOO0OOOO0O000OO0O ['ante']&~(O00OO000O000000OO |(OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['sucv']))&OOO0OOOO0O000OO0O ['cond'])#line:750
        O00000O0OOOO0O000 =OO00OOO00O00OO0OO ._bitcount (~(O00OO000O000000OO |(OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['antv']))&OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['cond']&OOO0OOOO0O000OO0O ['sucv'])#line:751
        OOOOOO0O00OO0OOO0 =OO00OOO00O00OO0OO ._bitcount (~(O00OO000O000000OO |(OOO0OOOO0O000OO0O ['ante']&OOO0OOOO0O000OO0O ['antv']))&~(O00OO000O000000OO |(OOO0OOOO0O000OO0O ['succ']&OOO0OOOO0O000OO0O ['sucv']))&OOO0OOOO0O000OO0O ['cond'])#line:752
        OO00OOOO0OOOO0O0O =True #line:753
        for O0OOO00O000OO0000 in OO00OOO00O00OO0OO .quantifiers .keys ():#line:754
            if (O0OOO00O000OO0000 =='PreBase')|(O0OOO00O000OO0000 =='Base1'):#line:755
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=OOOO0O000O0O00O00 )#line:756
            if (O0OOO00O000OO0000 =='PostBase')|(O0OOO00O000OO0000 =='Base2'):#line:757
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=OO0OOO000000O00OO )#line:758
            if (O0OOO00O000OO0000 =='PreRelBase')|(O0OOO00O000OO0000 =='RelBase1'):#line:759
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=OOOO0O000O0O00O00 *1.0 /OO00OOO00O00OO0OO .data ["rows_count"])#line:760
            if (O0OOO00O000OO0000 =='PostRelBase')|(O0OOO00O000OO0000 =='RelBase2'):#line:761
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=OO0OOO000000O00OO *1.0 /OO00OOO00O00OO0OO .data ["rows_count"])#line:762
            if (O0OOO00O000OO0000 =='Prepim')|(O0OOO00O000OO0000 =='pim1')|(O0OOO00O000OO0000 =='PreConf')|(O0OOO00O000OO0000 =='conf1'):#line:763
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=O0O000OO0OO0OO0O0 )#line:764
            if (O0OOO00O000OO0000 =='Postpim')|(O0OOO00O000OO0000 =='pim2')|(O0OOO00O000OO0000 =='PostConf')|(O0OOO00O000OO0000 =='conf2'):#line:765
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=O0OOO00OOO0O0OO0O )#line:766
            if (O0OOO00O000OO0000 =='Deltapim')|(O0OOO00O000OO0000 =='DeltaConf'):#line:767
                OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=O0O000OO0OO0OO0O0 -O0OOO00OOO0O0OO0O )#line:768
            if (O0OOO00O000OO0000 =='Ratiopim')|(O0OOO00O000OO0000 =='RatioConf'):#line:771
                if (O0OOO00OOO0O0OO0O >0 ):#line:772
                    OO00OOOO0OOOO0O0O =OO00OOOO0OOOO0O0O and (OO00OOO00O00OO0OO .quantifiers .get (O0OOO00O000OO0000 )<=O0O000OO0OO0OO0O0 *1.0 /O0OOO00OOO0O0OO0O )#line:773
                else :#line:774
                    OO00OOOO0OOOO0O0O =False #line:775
        O0OO0O0O0OO0OOOOO ={}#line:776
        if OO00OOOO0OOOO0O0O ==True :#line:777
            OO00OOO00O00OO0OO .stats ['total_valid']+=1 #line:779
            O0OO0O0O0OO0OOOOO ["base1"]=OOOO0O000O0O00O00 #line:780
            O0OO0O0O0OO0OOOOO ["base2"]=OO0OOO000000O00OO #line:781
            O0OO0O0O0OO0OOOOO ["rel_base1"]=OOOO0O000O0O00O00 *1.0 /OO00OOO00O00OO0OO .data ["rows_count"]#line:782
            O0OO0O0O0OO0OOOOO ["rel_base2"]=OO0OOO000000O00OO *1.0 /OO00OOO00O00OO0OO .data ["rows_count"]#line:783
            O0OO0O0O0OO0OOOOO ["conf1"]=O0O000OO0OO0OO0O0 #line:784
            O0OO0O0O0OO0OOOOO ["conf2"]=O0OOO00OOO0O0OO0O #line:785
            O0OO0O0O0OO0OOOOO ["deltaconf"]=O0O000OO0OO0OO0O0 -O0OOO00OOO0O0OO0O #line:786
            if (O0OOO00OOO0O0OO0O >0 ):#line:787
                O0OO0O0O0OO0OOOOO ["ratioconf"]=O0O000OO0OO0OO0O0 *1.0 /O0OOO00OOO0O0OO0O #line:788
            else :#line:789
                O0OO0O0O0OO0OOOOO ["ratioconf"]=None #line:790
            O0OO0O0O0OO0OOOOO ["fourfoldpre"]=[OOO00OO0O0OO0O00O ,OOOOO0O00000O00OO ,OO0OO0O0OO0O0000O ,O00O0OOO00000OOOO ]#line:791
            O0OO0O0O0OO0OOOOO ["fourfoldpost"]=[O0OOOO0OO00O0O0O0 ,OOO0O000000OOO0O0 ,O00000O0OOOO0O000 ,OOOOOO0O00OO0OOO0 ]#line:792
        return OO00OOOO0OOOO0O0O ,O0OO0O0O0OO0OOOOO #line:794
    def _verifyact4ft (OO0000OOO0OO0O0OO ,_OO0000OOOOO0OOOO0 ):#line:796
        O00OOOO0O00OOOOO0 ={}#line:797
        for OOOO0OO00000O0000 in OO0000OOO0OO0O0OO .task_actinfo ['cedents']:#line:798
            O00OOOO0O00OOOOO0 [OOOO0OO00000O0000 ['cedent_type']]=OOOO0OO00000O0000 ['filter_value']#line:800
        O0O0O0OOOOO0000OO =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv-']&O00OOOO0O00OOOOO0 ['sucv-'])#line:802
        O0OOOO0000O000OOO =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv+']&O00OOOO0O00OOOOO0 ['sucv+'])#line:803
        O00OOO0OO00OO00O0 =None #line:804
        O000O00OOOO0000O0 =0 #line:805
        OOOO0O000O0OO00O0 =0 #line:806
        if O0O0O0OOOOO0000OO >0 :#line:815
            O000O00OOOO0000O0 =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv-']&O00OOOO0O00OOOOO0 ['sucv-'])*1.0 /OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv-'])#line:817
        if O0OOOO0000O000OOO >0 :#line:818
            OOOO0O000O0OO00O0 =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv+']&O00OOOO0O00OOOOO0 ['sucv+'])*1.0 /OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv+'])#line:820
        O0OO000O00000000O =1 <<OO0000OOO0OO0O0OO .data ["rows_count"]#line:822
        O0OO00O00000O00OO =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv-']&O00OOOO0O00OOOOO0 ['sucv-'])#line:823
        OO00O000000000O00 =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv-']&~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['sucv-']))&O00OOOO0O00OOOOO0 ['cond'])#line:824
        O0000O0O00OOOOO0O =OO0000OOO0OO0O0OO ._bitcount (~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv-']))&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['sucv-'])#line:825
        O0O0000000O00000O =OO0000OOO0OO0O0OO ._bitcount (~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv-']))&~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['sucv-']))&O00OOOO0O00OOOOO0 ['cond'])#line:826
        O0OOO0OOO0OOO00O0 =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['antv+']&O00OOOO0O00OOOOO0 ['sucv+'])#line:827
        OO0O00O0O0OOOO0OO =OO0000OOO0OO0O0OO ._bitcount (O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv+']&~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['sucv+']))&O00OOOO0O00OOOOO0 ['cond'])#line:828
        OOOOOO000O0OO0O00 =OO0000OOO0OO0O0OO ._bitcount (~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv+']))&O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['cond']&O00OOOO0O00OOOOO0 ['sucv+'])#line:829
        OOO00O0OOOOO00O0O =OO0000OOO0OO0O0OO ._bitcount (~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['ante']&O00OOOO0O00OOOOO0 ['antv+']))&~(O0OO000O00000000O |(O00OOOO0O00OOOOO0 ['succ']&O00OOOO0O00OOOOO0 ['sucv+']))&O00OOOO0O00OOOOO0 ['cond'])#line:830
        O0O0OOO0OOO0OO000 =True #line:831
        for O0OO0OOO000OO0OO0 in OO0000OOO0OO0O0OO .quantifiers .keys ():#line:832
            if (O0OO0OOO000OO0OO0 =='PreBase')|(O0OO0OOO000OO0OO0 =='Base1'):#line:833
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O0O0O0OOOOO0000OO )#line:834
            if (O0OO0OOO000OO0OO0 =='PostBase')|(O0OO0OOO000OO0OO0 =='Base2'):#line:835
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O0OOOO0000O000OOO )#line:836
            if (O0OO0OOO000OO0OO0 =='PreRelBase')|(O0OO0OOO000OO0OO0 =='RelBase1'):#line:837
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O0O0O0OOOOO0000OO *1.0 /OO0000OOO0OO0O0OO .data ["rows_count"])#line:838
            if (O0OO0OOO000OO0OO0 =='PostRelBase')|(O0OO0OOO000OO0OO0 =='RelBase2'):#line:839
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O0OOOO0000O000OOO *1.0 /OO0000OOO0OO0O0OO .data ["rows_count"])#line:840
            if (O0OO0OOO000OO0OO0 =='Prepim')|(O0OO0OOO000OO0OO0 =='pim1')|(O0OO0OOO000OO0OO0 =='PreConf')|(O0OO0OOO000OO0OO0 =='conf1'):#line:841
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O000O00OOOO0000O0 )#line:842
            if (O0OO0OOO000OO0OO0 =='Postpim')|(O0OO0OOO000OO0OO0 =='pim2')|(O0OO0OOO000OO0OO0 =='PostConf')|(O0OO0OOO000OO0OO0 =='conf2'):#line:843
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=OOOO0O000O0OO00O0 )#line:844
            if (O0OO0OOO000OO0OO0 =='Deltapim')|(O0OO0OOO000OO0OO0 =='DeltaConf'):#line:845
                O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=O000O00OOOO0000O0 -OOOO0O000O0OO00O0 )#line:846
            if (O0OO0OOO000OO0OO0 =='Ratiopim')|(O0OO0OOO000OO0OO0 =='RatioConf'):#line:849
                if (O000O00OOOO0000O0 >0 ):#line:850
                    O0O0OOO0OOO0OO000 =O0O0OOO0OOO0OO000 and (OO0000OOO0OO0O0OO .quantifiers .get (O0OO0OOO000OO0OO0 )<=OOOO0O000O0OO00O0 *1.0 /O000O00OOOO0000O0 )#line:851
                else :#line:852
                    O0O0OOO0OOO0OO000 =False #line:853
        OO0OO000O0OOO0000 ={}#line:854
        if O0O0OOO0OOO0OO000 ==True :#line:855
            OO0000OOO0OO0O0OO .stats ['total_valid']+=1 #line:857
            OO0OO000O0OOO0000 ["base1"]=O0O0O0OOOOO0000OO #line:858
            OO0OO000O0OOO0000 ["base2"]=O0OOOO0000O000OOO #line:859
            OO0OO000O0OOO0000 ["rel_base1"]=O0O0O0OOOOO0000OO *1.0 /OO0000OOO0OO0O0OO .data ["rows_count"]#line:860
            OO0OO000O0OOO0000 ["rel_base2"]=O0OOOO0000O000OOO *1.0 /OO0000OOO0OO0O0OO .data ["rows_count"]#line:861
            OO0OO000O0OOO0000 ["conf1"]=O000O00OOOO0000O0 #line:862
            OO0OO000O0OOO0000 ["conf2"]=OOOO0O000O0OO00O0 #line:863
            OO0OO000O0OOO0000 ["deltaconf"]=O000O00OOOO0000O0 -OOOO0O000O0OO00O0 #line:864
            if (O000O00OOOO0000O0 >0 ):#line:865
                OO0OO000O0OOO0000 ["ratioconf"]=OOOO0O000O0OO00O0 *1.0 /O000O00OOOO0000O0 #line:866
            else :#line:867
                OO0OO000O0OOO0000 ["ratioconf"]=None #line:868
            OO0OO000O0OOO0000 ["fourfoldpre"]=[O0OO00O00000O00OO ,OO00O000000000O00 ,O0000O0O00OOOOO0O ,O0O0000000O00000O ]#line:869
            OO0OO000O0OOO0000 ["fourfoldpost"]=[O0OOO0OOO0OOO00O0 ,OO0O00O0O0OOOO0OO ,OOOOOO000O0OO0O00 ,OOO00O0OOOOO00O0O ]#line:870
        return O0O0OOO0OOO0OO000 ,OO0OO000O0OOO0000 #line:872
    def _verify_opt (O0OO00O0O0000O000 ,OO000OO0OO00OO000 ,O00O00O00O00O00OO ):#line:874
        O0OO00O0O0000O000 .stats ['total_ver']+=1 #line:875
        OO0O00O0O0O0O0OO0 =False #line:876
        if not (OO000OO0OO00OO000 ['optim'].get ('only_con')):#line:879
            return False #line:880
        if not (O0OO00O0O0000O000 .options ['optimizations']):#line:883
            return False #line:885
        OO0O000000O00O0O0 ={}#line:887
        for O0O0O00OO0O0O0OOO in O0OO00O0O0000O000 .task_actinfo ['cedents']:#line:888
            OO0O000000O00O0O0 [O0O0O00OO0O0O0OOO ['cedent_type']]=O0O0O00OO0O0O0OOO ['filter_value']#line:890
        OO00OOOO000000O0O =1 <<O0OO00O0O0000O000 .data ["rows_count"]#line:892
        OO000OO0O0O00OOOO =OO00OOOO000000O0O -1 #line:893
        OOOO00OOO00O0OOO0 =""#line:894
        O0O000000OO0O000O =0 #line:895
        if (OO0O000000O00O0O0 .get ('ante')!=None ):#line:896
            OO000OO0O0O00OOOO =OO000OO0O0O00OOOO &OO0O000000O00O0O0 ['ante']#line:897
        if (OO0O000000O00O0O0 .get ('succ')!=None ):#line:898
            OO000OO0O0O00OOOO =OO000OO0O0O00OOOO &OO0O000000O00O0O0 ['succ']#line:899
        if (OO0O000000O00O0O0 .get ('cond')!=None ):#line:900
            OO000OO0O0O00OOOO =OO000OO0O0O00OOOO &OO0O000000O00O0O0 ['cond']#line:901
        O00O0O0000OOO0OOO =None #line:904
        if (O0OO00O0O0000O000 .proc =='CFMiner')|(O0OO00O0O0000O000 .proc =='4ftMiner')|(O0OO00O0O0000O000 .proc =='UICMiner'):#line:929
            OOO0000000O00O0OO =O0OO00O0O0000O000 ._bitcount (OO000OO0O0O00OOOO )#line:930
            if not (O0OO00O0O0000O000 ._opt_base ==None ):#line:931
                if not (O0OO00O0O0000O000 ._opt_base <=OOO0000000O00O0OO ):#line:932
                    OO0O00O0O0O0O0OO0 =True #line:933
            if not (O0OO00O0O0000O000 ._opt_relbase ==None ):#line:935
                if not (O0OO00O0O0000O000 ._opt_relbase <=OOO0000000O00O0OO *1.0 /O0OO00O0O0000O000 .data ["rows_count"]):#line:936
                    OO0O00O0O0O0O0OO0 =True #line:937
        if (O0OO00O0O0000O000 .proc =='SD4ftMiner'):#line:939
            OOO0000000O00O0OO =O0OO00O0O0000O000 ._bitcount (OO000OO0O0O00OOOO )#line:940
            if (not (O0OO00O0O0000O000 ._opt_base1 ==None ))&(not (O0OO00O0O0000O000 ._opt_base2 ==None )):#line:941
                if not (max (O0OO00O0O0000O000 ._opt_base1 ,O0OO00O0O0000O000 ._opt_base2 )<=OOO0000000O00O0OO ):#line:942
                    OO0O00O0O0O0O0OO0 =True #line:944
            if (not (O0OO00O0O0000O000 ._opt_relbase1 ==None ))&(not (O0OO00O0O0000O000 ._opt_relbase2 ==None )):#line:945
                if not (max (O0OO00O0O0000O000 ._opt_relbase1 ,O0OO00O0O0000O000 ._opt_relbase2 )<=OOO0000000O00O0OO *1.0 /O0OO00O0O0000O000 .data ["rows_count"]):#line:946
                    OO0O00O0O0O0O0OO0 =True #line:947
        return OO0O00O0O0O0O0OO0 #line:949
        if O0OO00O0O0000O000 .proc =='CFMiner':#line:952
            if (O00O00O00O00O00OO ['cedent_type']=='cond')&(O00O00O00O00O00OO ['defi'].get ('type')=='con'):#line:953
                OOO0000000O00O0OO =bin (OO0O000000O00O0O0 ['cond']).count ("1")#line:954
                OO0000OO0OO00OO00 =True #line:955
                for OO0OOO0OOO0OOOO00 in O0OO00O0O0000O000 .quantifiers .keys ():#line:956
                    if OO0OOO0OOO0OOOO00 =='Base':#line:957
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO )#line:958
                        if not (OO0000OO0OO00OO00 ):#line:959
                            print (f"...optimization : base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:960
                    if OO0OOO0OOO0OOOO00 =='RelBase':#line:961
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO *1.0 /O0OO00O0O0000O000 .data ["rows_count"])#line:962
                        if not (OO0000OO0OO00OO00 ):#line:963
                            print (f"...optimization : base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:964
                OO0O00O0O0O0O0OO0 =not (OO0000OO0OO00OO00 )#line:965
        elif O0OO00O0O0000O000 .proc =='4ftMiner':#line:966
            if (O00O00O00O00O00OO ['cedent_type']=='cond')&(O00O00O00O00O00OO ['defi'].get ('type')=='con'):#line:967
                OOO0000000O00O0OO =bin (OO0O000000O00O0O0 ['cond']).count ("1")#line:968
                OO0000OO0OO00OO00 =True #line:969
                for OO0OOO0OOO0OOOO00 in O0OO00O0O0000O000 .quantifiers .keys ():#line:970
                    if OO0OOO0OOO0OOOO00 =='Base':#line:971
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO )#line:972
                        if not (OO0000OO0OO00OO00 ):#line:973
                            print (f"...optimization : base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:974
                    if OO0OOO0OOO0OOOO00 =='RelBase':#line:975
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO *1.0 /O0OO00O0O0000O000 .data ["rows_count"])#line:976
                        if not (OO0000OO0OO00OO00 ):#line:977
                            print (f"...optimization : base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:978
                OO0O00O0O0O0O0OO0 =not (OO0000OO0OO00OO00 )#line:979
            if (O00O00O00O00O00OO ['cedent_type']=='ante')&(O00O00O00O00O00OO ['defi'].get ('type')=='con'):#line:980
                OOO0000000O00O0OO =bin (OO0O000000O00O0O0 ['ante']&OO0O000000O00O0O0 ['cond']).count ("1")#line:981
                OO0000OO0OO00OO00 =True #line:982
                for OO0OOO0OOO0OOOO00 in O0OO00O0O0000O000 .quantifiers .keys ():#line:983
                    if OO0OOO0OOO0OOOO00 =='Base':#line:984
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO )#line:985
                        if not (OO0000OO0OO00OO00 ):#line:986
                            print (f"...optimization : ANTE: base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:987
                    if OO0OOO0OOO0OOOO00 =='RelBase':#line:988
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OOO0000000O00O0OO *1.0 /O0OO00O0O0000O000 .data ["rows_count"])#line:989
                        if not (OO0000OO0OO00OO00 ):#line:990
                            print (f"...optimization : ANTE:  base is {OOO0000000O00O0OO} for {O00O00O00O00O00OO['generated_string']}")#line:991
                OO0O00O0O0O0O0OO0 =not (OO0000OO0OO00OO00 )#line:992
            if (O00O00O00O00O00OO ['cedent_type']=='succ')&(O00O00O00O00O00OO ['defi'].get ('type')=='con'):#line:993
                OOO0000000O00O0OO =bin (OO0O000000O00O0O0 ['ante']&OO0O000000O00O0O0 ['cond']&OO0O000000O00O0O0 ['succ']).count ("1")#line:994
                O00O0O0000OOO0OOO =0 #line:995
                if OOO0000000O00O0OO >0 :#line:996
                    O00O0O0000OOO0OOO =bin (OO0O000000O00O0O0 ['ante']&OO0O000000O00O0O0 ['succ']&OO0O000000O00O0O0 ['cond']).count ("1")*1.0 /bin (OO0O000000O00O0O0 ['ante']&OO0O000000O00O0O0 ['cond']).count ("1")#line:997
                OO00OOOO000000O0O =1 <<O0OO00O0O0000O000 .data ["rows_count"]#line:998
                OO0O000OOOOOO0O0O =bin (OO0O000000O00O0O0 ['ante']&OO0O000000O00O0O0 ['succ']&OO0O000000O00O0O0 ['cond']).count ("1")#line:999
                OOO000O0O000O0O0O =bin (OO0O000000O00O0O0 ['ante']&~(OO00OOOO000000O0O |OO0O000000O00O0O0 ['succ'])&OO0O000000O00O0O0 ['cond']).count ("1")#line:1000
                O0O0O00OO0O0O0OOO =bin (~(OO00OOOO000000O0O |OO0O000000O00O0O0 ['ante'])&OO0O000000O00O0O0 ['succ']&OO0O000000O00O0O0 ['cond']).count ("1")#line:1001
                O00OOOOO0000000O0 =bin (~(OO00OOOO000000O0O |OO0O000000O00O0O0 ['ante'])&~(OO00OOOO000000O0O |OO0O000000O00O0O0 ['succ'])&OO0O000000O00O0O0 ['cond']).count ("1")#line:1002
                OO0000OO0OO00OO00 =True #line:1003
                for OO0OOO0OOO0OOOO00 in O0OO00O0O0000O000 .quantifiers .keys ():#line:1004
                    if OO0OOO0OOO0OOOO00 =='pim':#line:1005
                        OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=O00O0O0000OOO0OOO )#line:1006
                    if not (OO0000OO0OO00OO00 ):#line:1007
                        print (f"...optimization : SUCC:  pim is {O00O0O0000OOO0OOO} for {O00O00O00O00O00OO['generated_string']}")#line:1008
                    if OO0OOO0OOO0OOOO00 =='aad':#line:1010
                        if (OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )*(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO )>0 :#line:1011
                            OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=OO0O000OOOOOO0O0O *(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O +O0O0O00OO0O0O0OOO +O00OOOOO0000000O0 )/(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )/(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO )-1 )#line:1012
                        else :#line:1013
                            OO0000OO0OO00OO00 =False #line:1014
                        if not (OO0000OO0OO00OO00 ):#line:1015
                            O00OOO0O0OO00O000 =OO0O000OOOOOO0O0O *(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O +O0O0O00OO0O0O0OOO +O00OOOOO0000000O0 )/(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )/(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO )-1 #line:1016
                            print (f"...optimization : SUCC:  aad is {O00OOO0O0OO00O000} for {O00O00O00O00O00OO['generated_string']}")#line:1017
                    if OO0OOO0OOO0OOOO00 =='bad':#line:1018
                        if (OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )*(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO )>0 :#line:1019
                            OO0000OO0OO00OO00 =OO0000OO0OO00OO00 and (O0OO00O0O0000O000 .quantifiers .get (OO0OOO0OOO0OOOO00 )<=1 -OO0O000OOOOOO0O0O *(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O +O0O0O00OO0O0O0OOO +O00OOOOO0000000O0 )/(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )/(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO ))#line:1020
                        else :#line:1021
                            OO0000OO0OO00OO00 =False #line:1022
                        if not (OO0000OO0OO00OO00 ):#line:1023
                            OOO0OO0OO0O0O00OO =1 -OO0O000OOOOOO0O0O *(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O +O0O0O00OO0O0O0OOO +O00OOOOO0000000O0 )/(OO0O000OOOOOO0O0O +OOO000O0O000O0O0O )/(OO0O000OOOOOO0O0O +O0O0O00OO0O0O0OOO )#line:1024
                            print (f"...optimization : SUCC:  bad is {OOO0OO0OO0O0O00OO} for {O00O00O00O00O00OO['generated_string']}")#line:1025
                OO0O00O0O0O0O0OO0 =not (OO0000OO0OO00OO00 )#line:1026
        if (OO0O00O0O0O0O0OO0 ):#line:1027
            print (f"... OPTIMALIZATION - SKIPPING BRANCH at cedent {O00O00O00O00O00OO['cedent_type']}")#line:1028
        return OO0O00O0O0O0O0OO0 #line:1029
    def _print (O0O00OO0000O00000 ,OOO00O0OOOOO00OOO ,_OOOOO000O0000O0OO ,_O0OO000000O0OO000 ):#line:1032
        if (len (_OOOOO000O0000O0OO ))!=len (_O0OO000000O0OO000 ):#line:1033
            print ("DIFF IN LEN for following cedent : "+str (len (_OOOOO000O0000O0OO ))+" vs "+str (len (_O0OO000000O0OO000 )))#line:1034
            print ("trace cedent : "+str (_OOOOO000O0000O0OO )+", traces "+str (_O0OO000000O0OO000 ))#line:1035
        O0OOOOO00O00OO0OO =''#line:1036
        O00OOO000000OO000 ={}#line:1037
        O0O0O0000OOOO00OO =[]#line:1038
        for O000OOO00OO0OOO0O in range (len (_OOOOO000O0000O0OO )):#line:1039
            OO0O0O00O0O0OOOOO =O0O00OO0000O00000 .data ["varname"].index (OOO00O0OOOOO00OOO ['defi'].get ('attributes')[_OOOOO000O0000O0OO [O000OOO00OO0OOO0O ]].get ('name'))#line:1040
            O0OOOOO00O00OO0OO =O0OOOOO00O00OO0OO +O0O00OO0000O00000 .data ["varname"][OO0O0O00O0O0OOOOO ]+'('#line:1042
            O0O0O0000OOOO00OO .append (OO0O0O00O0O0OOOOO )#line:1043
            O0OOOOO0000OO0O0O =[]#line:1044
            for OOOO0O00000OOO0OO in _O0OO000000O0OO000 [O000OOO00OO0OOO0O ]:#line:1045
                O0OOOOO00O00OO0OO =O0OOOOO00O00OO0OO +str (O0O00OO0000O00000 .data ["catnames"][OO0O0O00O0O0OOOOO ][OOOO0O00000OOO0OO ])+" "#line:1046
                O0OOOOO0000OO0O0O .append (str (O0O00OO0000O00000 .data ["catnames"][OO0O0O00O0O0OOOOO ][OOOO0O00000OOO0OO ]))#line:1047
            O0OOOOO00O00OO0OO =O0OOOOO00O00OO0OO [:-1 ]+')'#line:1048
            O00OOO000000OO000 [O0O00OO0000O00000 .data ["varname"][OO0O0O00O0O0OOOOO ]]=O0OOOOO0000OO0O0O #line:1049
            if O000OOO00OO0OOO0O +1 <len (_OOOOO000O0000O0OO ):#line:1050
                O0OOOOO00O00OO0OO =O0OOOOO00O00OO0OO +' & '#line:1051
        return O0OOOOO00O00OO0OO ,O00OOO000000OO000 ,O0O0O0000OOOO00OO #line:1055
    def _print_hypo (O0OOO00OO00O0OOOO ,O0OOO0OOOOOOO0OO0 ):#line:1057
        O0OOO00OO00O0OOOO .print_rule (O0OOO0OOOOOOO0OO0 )#line:1058
    def _print_rule (O0O0OOOO0OO0O0OO0 ,O000O000OOO00OOOO ):#line:1060
        if O0O0OOOO0OO0O0OO0 .verbosity ['print_rules']:#line:1061
            print ('Rules info : '+str (O000O000OOO00OOOO ['params']))#line:1062
            for OO0O0O0OOO00O000O in O0O0OOOO0OO0O0OO0 .task_actinfo ['cedents']:#line:1063
                print (OO0O0O0OOO00O000O ['cedent_type']+' = '+OO0O0O0OOO00O000O ['generated_string'])#line:1064
    def _genvar (O00OO0O00000OOOO0 ,O00OO00OOOOO0O0OO ,O000O000O0O0OO0OO ,_OO000OO0O00O0OOO0 ,_O0OOO000OO00000OO ,_O00OO0OOO0OO0O000 ,_O0OO000OOOOOOOOOO ,_OO00OO00O0O000O00 ):#line:1066
        for OO0000O000OO000O0 in range (O000O000O0O0OO0OO ['num_cedent']):#line:1067
            if len (_OO000OO0O00O0OOO0 )==0 or OO0000O000OO000O0 >_OO000OO0O00O0OOO0 [-1 ]:#line:1068
                _OO000OO0O00O0OOO0 .append (OO0000O000OO000O0 )#line:1069
                O000OOOO00OO0OO0O =O00OO0O00000OOOO0 .data ["varname"].index (O000O000O0O0OO0OO ['defi'].get ('attributes')[OO0000O000OO000O0 ].get ('name'))#line:1070
                _O00O00O0O0OOO0O00 =O000O000O0O0OO0OO ['defi'].get ('attributes')[OO0000O000OO000O0 ].get ('minlen')#line:1071
                _OOOO0OO0O0O0OO0OO =O000O000O0O0OO0OO ['defi'].get ('attributes')[OO0000O000OO000O0 ].get ('maxlen')#line:1072
                _O0000000000O0O0OO =O000O000O0O0OO0OO ['defi'].get ('attributes')[OO0000O000OO000O0 ].get ('type')#line:1073
                OOOOOOO000OOOO0OO =len (O00OO0O00000OOOO0 .data ["dm"][O000OOOO00OO0OO0O ])#line:1074
                _O0O0O00OOOOO0O0OO =[]#line:1075
                _O0OOO000OO00000OO .append (_O0O0O00OOOOO0O0OO )#line:1076
                _O0OOO0000000O0OO0 =int (0 )#line:1077
                O00OO0O00000OOOO0 ._gencomb (O00OO00OOOOO0O0OO ,O000O000O0O0OO0OO ,_OO000OO0O00O0OOO0 ,_O0OOO000OO00000OO ,_O0O0O00OOOOO0O0OO ,_O00OO0OOO0OO0O000 ,_O0OOO0000000O0OO0 ,OOOOOOO000OOOO0OO ,_O0000000000O0O0OO ,_O0OO000OOOOOOOOOO ,_OO00OO00O0O000O00 ,_O00O00O0O0OOO0O00 ,_OOOO0OO0O0O0OO0OO )#line:1078
                _O0OOO000OO00000OO .pop ()#line:1079
                _OO000OO0O00O0OOO0 .pop ()#line:1080
    def _gencomb (O0OO0O000OO000OOO ,O0O0O0000OO0OO00O ,O0OO0O0O0000OO00O ,_O0O000OOOO0OO00O0 ,_O000000O0O0OO0OOO ,_OO0O0OO0O0O0O0000 ,_O0OO00O00O00000OO ,_OO0OOOO000O000OO0 ,O00O00OO0OO00OOOO ,_O0OOO0000000000OO ,_O00O00OOO0OOOOOOO ,_OOO00O0000OO00000 ,_OO0OOOOOO00OO0OO0 ,_OOO0000O0O0OOO0O0 ):#line:1082
        _O000OO000O00O0000 =[]#line:1083
        if _O0OOO0000000000OO =="subset":#line:1084
            if len (_OO0O0OO0O0O0O0000 )==0 :#line:1085
                _O000OO000O00O0000 =range (O00O00OO0OO00OOOO )#line:1086
            else :#line:1087
                _O000OO000O00O0000 =range (_OO0O0OO0O0O0O0000 [-1 ]+1 ,O00O00OO0OO00OOOO )#line:1088
        elif _O0OOO0000000000OO =="seq":#line:1089
            if len (_OO0O0OO0O0O0O0000 )==0 :#line:1090
                _O000OO000O00O0000 =range (O00O00OO0OO00OOOO -_OO0OOOOOO00OO0OO0 +1 )#line:1091
            else :#line:1092
                if _OO0O0OO0O0O0O0000 [-1 ]+1 ==O00O00OO0OO00OOOO :#line:1093
                    return #line:1094
                O000OO0O00O0OO000 =_OO0O0OO0O0O0O0000 [-1 ]+1 #line:1095
                _O000OO000O00O0000 .append (O000OO0O00O0OO000 )#line:1096
        elif _O0OOO0000000000OO =="lcut":#line:1097
            if len (_OO0O0OO0O0O0O0000 )==0 :#line:1098
                O000OO0O00O0OO000 =0 ;#line:1099
            else :#line:1100
                if _OO0O0OO0O0O0O0000 [-1 ]+1 ==O00O00OO0OO00OOOO :#line:1101
                    return #line:1102
                O000OO0O00O0OO000 =_OO0O0OO0O0O0O0000 [-1 ]+1 #line:1103
            _O000OO000O00O0000 .append (O000OO0O00O0OO000 )#line:1104
        elif _O0OOO0000000000OO =="rcut":#line:1105
            if len (_OO0O0OO0O0O0O0000 )==0 :#line:1106
                O000OO0O00O0OO000 =O00O00OO0OO00OOOO -1 ;#line:1107
            else :#line:1108
                if _OO0O0OO0O0O0O0000 [-1 ]==0 :#line:1109
                    return #line:1110
                O000OO0O00O0OO000 =_OO0O0OO0O0O0O0000 [-1 ]-1 #line:1111
            _O000OO000O00O0000 .append (O000OO0O00O0OO000 )#line:1113
        elif _O0OOO0000000000OO =="one":#line:1114
            if len (_OO0O0OO0O0O0O0000 )==0 :#line:1115
                O0OO0O0O00OOOOO00 =O0OO0O000OO000OOO .data ["varname"].index (O0OO0O0O0000OO00O ['defi'].get ('attributes')[_O0O000OOOO0OO00O0 [-1 ]].get ('name'))#line:1116
                try :#line:1117
                    O000OO0O00O0OO000 =O0OO0O000OO000OOO .data ["catnames"][O0OO0O0O00OOOOO00 ].index (O0OO0O0O0000OO00O ['defi'].get ('attributes')[_O0O000OOOO0OO00O0 [-1 ]].get ('value'))#line:1118
                except :#line:1119
                    print (f"ERROR: attribute '{O0OO0O0O0000OO00O['defi'].get('attributes')[_O0O000OOOO0OO00O0[-1]].get('name')}' has not value '{O0OO0O0O0000OO00O['defi'].get('attributes')[_O0O000OOOO0OO00O0[-1]].get('value')}'")#line:1120
                    exit (1 )#line:1121
                _O000OO000O00O0000 .append (O000OO0O00O0OO000 )#line:1122
                _OO0OOOOOO00OO0OO0 =1 #line:1123
                _OOO0000O0O0OOO0O0 =1 #line:1124
            else :#line:1125
                print ("DEBUG: one category should not have more categories")#line:1126
                return #line:1127
        else :#line:1128
            print ("Attribute type "+_O0OOO0000000000OO +" not supported.")#line:1129
            return #line:1130
        for OO0OO0000OO0OO0OO in _O000OO000O00O0000 :#line:1133
                _OO0O0OO0O0O0O0000 .append (OO0OO0000OO0OO0OO )#line:1135
                _O000000O0O0OO0OOO .pop ()#line:1136
                _O000000O0O0OO0OOO .append (_OO0O0OO0O0O0O0000 )#line:1137
                _O00000OO0OOOOOO00 =_OO0OOOO000O000OO0 |O0OO0O000OO000OOO .data ["dm"][O0OO0O000OO000OOO .data ["varname"].index (O0OO0O0O0000OO00O ['defi'].get ('attributes')[_O0O000OOOO0OO00O0 [-1 ]].get ('name'))][OO0OO0000OO0OO0OO ]#line:1141
                _OOO0OOOO0O0OOO00O =1 #line:1143
                if (len (_O0O000OOOO0OO00O0 )<_O00O00OOO0OOOOOOO ):#line:1144
                    _OOO0OOOO0O0OOO00O =-1 #line:1145
                if (len (_O000000O0O0OO0OOO [-1 ])<_OO0OOOOOO00OO0OO0 ):#line:1147
                    _OOO0OOOO0O0OOO00O =0 #line:1148
                _O0OO0O0O00O0O0O00 =0 #line:1150
                if O0OO0O0O0000OO00O ['defi'].get ('type')=='con':#line:1151
                    _O0OO0O0O00O0O0O00 =_O0OO00O00O00000OO &_O00000OO0OOOOOO00 #line:1152
                else :#line:1153
                    _O0OO0O0O00O0O0O00 =_O0OO00O00O00000OO |_O00000OO0OOOOOO00 #line:1154
                O0OO0O0O0000OO00O ['trace_cedent']=_O0O000OOOO0OO00O0 #line:1155
                O0OO0O0O0000OO00O ['traces']=_O000000O0O0OO0OOO #line:1156
                OOO000O00O00OO0OO ,OO0OOO00O0000000O ,OO000OOOO00OO0000 =O0OO0O000OO000OOO ._print (O0OO0O0O0000OO00O ,_O0O000OOOO0OO00O0 ,_O000000O0O0OO0OOO )#line:1157
                O0OO0O0O0000OO00O ['generated_string']=OOO000O00O00OO0OO #line:1158
                O0OO0O0O0000OO00O ['rule']=OO0OOO00O0000000O #line:1159
                O0OO0O0O0000OO00O ['filter_value']=_O0OO0O0O00O0O0O00 #line:1160
                O0OO0O0O0000OO00O ['traces']=copy .deepcopy (_O000000O0O0OO0OOO )#line:1161
                O0OO0O0O0000OO00O ['trace_cedent']=copy .deepcopy (_O0O000OOOO0OO00O0 )#line:1162
                O0OO0O0O0000OO00O ['trace_cedent_asindata']=copy .deepcopy (OO000OOOO00OO0000 )#line:1163
                O0O0O0000OO0OO00O ['cedents'].append (O0OO0O0O0000OO00O )#line:1165
                O0OOOO00000OOOO00 =O0OO0O000OO000OOO ._verify_opt (O0O0O0000OO0OO00O ,O0OO0O0O0000OO00O )#line:1166
                if not (O0OOOO00000OOOO00 ):#line:1172
                    if _OOO0OOOO0O0OOO00O ==1 :#line:1173
                        if len (O0O0O0000OO0OO00O ['cedents_to_do'])==len (O0O0O0000OO0OO00O ['cedents']):#line:1175
                            if O0OO0O000OO000OOO .proc =='CFMiner':#line:1176
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verifyCF (_O0OO0O0O00O0O0O00 )#line:1177
                            elif O0OO0O000OO000OOO .proc =='UICMiner':#line:1178
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verifyUIC (_O0OO0O0O00O0O0O00 )#line:1179
                            elif O0OO0O000OO000OOO .proc =='4ftMiner':#line:1180
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verify4ft (_O00000OO0OOOOOO00 )#line:1181
                            elif O0OO0O000OO000OOO .proc =='SD4ftMiner':#line:1182
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verifysd4ft (_O00000OO0OOOOOO00 )#line:1183
                            elif O0OO0O000OO000OOO .proc =='NewAct4ftMiner':#line:1184
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verifynewact4ft (_O00000OO0OOOOOO00 )#line:1185
                            elif O0OO0O000OO000OOO .proc =='Act4ftMiner':#line:1186
                                OOOOO00O00OOO00O0 ,OO0000O00OO00O0OO =O0OO0O000OO000OOO ._verifyact4ft (_O00000OO0OOOOOO00 )#line:1187
                            else :#line:1188
                                print ("Unsupported procedure : "+O0OO0O000OO000OOO .proc )#line:1189
                                exit (0 )#line:1190
                            if OOOOO00O00OOO00O0 ==True :#line:1191
                                OOO0000OOOOO00OO0 ={}#line:1192
                                OOO0000OOOOO00OO0 ["rule_id"]=O0OO0O000OO000OOO .stats ['total_valid']#line:1193
                                OOO0000OOOOO00OO0 ["cedents_str"]={}#line:1194
                                OOO0000OOOOO00OO0 ["cedents_struct"]={}#line:1195
                                OOO0000OOOOO00OO0 ['traces']={}#line:1196
                                OOO0000OOOOO00OO0 ['trace_cedent_taskorder']={}#line:1197
                                OOO0000OOOOO00OO0 ['trace_cedent_dataorder']={}#line:1198
                                for OO000O0O00OOOO0OO in O0O0O0000OO0OO00O ['cedents']:#line:1199
                                    OOO0000OOOOO00OO0 ['cedents_str'][OO000O0O00OOOO0OO ['cedent_type']]=OO000O0O00OOOO0OO ['generated_string']#line:1201
                                    OOO0000OOOOO00OO0 ['cedents_struct'][OO000O0O00OOOO0OO ['cedent_type']]=OO000O0O00OOOO0OO ['rule']#line:1202
                                    OOO0000OOOOO00OO0 ['traces'][OO000O0O00OOOO0OO ['cedent_type']]=OO000O0O00OOOO0OO ['traces']#line:1203
                                    OOO0000OOOOO00OO0 ['trace_cedent_taskorder'][OO000O0O00OOOO0OO ['cedent_type']]=OO000O0O00OOOO0OO ['trace_cedent']#line:1204
                                    OOO0000OOOOO00OO0 ['trace_cedent_dataorder'][OO000O0O00OOOO0OO ['cedent_type']]=OO000O0O00OOOO0OO ['trace_cedent_asindata']#line:1205
                                OOO0000OOOOO00OO0 ["params"]=OO0000O00OO00O0OO #line:1207
                                O0OO0O000OO000OOO ._print_rule (OOO0000OOOOO00OO0 )#line:1209
                                O0OO0O000OO000OOO .rulelist .append (OOO0000OOOOO00OO0 )#line:1215
                            O0OO0O000OO000OOO .stats ['total_cnt']+=1 #line:1217
                            O0OO0O000OO000OOO .stats ['total_ver']+=1 #line:1218
                    if _OOO0OOOO0O0OOO00O >=0 :#line:1219
                        if len (O0O0O0000OO0OO00O ['cedents_to_do'])>len (O0O0O0000OO0OO00O ['cedents']):#line:1220
                            O0OO0O000OO000OOO ._start_cedent (O0O0O0000OO0OO00O )#line:1221
                    O0O0O0000OO0OO00O ['cedents'].pop ()#line:1222
                    if (len (_O0O000OOOO0OO00O0 )<_OOO00O0000OO00000 ):#line:1223
                        O0OO0O000OO000OOO ._genvar (O0O0O0000OO0OO00O ,O0OO0O0O0000OO00O ,_O0O000OOOO0OO00O0 ,_O000000O0O0OO0OOO ,_O0OO0O0O00O0O0O00 ,_O00O00OOO0OOOOOOO ,_OOO00O0000OO00000 )#line:1224
                else :#line:1225
                    O0O0O0000OO0OO00O ['cedents'].pop ()#line:1226
                if len (_OO0O0OO0O0O0O0000 )<_OOO0000O0O0OOO0O0 :#line:1227
                    O0OO0O000OO000OOO ._gencomb (O0O0O0000OO0OO00O ,O0OO0O0O0000OO00O ,_O0O000OOOO0OO00O0 ,_O000000O0O0OO0OOO ,_OO0O0OO0O0O0O0000 ,_O0OO00O00O00000OO ,_O00000OO0OOOOOO00 ,O00O00OO0OO00OOOO ,_O0OOO0000000000OO ,_O00O00OOO0OOOOOOO ,_OOO00O0000OO00000 ,_OO0OOOOOO00OO0OO0 ,_OOO0000O0O0OOO0O0 )#line:1228
                _OO0O0OO0O0O0O0000 .pop ()#line:1229
    def _start_cedent (O0OOOO000000O0OOO ,OO00OO0OO0O000O00 ):#line:1231
        if len (OO00OO0OO0O000O00 ['cedents_to_do'])>len (OO00OO0OO0O000O00 ['cedents']):#line:1232
            _O000OOO0OOOO00OOO =[]#line:1233
            _O0OO0OOOO0O000000 =[]#line:1234
            O000O0OOO00O00O00 ={}#line:1235
            O000O0OOO00O00O00 ['cedent_type']=OO00OO0OO0O000O00 ['cedents_to_do'][len (OO00OO0OO0O000O00 ['cedents'])]#line:1236
            OOO000OOOO0O0OOO0 =O000O0OOO00O00O00 ['cedent_type']#line:1237
            if ((OOO000OOOO0O0OOO0 [-1 ]=='-')|(OOO000OOOO0O0OOO0 [-1 ]=='+')):#line:1238
                OOO000OOOO0O0OOO0 =OOO000OOOO0O0OOO0 [:-1 ]#line:1239
            O000O0OOO00O00O00 ['defi']=O0OOOO000000O0OOO .kwargs .get (OOO000OOOO0O0OOO0 )#line:1241
            if (O000O0OOO00O00O00 ['defi']==None ):#line:1242
                print ("Error getting cedent ",O000O0OOO00O00O00 ['cedent_type'])#line:1243
            _OO0O00OOO00OOO0O0 =int (0 )#line:1244
            O000O0OOO00O00O00 ['num_cedent']=len (O000O0OOO00O00O00 ['defi'].get ('attributes'))#line:1249
            if (O000O0OOO00O00O00 ['defi'].get ('type')=='con'):#line:1250
                _OO0O00OOO00OOO0O0 =(1 <<O0OOOO000000O0OOO .data ["rows_count"])-1 #line:1251
            O0OOOO000000O0OOO ._genvar (OO00OO0OO0O000O00 ,O000O0OOO00O00O00 ,_O000OOO0OOOO00OOO ,_O0OO0OOOO0O000000 ,_OO0O00OOO00OOO0O0 ,O000O0OOO00O00O00 ['defi'].get ('minlen'),O000O0OOO00O00O00 ['defi'].get ('maxlen'))#line:1252
    def _calc_all (OOO0OOOO000O0O00O ,**O0O0O0OOOO0OO0O0O ):#line:1255
        if "df"in O0O0O0OOOO0OO0O0O :#line:1256
            OOO0OOOO000O0O00O ._prep_data (OOO0OOOO000O0O00O .kwargs .get ("df"))#line:1257
        if not (OOO0OOOO000O0O00O ._initialized ):#line:1258
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1259
        else :#line:1260
            OOO0OOOO000O0O00O ._calculate (**O0O0O0OOOO0OO0O0O )#line:1261
    def _check_cedents (OOOOOO00O0O0OO00O ,O00OO00OO00O0O0OO ,**O0000OOO0OO0OOOOO ):#line:1263
        OOO00O0OO000OOOO0 =True #line:1264
        if (O0000OOO0OO0OOOOO .get ('quantifiers',None )==None ):#line:1265
            print (f"Error: missing quantifiers.")#line:1266
            OOO00O0OO000OOOO0 =False #line:1267
            return OOO00O0OO000OOOO0 #line:1268
        if (type (O0000OOO0OO0OOOOO .get ('quantifiers'))!=dict ):#line:1269
            print (f"Error: quantifiers are not dictionary type.")#line:1270
            OOO00O0OO000OOOO0 =False #line:1271
            return OOO00O0OO000OOOO0 #line:1272
        for OOOOO0O0OO000OO00 in O00OO00OO00O0O0OO :#line:1274
            if (O0000OOO0OO0OOOOO .get (OOOOO0O0OO000OO00 ,None )==None ):#line:1275
                print (f"Error: cedent {OOOOO0O0OO000OO00} is missing in parameters.")#line:1276
                OOO00O0OO000OOOO0 =False #line:1277
                return OOO00O0OO000OOOO0 #line:1278
            OO0O0000O00OO0000 =O0000OOO0OO0OOOOO .get (OOOOO0O0OO000OO00 )#line:1279
            if (OO0O0000O00OO0000 .get ('minlen'),None )==None :#line:1280
                print (f"Error: cedent {OOOOO0O0OO000OO00} has no minimal length specified.")#line:1281
                OOO00O0OO000OOOO0 =False #line:1282
                return OOO00O0OO000OOOO0 #line:1283
            if not (type (OO0O0000O00OO0000 .get ('minlen'))is int ):#line:1284
                print (f"Error: cedent {OOOOO0O0OO000OO00} has invalid type of minimal length ({type(OO0O0000O00OO0000.get('minlen'))}).")#line:1285
                OOO00O0OO000OOOO0 =False #line:1286
                return OOO00O0OO000OOOO0 #line:1287
            if (OO0O0000O00OO0000 .get ('maxlen'),None )==None :#line:1288
                print (f"Error: cedent {OOOOO0O0OO000OO00} has no maximal length specified.")#line:1289
                OOO00O0OO000OOOO0 =False #line:1290
                return OOO00O0OO000OOOO0 #line:1291
            if not (type (OO0O0000O00OO0000 .get ('maxlen'))is int ):#line:1292
                print (f"Error: cedent {OOOOO0O0OO000OO00} has invalid type of maximal length.")#line:1293
                OOO00O0OO000OOOO0 =False #line:1294
                return OOO00O0OO000OOOO0 #line:1295
            if (OO0O0000O00OO0000 .get ('type'),None )==None :#line:1296
                print (f"Error: cedent {OOOOO0O0OO000OO00} has no type specified.")#line:1297
                OOO00O0OO000OOOO0 =False #line:1298
                return OOO00O0OO000OOOO0 #line:1299
            if not ((OO0O0000O00OO0000 .get ('type'))in (['con','dis'])):#line:1300
                print (f"Error: cedent {OOOOO0O0OO000OO00} has invalid type. Allowed values are 'con' and 'dis'.")#line:1301
                OOO00O0OO000OOOO0 =False #line:1302
                return OOO00O0OO000OOOO0 #line:1303
            if (OO0O0000O00OO0000 .get ('attributes'),None )==None :#line:1304
                print (f"Error: cedent {OOOOO0O0OO000OO00} has no attributes specified.")#line:1305
                OOO00O0OO000OOOO0 =False #line:1306
                return OOO00O0OO000OOOO0 #line:1307
            for OOO00O0000O0O0OO0 in OO0O0000O00OO0000 .get ('attributes'):#line:1308
                if (OOO00O0000O0O0OO0 .get ('name'),None )==None :#line:1309
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0} has no 'name' attribute specified.")#line:1310
                    OOO00O0OO000OOOO0 =False #line:1311
                    return OOO00O0OO000OOOO0 #line:1312
                if not ((OOO00O0000O0O0OO0 .get ('name'))in OOOOOO00O0O0OO00O .data ["varname"]):#line:1313
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} not in variable list. Please check spelling.")#line:1314
                    OOO00O0OO000OOOO0 =False #line:1315
                    return OOO00O0OO000OOOO0 #line:1316
                if (OOO00O0000O0O0OO0 .get ('type'),None )==None :#line:1317
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has no 'type' attribute specified.")#line:1318
                    OOO00O0OO000OOOO0 =False #line:1319
                    return OOO00O0OO000OOOO0 #line:1320
                if not ((OOO00O0000O0O0OO0 .get ('type'))in (['rcut','lcut','seq','subset','one'])):#line:1321
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has unsupported type {OOO00O0000O0O0OO0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one'.")#line:1322
                    OOO00O0OO000OOOO0 =False #line:1323
                    return OOO00O0OO000OOOO0 #line:1324
                if (OOO00O0000O0O0OO0 .get ('minlen'),None )==None :#line:1325
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has no minimal length specified.")#line:1326
                    OOO00O0OO000OOOO0 =False #line:1327
                    return OOO00O0OO000OOOO0 #line:1328
                if not (type (OOO00O0000O0O0OO0 .get ('minlen'))is int ):#line:1329
                    if not (OOO00O0000O0O0OO0 .get ('type')=='one'):#line:1330
                        print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has invalid type of minimal length.")#line:1331
                        OOO00O0OO000OOOO0 =False #line:1332
                        return OOO00O0OO000OOOO0 #line:1333
                if (OOO00O0000O0O0OO0 .get ('maxlen'),None )==None :#line:1334
                    print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has no maximal length specified.")#line:1335
                    OOO00O0OO000OOOO0 =False #line:1336
                    return OOO00O0OO000OOOO0 #line:1337
                if not (type (OOO00O0000O0O0OO0 .get ('maxlen'))is int ):#line:1338
                    if not (OOO00O0000O0O0OO0 .get ('type')=='one'):#line:1339
                        print (f"Error: cedent {OOOOO0O0OO000OO00} / attribute {OOO00O0000O0O0OO0.get('name')} has invalid type of maximal length.")#line:1340
                        OOO00O0OO000OOOO0 =False #line:1341
                        return OOO00O0OO000OOOO0 #line:1342
        return OOO00O0OO000OOOO0 #line:1343
    def _calculate (OOO00O000OOOO00OO ,**OOO0O00OOO0OOOOO0 ):#line:1345
        if OOO00O000OOOO00OO .data ["data_prepared"]==0 :#line:1346
            print ("Error: data not prepared")#line:1347
            return #line:1348
        OOO00O000OOOO00OO .kwargs =OOO0O00OOO0OOOOO0 #line:1349
        OOO00O000OOOO00OO .proc =OOO0O00OOO0OOOOO0 .get ('proc')#line:1350
        OOO00O000OOOO00OO .quantifiers =OOO0O00OOO0OOOOO0 .get ('quantifiers')#line:1351
        OOO00O000OOOO00OO ._init_task ()#line:1353
        OOO00O000OOOO00OO .stats ['start_proc_time']=time .time ()#line:1354
        OOO00O000OOOO00OO .task_actinfo ['cedents_to_do']=[]#line:1355
        OOO00O000OOOO00OO .task_actinfo ['cedents']=[]#line:1356
        if OOO0O00OOO0OOOOO0 .get ("proc")=='UICMiner':#line:1359
            if not (OOO00O000OOOO00OO ._check_cedents (['ante'],**OOO0O00OOO0OOOOO0 )):#line:1360
                return #line:1361
            _OO00000OOOO0O000O =OOO0O00OOO0OOOOO0 .get ("cond")#line:1363
            if _OO00000OOOO0O000O !=None :#line:1364
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1365
            else :#line:1366
                OO00OO00O00O0O00O =OOO00O000OOOO00OO .cedent #line:1367
                OO00OO00O00O0O00O ['cedent_type']='cond'#line:1368
                OO00OO00O00O0O00O ['filter_value']=(1 <<OOO00O000OOOO00OO .data ["rows_count"])-1 #line:1369
                OO00OO00O00O0O00O ['generated_string']='---'#line:1370
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1372
                OOO00O000OOOO00OO .task_actinfo ['cedents'].append (OO00OO00O00O0O00O )#line:1373
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('ante')#line:1374
            if OOO0O00OOO0OOOOO0 .get ('target',None )==None :#line:1375
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:1376
                return #line:1377
            if not (OOO0O00OOO0OOOOO0 .get ('target')in OOO00O000OOOO00OO .data ["varname"]):#line:1378
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1379
                return #line:1380
            if ("aad_score"in OOO00O000OOOO00OO .quantifiers ):#line:1381
                if not ("aad_weights"in OOO00O000OOOO00OO .quantifiers ):#line:1382
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1383
                    return #line:1384
                if not (len (OOO00O000OOOO00OO .quantifiers .get ("aad_weights"))==len (OOO00O000OOOO00OO .data ["dm"][OOO00O000OOOO00OO .data ["varname"].index (OOO00O000OOOO00OO .kwargs .get ('target'))])):#line:1385
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1386
                    return #line:1387
        elif OOO0O00OOO0OOOOO0 .get ("proc")=='CFMiner':#line:1388
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do']=['cond']#line:1389
            if OOO0O00OOO0OOOOO0 .get ('target',None )==None :#line:1390
                print ("ERROR: no target variable defined for CF Miner")#line:1391
                return #line:1392
            if not (OOO00O000OOOO00OO ._check_cedents (['cond'],**OOO0O00OOO0OOOOO0 )):#line:1393
                return #line:1394
            if not (OOO0O00OOO0OOOOO0 .get ('target')in OOO00O000OOOO00OO .data ["varname"]):#line:1395
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:1396
                return #line:1397
            if ("aad"in OOO00O000OOOO00OO .quantifiers ):#line:1398
                if not ("aad_weights"in OOO00O000OOOO00OO .quantifiers ):#line:1399
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:1400
                    return #line:1401
                if not (len (OOO00O000OOOO00OO .quantifiers .get ("aad_weights"))==len (OOO00O000OOOO00OO .data ["dm"][OOO00O000OOOO00OO .data ["varname"].index (OOO00O000OOOO00OO .kwargs .get ('target'))])):#line:1402
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:1403
                    return #line:1404
        elif OOO0O00OOO0OOOOO0 .get ("proc")=='4ftMiner':#line:1407
            if not (OOO00O000OOOO00OO ._check_cedents (['ante','succ'],**OOO0O00OOO0OOOOO0 )):#line:1408
                return #line:1409
            _OO00000OOOO0O000O =OOO0O00OOO0OOOOO0 .get ("cond")#line:1411
            if _OO00000OOOO0O000O !=None :#line:1412
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1413
            else :#line:1414
                OO00OO00O00O0O00O =OOO00O000OOOO00OO .cedent #line:1415
                OO00OO00O00O0O00O ['cedent_type']='cond'#line:1416
                OO00OO00O00O0O00O ['filter_value']=(1 <<OOO00O000OOOO00OO .data ["rows_count"])-1 #line:1417
                OO00OO00O00O0O00O ['generated_string']='---'#line:1418
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1420
                OOO00O000OOOO00OO .task_actinfo ['cedents'].append (OO00OO00O00O0O00O )#line:1421
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('ante')#line:1425
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('succ')#line:1426
        elif OOO0O00OOO0OOOOO0 .get ("proc")=='NewAct4ftMiner':#line:1427
            _OO00000OOOO0O000O =OOO0O00OOO0OOOOO0 .get ("cond")#line:1430
            if _OO00000OOOO0O000O !=None :#line:1431
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1432
            else :#line:1433
                OO00OO00O00O0O00O =OOO00O000OOOO00OO .cedent #line:1434
                OO00OO00O00O0O00O ['cedent_type']='cond'#line:1435
                OO00OO00O00O0O00O ['filter_value']=(1 <<OOO00O000OOOO00OO .data ["rows_count"])-1 #line:1436
                OO00OO00O00O0O00O ['generated_string']='---'#line:1437
                print (OO00OO00O00O0O00O ['filter_value'])#line:1438
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1439
                OOO00O000OOOO00OO .task_actinfo ['cedents'].append (OO00OO00O00O0O00O )#line:1440
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('antv')#line:1441
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('sucv')#line:1442
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('ante')#line:1443
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('succ')#line:1444
        elif OOO0O00OOO0OOOOO0 .get ("proc")=='Act4ftMiner':#line:1445
            _OO00000OOOO0O000O =OOO0O00OOO0OOOOO0 .get ("cond")#line:1448
            if _OO00000OOOO0O000O !=None :#line:1449
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1450
            else :#line:1451
                OO00OO00O00O0O00O =OOO00O000OOOO00OO .cedent #line:1452
                OO00OO00O00O0O00O ['cedent_type']='cond'#line:1453
                OO00OO00O00O0O00O ['filter_value']=(1 <<OOO00O000OOOO00OO .data ["rows_count"])-1 #line:1454
                OO00OO00O00O0O00O ['generated_string']='---'#line:1455
                print (OO00OO00O00O0O00O ['filter_value'])#line:1456
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1457
                OOO00O000OOOO00OO .task_actinfo ['cedents'].append (OO00OO00O00O0O00O )#line:1458
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('antv-')#line:1459
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('antv+')#line:1460
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('sucv-')#line:1461
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('sucv+')#line:1462
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('ante')#line:1463
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('succ')#line:1464
        elif OOO0O00OOO0OOOOO0 .get ("proc")=='SD4ftMiner':#line:1465
            if not (OOO00O000OOOO00OO ._check_cedents (['ante','succ','frst','scnd'],**OOO0O00OOO0OOOOO0 )):#line:1468
                return #line:1469
            _OO00000OOOO0O000O =OOO0O00OOO0OOOOO0 .get ("cond")#line:1470
            if _OO00000OOOO0O000O !=None :#line:1471
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1472
            else :#line:1473
                OO00OO00O00O0O00O =OOO00O000OOOO00OO .cedent #line:1474
                OO00OO00O00O0O00O ['cedent_type']='cond'#line:1475
                OO00OO00O00O0O00O ['filter_value']=(1 <<OOO00O000OOOO00OO .data ["rows_count"])-1 #line:1476
                OO00OO00O00O0O00O ['generated_string']='---'#line:1477
                OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('cond')#line:1479
                OOO00O000OOOO00OO .task_actinfo ['cedents'].append (OO00OO00O00O0O00O )#line:1480
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('frst')#line:1481
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('scnd')#line:1482
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('ante')#line:1483
            OOO00O000OOOO00OO .task_actinfo ['cedents_to_do'].append ('succ')#line:1484
        else :#line:1485
            print ("Unsupported procedure")#line:1486
            return #line:1487
        print ("Will go for ",OOO0O00OOO0OOOOO0 .get ("proc"))#line:1488
        OOO00O000OOOO00OO .task_actinfo ['optim']={}#line:1491
        OO0000000O000OO0O =True #line:1492
        for OO0OOOO000O0000OO in OOO00O000OOOO00OO .task_actinfo ['cedents_to_do']:#line:1493
            try :#line:1494
                OOOO0O0O000OO000O =OOO00O000OOOO00OO .kwargs .get (OO0OOOO000O0000OO )#line:1495
                if OOOO0O0O000OO000O .get ('type')!='con':#line:1499
                    OO0000000O000OO0O =False #line:1500
            except :#line:1502
                OO0OOO0OOO0O0OOO0 =1 <2 #line:1503
        if OOO00O000OOOO00OO .options ['optimizations']==False :#line:1505
            OO0000000O000OO0O =False #line:1506
        OOOOO0O0O0O00OO0O ={}#line:1507
        OOOOO0O0O0O00OO0O ['only_con']=OO0000000O000OO0O #line:1508
        OOO00O000OOOO00OO .task_actinfo ['optim']=OOOOO0O0O0O00OO0O #line:1509
        print ("Starting to mine rules.")#line:1517
        OOO00O000OOOO00OO ._start_cedent (OOO00O000OOOO00OO .task_actinfo )#line:1518
        OOO00O000OOOO00OO .stats ['end_proc_time']=time .time ()#line:1520
        print ("Done. Total verifications : "+str (OOO00O000OOOO00OO .stats ['total_cnt'])+", rules "+str (OOO00O000OOOO00OO .stats ['total_valid'])+", times: prep "+"{:.2f}".format (OOO00O000OOOO00OO .stats ['end_prep_time']-OOO00O000OOOO00OO .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (OOO00O000OOOO00OO .stats ['end_proc_time']-OOO00O000OOOO00OO .stats ['start_proc_time'])+"sec")#line:1524
        OO0O00OOO000O0000 ={}#line:1525
        OOO0O00OOOO0OO000 ={}#line:1526
        OOO0O00OOOO0OO000 ["task_type"]=OOO0O00OOO0OOOOO0 .get ('proc')#line:1527
        OOO0O00OOOO0OO000 ["target"]=OOO0O00OOO0OOOOO0 .get ('target')#line:1529
        OOO0O00OOOO0OO000 ["self.quantifiers"]=OOO00O000OOOO00OO .quantifiers #line:1530
        if OOO0O00OOO0OOOOO0 .get ('cond')!=None :#line:1532
            OOO0O00OOOO0OO000 ['cond']=OOO0O00OOO0OOOOO0 .get ('cond')#line:1533
        if OOO0O00OOO0OOOOO0 .get ('ante')!=None :#line:1534
            OOO0O00OOOO0OO000 ['ante']=OOO0O00OOO0OOOOO0 .get ('ante')#line:1535
        if OOO0O00OOO0OOOOO0 .get ('succ')!=None :#line:1536
            OOO0O00OOOO0OO000 ['succ']=OOO0O00OOO0OOOOO0 .get ('succ')#line:1537
        if OOO0O00OOO0OOOOO0 .get ('opts')!=None :#line:1538
            OOO0O00OOOO0OO000 ['opts']=OOO0O00OOO0OOOOO0 .get ('opts')#line:1539
        OO0O00OOO000O0000 ["taskinfo"]=OOO0O00OOOO0OO000 #line:1540
        O0OO0O0OO000OOOO0 ={}#line:1541
        O0OO0O0OO000OOOO0 ["total_verifications"]=OOO00O000OOOO00OO .stats ['total_cnt']#line:1542
        O0OO0O0OO000OOOO0 ["valid_rules"]=OOO00O000OOOO00OO .stats ['total_valid']#line:1543
        O0OO0O0OO000OOOO0 ["total_verifications_with_opt"]=OOO00O000OOOO00OO .stats ['total_ver']#line:1544
        O0OO0O0OO000OOOO0 ["time_prep"]=OOO00O000OOOO00OO .stats ['end_prep_time']-OOO00O000OOOO00OO .stats ['start_prep_time']#line:1545
        O0OO0O0OO000OOOO0 ["time_processing"]=OOO00O000OOOO00OO .stats ['end_proc_time']-OOO00O000OOOO00OO .stats ['start_proc_time']#line:1546
        O0OO0O0OO000OOOO0 ["time_total"]=OOO00O000OOOO00OO .stats ['end_prep_time']-OOO00O000OOOO00OO .stats ['start_prep_time']+OOO00O000OOOO00OO .stats ['end_proc_time']-OOO00O000OOOO00OO .stats ['start_proc_time']#line:1547
        OO0O00OOO000O0000 ["summary_statistics"]=O0OO0O0OO000OOOO0 #line:1548
        OO0O00OOO000O0000 ["rules"]=OOO00O000OOOO00OO .rulelist #line:1549
        O0O0OO000000O0000 ={}#line:1550
        O0O0OO000000O0000 ["varname"]=OOO00O000OOOO00OO .data ["varname"]#line:1551
        O0O0OO000000O0000 ["catnames"]=OOO00O000OOOO00OO .data ["catnames"]#line:1552
        OO0O00OOO000O0000 ["datalabels"]=O0O0OO000000O0000 #line:1553
        OOO00O000OOOO00OO .result =OO0O00OOO000O0000 #line:1556
    def print_summary (O00O000O00O0000OO ):#line:1558
        print ("")#line:1559
        print ("CleverMiner task processing summary:")#line:1560
        print ("")#line:1561
        print (f"Task type : {O00O000O00O0000OO.result['taskinfo']['task_type']}")#line:1562
        print (f"Number of verifications : {O00O000O00O0000OO.result['summary_statistics']['total_verifications']}")#line:1563
        print (f"Number of rules : {O00O000O00O0000OO.result['summary_statistics']['valid_rules']}")#line:1564
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(O00O000O00O0000OO.result['summary_statistics']['time_total']))}")#line:1565
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(O00O000O00O0000OO.result['summary_statistics']['time_prep']))}")#line:1567
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(O00O000O00O0000OO.result['summary_statistics']['time_processing']))}")#line:1568
        print ("")#line:1569
    def print_hypolist (O000OOOO000OO0O00 ):#line:1571
        O000OOOO000OO0O00 .print_rulelist ();#line:1572
    def print_rulelist (O0O0OO00O0O00OO00 ,sortby =None ,storesorted =False ):#line:1574
        def O0O00OOOOOOOO0OO0 (O0OOO0O0000OO0000 ):#line:1575
            OO0OO000O0O0OO0OO =O0OOO0O0000OO0000 ["params"]#line:1576
            return OO0OO000O0O0OO0OO .get (sortby ,0 )#line:1577
        print ("")#line:1579
        print ("List of rules:")#line:1580
        if O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1581
            print ("RULEID BASE  CONF  AAD    Rule")#line:1582
        elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1583
            print ("RULEID BASE  AAD_SCORE  Rule")#line:1584
        elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1585
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:1586
        elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1587
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:1588
        else :#line:1589
            print ("Unsupported task type for rulelist")#line:1590
            return #line:1591
        O0O00O0OO000000O0 =O0O0OO00O0O00OO00 .result ["rules"]#line:1592
        if sortby is not None :#line:1593
            O0O00O0OO000000O0 =sorted (O0O00O0OO000000O0 ,key =O0O00OOOOOOOO0OO0 ,reverse =True )#line:1594
            if storesorted :#line:1595
                O0O0OO00O0O00OO00 .result ["rules"]=O0O00O0OO000000O0 #line:1596
        for O00O0000O0000O000 in O0O00O0OO000000O0 :#line:1598
            OOO0O0O00O00OOOO0 ="{:6d}".format (O00O0000O0000O000 ["rule_id"])#line:1599
            if O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:1600
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+"{:5d}".format (O00O0000O0000O000 ["params"]["base"])+" "+"{:.3f}".format (O00O0000O0000O000 ["params"]["conf"])+" "+"{:+.3f}".format (O00O0000O0000O000 ["params"]["aad"])#line:1602
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+O00O0000O0000O000 ["cedents_str"]["ante"]+" => "+O00O0000O0000O000 ["cedents_str"]["succ"]+" | "+O00O0000O0000O000 ["cedents_str"]["cond"]#line:1603
            elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="UICMiner":#line:1604
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+"{:5d}".format (O00O0000O0000O000 ["params"]["base"])+" "+"{:.3f}".format (O00O0000O0000O000 ["params"]["aad_score"])#line:1605
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +"     "+O00O0000O0000O000 ["cedents_str"]["ante"]+" => "+O0O0OO00O0O00OO00 .result ['taskinfo']['target']+"(*) | "+O00O0000O0000O000 ["cedents_str"]["cond"]#line:1606
            elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="CFMiner":#line:1607
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+"{:5d}".format (O00O0000O0000O000 ["params"]["base"])+" "+"{:5d}".format (O00O0000O0000O000 ["params"]["s_up"])+" "+"{:5d}".format (O00O0000O0000O000 ["params"]["s_down"])#line:1608
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+O00O0000O0000O000 ["cedents_str"]["cond"]#line:1609
            elif O0O0OO00O0O00OO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1610
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +" "+"{:5d}".format (O00O0000O0000O000 ["params"]["base1"])+" "+"{:5d}".format (O00O0000O0000O000 ["params"]["base2"])+"    "+"{:.3f}".format (O00O0000O0000O000 ["params"]["ratioconf"])+"    "+"{:+.3f}".format (O00O0000O0000O000 ["params"]["deltaconf"])#line:1611
                OOO0O0O00O00OOOO0 =OOO0O0O00O00OOOO0 +"  "+O00O0000O0000O000 ["cedents_str"]["ante"]+" => "+O00O0000O0000O000 ["cedents_str"]["succ"]+" | "+O00O0000O0000O000 ["cedents_str"]["cond"]+" : "+O00O0000O0000O000 ["cedents_str"]["frst"]+" x "+O00O0000O0000O000 ["cedents_str"]["scnd"]#line:1612
            print (OOO0O0O00O00OOOO0 )#line:1614
        print ("")#line:1615
    def print_hypo (O0O00O000OO00O00O ,OOO0OO0OOOO0OO0O0 ):#line:1617
        O0O00O000OO00O00O .print_rule (OOO0OO0OOOO0OO0O0 )#line:1618
    def print_rule (O00O0OO0OOOOOOO0O ,O00O00OO0000O00O0 ):#line:1621
        print ("")#line:1622
        if (O00O00OO0000O00O0 <=len (O00O0OO0OOOOOOO0O .result ["rules"])):#line:1623
            if O00O0OO0OOOOOOO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1624
                print ("")#line:1625
                O00O0O0O00O0OOOOO =O00O0OO0OOOOOOO0O .result ["rules"][O00O00OO0000O00O0 -1 ]#line:1626
                print (f"Rule id : {O00O0O0O00O0OOOOO['rule_id']}")#line:1627
                print ("")#line:1628
                print (f"Base : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['base'])}  Relative base : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_base'])}  CONF : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['conf'])}  AAD : {'{:+.3f}'.format(O00O0O0O00O0OOOOO['params']['aad'])}  BAD : {'{:+.3f}'.format(O00O0O0O00O0OOOOO['params']['bad'])}")#line:1629
                print ("")#line:1630
                print ("Cedents:")#line:1631
                print (f"  antecedent : {O00O0O0O00O0OOOOO['cedents_str']['ante']}")#line:1632
                print (f"  succcedent : {O00O0O0O00O0OOOOO['cedents_str']['succ']}")#line:1633
                print (f"  condition  : {O00O0O0O00O0OOOOO['cedents_str']['cond']}")#line:1634
                print ("")#line:1635
                print ("Fourfold table")#line:1636
                print (f"    |  S  |  ¬S |")#line:1637
                print (f"----|-----|-----|")#line:1638
                print (f" A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold'][0])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold'][1])}|")#line:1639
                print (f"----|-----|-----|")#line:1640
                print (f"¬A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold'][2])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold'][3])}|")#line:1641
                print (f"----|-----|-----|")#line:1642
            elif O00O0OO0OOOOOOO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1643
                print ("")#line:1644
                O00O0O0O00O0OOOOO =O00O0OO0OOOOOOO0O .result ["rules"][O00O00OO0000O00O0 -1 ]#line:1645
                print (f"Rule id : {O00O0O0O00O0OOOOO['rule_id']}")#line:1646
                print ("")#line:1647
                OO0000OO0OO0OO000 =""#line:1648
                if ('aad'in O00O0O0O00O0OOOOO ['params']):#line:1649
                    OO0000OO0OO0OO000 ="aad : "+str (O00O0O0O00O0OOOOO ['params']['aad'])#line:1650
                print (f"Base : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['base'])}  Relative base : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['max'])}  Histogram minimum : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_min'])} {OO0000OO0OO0OO000}")#line:1652
                print ("")#line:1653
                print (f"Condition  : {O00O0O0O00O0OOOOO['cedents_str']['cond']}")#line:1654
                print ("")#line:1655
                print (f"Histogram                      {O00O0O0O00O0OOOOO['params']['hist']}")#line:1656
                if ('aad'in O00O0O0O00O0OOOOO ['params']):#line:1657
                    print (f"Histogram on full set          {O00O0O0O00O0OOOOO['params']['hist_full']}")#line:1658
                    print (f"Relative histogram             {O00O0O0O00O0OOOOO['params']['rel_hist']}")#line:1659
                    print (f"Relative histogram on full set {O00O0O0O00O0OOOOO['params']['rel_hist_full']}")#line:1660
            elif O00O0OO0OOOOOOO0O .result ['taskinfo']['task_type']=="UICMiner":#line:1661
                print ("")#line:1662
                O00O0O0O00O0OOOOO =O00O0OO0OOOOOOO0O .result ["rules"][O00O00OO0000O00O0 -1 ]#line:1663
                print (f"Rule id : {O00O0O0O00O0OOOOO['rule_id']}")#line:1664
                print ("")#line:1665
                OO0000OO0OO0OO000 =""#line:1666
                if ('aad_score'in O00O0O0O00O0OOOOO ['params']):#line:1667
                    OO0000OO0OO0OO000 ="aad score : "+str (O00O0O0O00O0OOOOO ['params']['aad_score'])#line:1668
                print (f"Base : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['base'])}  Relative base : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_base'])}   {OO0000OO0OO0OO000}")#line:1670
                print ("")#line:1671
                print (f"Condition  : {O00O0O0O00O0OOOOO['cedents_str']['cond']}")#line:1672
                print (f"Antecedent : {O00O0O0O00O0OOOOO['cedents_str']['ante']}")#line:1673
                print ("")#line:1674
                print (f"Histogram                                        {O00O0O0O00O0OOOOO['params']['hist']}")#line:1675
                if ('aad_score'in O00O0O0O00O0OOOOO ['params']):#line:1676
                    print (f"Histogram on full set with condition             {O00O0O0O00O0OOOOO['params']['hist_cond']}")#line:1677
                    print (f"Relative histogram                               {O00O0O0O00O0OOOOO['params']['rel_hist']}")#line:1678
                    print (f"Relative histogram on full set with condition    {O00O0O0O00O0OOOOO['params']['rel_hist_cond']}")#line:1679
                O0O000O000O00O0OO =O00O0OO0OOOOOOO0O .result ['datalabels']['catnames'][O00O0OO0OOOOOOO0O .result ['datalabels']['varname'].index (O00O0OO0OOOOOOO0O .result ['taskinfo']['target'])]#line:1680
                print (" ")#line:1682
                print ("Interpretation:")#line:1683
                for O00OO0OO00O00O000 in range (len (O0O000O000O00O0OO )):#line:1684
                  O0OOO0O000OOOOO00 =0 #line:1685
                  if O00O0O0O00O0OOOOO ['params']['rel_hist'][O00OO0OO00O00O000 ]>0 :#line:1686
                      O0OOO0O000OOOOO00 =O00O0O0O00O0OOOOO ['params']['rel_hist'][O00OO0OO00O00O000 ]/O00O0O0O00O0OOOOO ['params']['rel_hist_cond'][O00OO0OO00O00O000 ]#line:1687
                  OO0OOOOO0OOOO00OO =''#line:1688
                  if not (O00O0O0O00O0OOOOO ['cedents_str']['cond']=='---'):#line:1689
                      OO0OOOOO0OOOO00OO ="For "+O00O0O0O00O0OOOOO ['cedents_str']['cond']+": "#line:1690
                  print (f"    {OO0OOOOO0OOOO00OO}{O00O0OO0OOOOOOO0O.result['taskinfo']['target']}({O0O000O000O00O0OO[O00OO0OO00O00O000]}) has occurence {'{:.1%}'.format(O00O0O0O00O0OOOOO['params']['rel_hist_cond'][O00OO0OO00O00O000])}, with antecedent it has occurence {'{:.1%}'.format(O00O0O0O00O0OOOOO['params']['rel_hist'][O00OO0OO00O00O000])}, that is {'{:.3f}'.format(O0OOO0O000OOOOO00)} times more.")#line:1692
            elif O00O0OO0OOOOOOO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1693
                print ("")#line:1694
                O00O0O0O00O0OOOOO =O00O0OO0OOOOOOO0O .result ["rules"][O00O00OO0000O00O0 -1 ]#line:1695
                print (f"Rule id : {O00O0O0O00O0OOOOO['rule_id']}")#line:1696
                print ("")#line:1697
                print (f"Base1 : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['base1'])} Base2 : {'{:5d}'.format(O00O0O0O00O0OOOOO['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O00O0O0O00O0OOOOO['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O00O0O0O00O0OOOOO['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O00O0O0O00O0OOOOO['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O00O0O0O00O0OOOOO['params']['ratioconf'])}")#line:1698
                print ("")#line:1699
                print ("Cedents:")#line:1700
                print (f"  antecedent : {O00O0O0O00O0OOOOO['cedents_str']['ante']}")#line:1701
                print (f"  succcedent : {O00O0O0O00O0OOOOO['cedents_str']['succ']}")#line:1702
                print (f"  condition  : {O00O0O0O00O0OOOOO['cedents_str']['cond']}")#line:1703
                print (f"  first set  : {O00O0O0O00O0OOOOO['cedents_str']['frst']}")#line:1704
                print (f"  second set : {O00O0O0O00O0OOOOO['cedents_str']['scnd']}")#line:1705
                print ("")#line:1706
                print ("Fourfold tables:")#line:1707
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:1708
                print (f"----|-----|-----|  ----|-----|-----| ")#line:1709
                print (f" A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold1'][0])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold2'][0])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold2'][1])}|")#line:1710
                print (f"----|-----|-----|  ----|-----|-----|")#line:1711
                print (f"¬A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold1'][2])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold2'][2])}|{'{:5d}'.format(O00O0O0O00O0OOOOO['params']['fourfold2'][3])}|")#line:1712
                print (f"----|-----|-----|  ----|-----|-----|")#line:1713
            else :#line:1714
                print ("Unsupported task type for rule details")#line:1715
            print ("")#line:1719
        else :#line:1720
            print ("No such rule.")#line:1721
    def get_rulecount (OO0O0O0OO0OO0OOOO ):#line:1723
        return len (OO0O0O0OO0OO0OOOO .result ["rules"])#line:1724
    def get_fourfold (O0OO0O0OO0OO0OO0O ,O00O0000O0OO0O000 ,order =0 ):#line:1726
        if (O00O0000O0OO0O000 <=len (O0OO0O0OO0OO0OO0O .result ["rules"])):#line:1728
            if O0OO0O0OO0OO0OO0O .result ['taskinfo']['task_type']=="4ftMiner":#line:1729
                O0O000O0O00000000 =O0OO0O0OO0OO0OO0O .result ["rules"][O00O0000O0OO0O000 -1 ]#line:1730
                return O0O000O0O00000000 ['params']['fourfold']#line:1731
            elif O0OO0O0OO0OO0OO0O .result ['taskinfo']['task_type']=="CFMiner":#line:1732
                print ("Error: fourfold for CFMiner is not defined")#line:1733
                return None #line:1734
            elif O0OO0O0OO0OO0OO0O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1735
                O0O000O0O00000000 =O0OO0O0OO0OO0OO0O .result ["rules"][O00O0000O0OO0O000 -1 ]#line:1736
                if order ==1 :#line:1737
                    return O0O000O0O00000000 ['params']['fourfold1']#line:1738
                if order ==2 :#line:1739
                    return O0O000O0O00000000 ['params']['fourfold2']#line:1740
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:1741
                return None #line:1742
            else :#line:1743
                print ("Unsupported task type for rule details")#line:1744
        else :#line:1745
            print ("No such rule.")#line:1746
    def get_hist (OOO0000OO0OO0OOOO ,OO0O00O000O0OO00O ):#line:1748
        if (OO0O00O000O0OO00O <=len (OOO0000OO0OO0OOOO .result ["rules"])):#line:1750
            if OOO0000OO0OO0OOOO .result ['taskinfo']['task_type']=="CFMiner":#line:1751
                OO0OOOOOOOO0OOOO0 =OOO0000OO0OO0OOOO .result ["rules"][OO0O00O000O0OO00O -1 ]#line:1752
                return OO0OOOOOOOO0OOOO0 ['params']['hist']#line:1753
            elif OOO0000OO0OO0OOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1754
                print ("Error: SD4ft-Miner has no histogram")#line:1755
                return None #line:1756
            elif OOO0000OO0OO0OOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:1757
                print ("Error: 4ft-Miner has no histogram")#line:1758
                return None #line:1759
            else :#line:1760
                print ("Unsupported task type for rule details")#line:1761
        else :#line:1762
            print ("No such rule.")#line:1763
    def get_hist_cond (OOO0O0O0OO00OO0OO ,O0000O00OO00O0O0O ):#line:1766
        if (O0000O00OO00O0O0O <=len (OOO0O0O0OO00OO0OO .result ["rules"])):#line:1768
            if OOO0O0O0OO00OO0OO .result ['taskinfo']['task_type']=="UICMiner":#line:1769
                O0OOOO000OO0O0O00 =OOO0O0O0OO00OO0OO .result ["rules"][O0000O00OO00O0O0O -1 ]#line:1770
                return O0OOOO000OO0O0O00 ['params']['hist_cond']#line:1771
            elif OOO0O0O0OO00OO0OO .result ['taskinfo']['task_type']=="CFMiner":#line:1772
                O0OOOO000OO0O0O00 =OOO0O0O0OO00OO0OO .result ["rules"][O0000O00OO00O0O0O -1 ]#line:1773
                return O0OOOO000OO0O0O00 ['params']['hist']#line:1774
            elif OOO0O0O0OO00OO0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1775
                print ("Error: SD4ft-Miner has no histogram")#line:1776
                return None #line:1777
            elif OOO0O0O0OO00OO0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:1778
                print ("Error: 4ft-Miner has no histogram")#line:1779
                return None #line:1780
            else :#line:1781
                print ("Unsupported task type for rule details")#line:1782
        else :#line:1783
            print ("No such rule.")#line:1784
    def get_quantifiers (OOO00OOO0O00O00O0 ,O00O0O0OO0O000OO0 ,order =0 ):#line:1786
        if (O00O0O0OO0O000OO0 <=len (OOO00OOO0O00O00O0 .result ["rules"])):#line:1788
            OO0OO0O0O0OO00O00 =OOO00OOO0O00O00O0 .result ["rules"][O00O0O0OO0O000OO0 -1 ]#line:1789
            if OOO00OOO0O00O00O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:1790
                return OO0OO0O0O0OO00O00 ['params']#line:1791
            elif OOO00OOO0O00O00O0 .result ['taskinfo']['task_type']=="CFMiner":#line:1792
                return OO0OO0O0O0OO00O00 ['params']#line:1793
            elif OOO00OOO0O00O00O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:1794
                return OO0OO0O0O0OO00O00 ['params']#line:1795
            else :#line:1796
                print ("Unsupported task type for rule details")#line:1797
        else :#line:1798
            print ("No such rule.")#line:1799
    def get_varlist (OO00000OO0OO0OO00 ):#line:1801
        return OO00000OO0OO0OO00 .result ["datalabels"]["varname"]#line:1802
    def get_category_names (OOOOOOO0OO00O0O00 ,varname =None ,varindex =None ):#line:1804
        OO00O0OOOOOOOO0OO =0 #line:1805
        if varindex is not None :#line:1806
            if OO00O0OOOOOOOO0OO >=0 &OO00O0OOOOOOOO0OO <len (OOOOOOO0OO00O0O00 .get_varlist ()):#line:1807
                OO00O0OOOOOOOO0OO =varindex #line:1808
            else :#line:1809
                print ("Error: no such variable.")#line:1810
                return #line:1811
        if (varname is not None ):#line:1812
            OO0000O0OOO0OO0O0 =OOOOOOO0OO00O0O00 .get_varlist ()#line:1813
            OO00O0OOOOOOOO0OO =OO0000O0OOO0OO0O0 .index (varname )#line:1814
            if OO00O0OOOOOOOO0OO ==-1 |OO00O0OOOOOOOO0OO <0 |OO00O0OOOOOOOO0OO >=len (OOOOOOO0OO00O0O00 .get_varlist ()):#line:1815
                print ("Error: no such variable.")#line:1816
                return #line:1817
        return OOOOOOO0OO00O0O00 .result ["datalabels"]["catnames"][OO00O0OOOOOOOO0OO ]#line:1818
    def print_data_definition (O0O0O0O00OO00O000 ):#line:1820
        OOO0OOOOOOO0O0O0O =O0O0O0O00OO00O000 .get_varlist ()#line:1821
        for OOOO0O0O00O00O0OO in OOO0OOOOOOO0O0O0O :#line:1822
            O000O0O0000OOOO0O =O0O0O0O00OO00O000 .get_category_names (OOOO0O0O00O00O0OO )#line:1823
            O0O00O00OOO0O0O00 =""#line:1824
            for OOOO00OO00000O00O in O000O0O0000OOOO0O :#line:1825
                O0O00O00OOO0O0O00 =O0O00O00OOO0O0O00 +str (OOOO00OO00000O00O )+" "#line:1826
            O0O00O00OOO0O0O00 =O0O00O00OOO0O0O00 [:-1 ]#line:1827
            print (f"Variable {OOOO0O0O00O00O0OO} has {len(OOO0OOOOOOO0O0O0O)} categories: {O0O00O00OOO0O0O00}")#line:1828
